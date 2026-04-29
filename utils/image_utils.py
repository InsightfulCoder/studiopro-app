import cv2
import numpy as np
from PIL import Image

def pil_to_cv2(image):
    """Converts a PIL image to an OpenCV image."""
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

def cv2_to_pil(image):
    """Converts an OpenCV image to a PIL image."""
    return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))

def detect_edges(image, threshold1=100, threshold2=200, aperture_size=3):
    """
    Applies Canny edge detection.
    Returns a binary edge mask.
    """
    img_cv2 = pil_to_cv2(image)
    gray = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)
    
    # Noise reduction before edge detection
    blurred = cv2.medianBlur(gray, 5)
    
    # Canny Edge Detection
    edges = cv2.Canny(blurred, threshold1, threshold2, apertureSize=aperture_size)
    return edges

def adaptive_threshold_edges(image, block_size=9, c_val=2):
    """
    Applies adaptive thresholding to detect edges.
    Returns a binary edge mask.
    """
    img_cv2 = pil_to_cv2(image)
    gray = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)
    
    # Noise reduction
    blurred = cv2.medianBlur(gray, 7)
    
    # Adaptive threshold
    edges = cv2.adaptiveThreshold(blurred, 255, 
                                 cv2.ADAPTIVE_THRESH_MEAN_C, 
                                 cv2.THRESH_BINARY, 
                                 block_size, c_val)
    return edges

def apply_bilateral_filter(image, d=9, sigma_color=75, sigma_space=75):
    """
    Applies bilateral filter for smoothing while preserving edges.
    """
    img_cv2 = pil_to_cv2(image)
    smoothed = cv2.bilateralFilter(img_cv2, d, sigma_color, sigma_space)
    return cv2_to_pil(smoothed)

def quantize_colors(image, k=8):
    """
    Reduces the number of colors in an image using K-means clustering.
    """
    img_cv2 = pil_to_cv2(image)
    data = img_cv2.reshape((-1, 3))
    data = np.float32(data)

    criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 10, 1.0)
    _, label, center = cv2.kmeans(data, k, None, criteria, 10, cv2.KMEANS_RANDOM_CENTERS)

    center = np.uint8(center)
    res = center[label.flatten()]
    res2 = res.reshape((img_cv2.shape))
    
    return cv2_to_pil(res2)

def cartoonify_classic(image, k=8, d=9, sigma=75):
    """
    Classic Cartoon: Smooth + Quantize + Bold Edges.
    """
    # 1. Smooth with Bilateral Filter
    smoothed = apply_bilateral_filter(image, d, sigma, sigma)
    
    # 2. Color Quantization
    quantized = quantize_colors(smoothed, k)
    
    # 3. Detect Edges
    edges = adaptive_threshold_edges(image)
    
    # 4. Combine (Mask quantized image with edges)
    # Convert quantized PIL to cv2
    q_cv2 = pil_to_cv2(quantized)
    # Convert edges to 3-channel
    edges_3 = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    
    # Combine (edges are black)
    cartoon = cv2.bitwise_and(q_cv2, edges_3)
    
    return cv2_to_pil(cartoon)

def pencil_sketch(image, k_size=21, sigma=0):
    """
    Sketch: Grayscale + Inverted Blur + Divide.
    """
    img_cv2 = pil_to_cv2(image)
    gray = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)
    
    # Invert
    inverted = 255 - gray
    
    # Blur
    blurred = cv2.GaussianBlur(inverted, (k_size, k_size), sigma)
    
    # Pencil Sketch = Gray / (255 - Blurred) * 255
    sketch = cv2.divide(gray, 255 - blurred, scale=256)
    
    return cv2_to_pil(cv2.cvtColor(sketch, cv2.COLOR_GRAY2BGR))

def pencil_color(image, k_size=21):
    """
    Pencil Color: Sketch mask over original colors.
    """
    img_cv2 = pil_to_cv2(image)
    sketch = pil_to_cv2(pencil_sketch(image, k_size))
    
    # Blend sketch and original image
    # We use a bitwise combination or simple weighted blend
    color_sketch = cv2.multiply(img_cv2, sketch, scale=1/256)
    
    return cv2_to_pil(color_sketch)

def style_anime(image):
    """
    Anime Style: Edge-preserved smoothing + High Brightness + Soft Quantization.
    """
    img_cv2 = pil_to_cv2(image)
    # 1. Smooth with large bilateral
    smoothed = cv2.bilateralFilter(img_cv2, 12, 80, 80)
    # 2. Increase brightness/gamma
    lookUpTable = np.empty((1,256), np.uint8)
    for i in range(256):
        lookUpTable[0,i] = np.clip(pow(i / 255.0, 0.8) * 255.0, 0, 255)
    anime = cv2.LUT(smoothed, lookUpTable)
    return cv2_to_pil(anime)

def style_pixar(image):
    """
    Pixar/3D Style: Multi-pass bilateral filter for plastic/soft look.
    """
    img_cv2 = pil_to_cv2(image)
    # Iterative bilateral filtering
    for _ in range(3):
        img_cv2 = cv2.bilateralFilter(img_cv2, 9, 50, 50)
    # Subtle color boost
    hsv = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2HSV).astype("float32")
    hsv[:,:,1] = hsv[:,:,1] * 1.2 # Saturation
    hsv[:,:,1] = np.clip(hsv[:,:,1], 0, 255)
    img_cv2 = cv2.cvtColor(hsv.astype("uint8"), cv2.COLOR_HSV2BGR)
    return cv2_to_pil(img_cv2)

def style_comic(image):
    """
    Comic Style: Heavy Black Edges + High Contrast + Quantization.
    """
    img_cv2 = pil_to_cv2(image)
    # 1. Strong Edges
    gray = cv2.cvtColor(img_cv2, cv2.COLOR_BGR2GRAY)
    edges = cv2.adaptiveThreshold(cv2.medianBlur(gray, 7), 255, 
                                 cv2.ADAPTIVE_THRESH_MEAN_C, 
                                 cv2.THRESH_BINARY, 9, 2)
    # 2. High Contrast Color
    quant = pil_to_cv2(quantize_colors(cv2_to_pil(img_cv2), k=8))
    # 3. Combine
    edges_3 = cv2.cvtColor(edges, cv2.COLOR_GRAY2BGR)
    comic = cv2.bitwise_and(quant, edges_3)
    return cv2_to_pil(comic)

def style_watercolor(image):
    """
    Watercolor: Multiscale smoothing + edge suppression.
    """
    img_cv2 = pil_to_cv2(image)
    # 1. Median blur many times
    temp = img_cv2.copy()
    for _ in range(5):
        temp = cv2.medianBlur(temp, 7)
    # 2. Edge suppression with original
    edges = detect_edges(image, 50, 150)
    edges_inv = 255 - edges
    edges_inv_3 = cv2.cvtColor(edges_inv, cv2.COLOR_GRAY2BGR)
    watercolor = cv2.bitwise_and(temp, edges_inv_3)
    return cv2_to_pil(watercolor)
