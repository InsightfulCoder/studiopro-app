// --- Modal Logic ---
const authModal = document.getElementById('authModal');
const payModal = document.getElementById('paymentModal');

function openAuth(mode) { 
    if(authModal) {
        authModal.classList.remove('hidden'); 
        switchMode(mode); 
    }
}
function closeAuth() { if(authModal) authModal.classList.add('hidden'); }
function openPayment() { if(payModal) payModal.classList.remove('hidden'); }
function closePayment() { if(payModal) payModal.classList.add('hidden'); }

function switchMode(mode) {
    document.getElementById('loginForm').classList.toggle('hidden', mode !== 'login');
    document.getElementById('registerForm').classList.toggle('hidden', mode !== 'register');
}

// --- Slider Logic ---
function moveSlider() {
    const sliderVal = document.getElementById('compareSlider').value;
    const foreground = document.getElementById('foregroundWrapper');
    const sliderBtn = document.getElementById('sliderBtn');
    if(foreground) foreground.style.width = `${sliderVal}%`;
    if(sliderBtn) sliderBtn.style.left = `${sliderVal}%`;
}

// --- Image Handling ---
let currentFile = null;
const fileInput = document.getElementById('fileInput');

if (fileInput) {
    fileInput.addEventListener('change', handleFileSelect);
}

window.addEventListener('paste', e => {
    if(e.clipboardData.items[0].type.indexOf('image')!==-1) {
        handleFileSelect({ target: { files: [e.clipboardData.items[0].getAsFile()] } });
    }
});

function handleFileSelect(e) {
    currentFile = e.target.files[0];
    const url = URL.createObjectURL(currentFile);
    
    // Update both images so they show the uploaded file immediately
    const originalImg = document.getElementById('originalImg');
    const processedImg = document.getElementById('processedImg');
    
    if(originalImg) originalImg.src = url;
    if(processedImg) processedImg.src = url; 

    // Important: Fix aspect ratio for comparison
    const container = document.getElementById('compContainer');
    if(container) {
        const width = container.offsetWidth;
        if(originalImg) originalImg.style.width = width + 'px';
    }
}

// Keep images responsive on window resize
new ResizeObserver(() => {
    const container = document.getElementById('compContainer');
    if(container) {
        const width = container.offsetWidth;
        const orig = document.getElementById('originalImg');
        const proc = document.getElementById('processedImg');
        if(orig) orig.style.width = width + 'px';
        if(proc) proc.style.width = width + 'px';
    }
}).observe(document.body);

async function generate() {
    if (!currentFile) return alert("Upload an image first!");
    
    // SHOW LOADER
    const loader = document.getElementById('loader');
    if(loader) loader.classList.remove('hidden'); 
    
    const fd = new FormData();
    fd.append('file', currentFile);
    
    // Check if style exists, default to cartoon if not
    const styleInput = document.querySelector('input[name="style"]:checked');
    fd.append('style', styleInput ? styleInput.value : 'cartoon');

    try {
        const res = await fetch('/process', { method: 'POST', body: fd });
        const data = await res.json();
        
        // HIDE LOADER
        if(loader) loader.classList.add('hidden');

        if (data.auth_required) {
            alert(data.message);
            openPayment();
        } else {
            const processedUrl = data.image + "?t=" + Date.now();
            document.getElementById('processedImg').src = processedUrl;
            const dlBtn = document.getElementById('dlBtn');
            if(dlBtn) {
                dlBtn.href = data.image;
                dlBtn.classList.remove('hidden');
            }
            
            // Reset Slider to center
            const slider = document.getElementById('compareSlider');
            if(slider) {
                slider.value = 50;
                moveSlider();
            }
        }
    } catch (e) {
        if(loader) loader.classList.add('hidden');
        console.error(e);
        alert("Error generating image.");
    }
}

// --- Auth & Payment ---
async function processMockPayment() {
    const btn = document.querySelector('.btn-pay');
    const text = document.getElementById('payText');
    const loader = document.getElementById('payLoader');
    
    if(btn) {
        btn.disabled = true; 
        btn.style.background = "#64748b"; 
    }
    if(text) text.classList.add('hidden'); 
    if(loader) loader.classList.remove('hidden');
    
    await new Promise(r => setTimeout(r, 2000));
    
    const res = await fetch('/mock_payment', { method: 'POST' });
    const data = await res.json();
    
    if (data.success) { 
        alert("Payment Successful! ✅\n\nYou are now a Pro Member."); 
        location.reload(); 
    } else { 
        alert("Transaction Failed."); 
        if(btn) btn.disabled = false; 
    }
}

async function submitAuth(endpoint) {
    const prefix = endpoint === '/login' ? 'l' : 'r';
    const username = document.getElementById(prefix + '_user').value;
    const password = document.getElementById(prefix + '_pass').value;
    
    const res = await fetch(endpoint, { 
        method: 'POST', 
        headers: { 'Content-Type': 'application/json' }, 
        body: JSON.stringify({ username, password }) 
    });
    
    const data = await res.json();
    if (data.success) location.reload(); 
    else document.getElementById('authError').innerText = data.message;
}

async function deleteAsset(id) {
    if(!confirm("Delete this project?")) return;
    const res = await fetch('/delete_history', { 
        method: 'POST', 
        headers: { 'Content-Type': 'application/json' }, 
        body: JSON.stringify({ id: id }) 
    });
    
    const data = await res.json();
    if(data.success) { 
        const card = document.getElementById(`card-${id}`);
        if(card) card.remove(); 
        if(document.querySelectorAll('.h-card').length === 0) location.reload(); 
    }
}

// --- NEW FEATURE: QR Code & PWA Install ---
function showQRCode() {
    // 1. Get your live URL
    const url = window.location.href;
    // 2. Generate QR Image
    const qrImage = `https://api.qrserver.com/v1/create-qr-code/?size=200x200&data=${url}`;
    
    // 3. Create the Popup HTML
    const modalContent = `
        <div style="text-align:center; color: white;">
            <h2 style="margin-bottom:10px;">📲 Install StudioPro</h2>
            <p style="color:#94a3b8; margin-bottom:20px; font-size: 14px;">Scan this to open on your phone!</p>
            <div style="background: white; padding: 10px; display: inline-block; border-radius: 10px;">
                <img src="${qrImage}" style="display:block;">
            </div>
            <p style="margin-top:20px; font-size:12px; color:#64748b;">Tap "Add to Home Screen" on your mobile browser.</p>
            <button id="closeQR" style="margin-top:20px; background:transparent; border:1px solid #334155; color:white; padding:8px 20px; border-radius:8px; cursor:pointer;">Close</button>
        </div>
    `;
    
    // 4. Show it using the existing Modal Box
    const modalBox = document.querySelector('#authModal .modal-box');
    
    // Save original Login content so we don't lose it
    if(!window.originalAuthContent) window.originalAuthContent = modalBox.innerHTML;
    
    modalBox.innerHTML = modalContent;
    document.getElementById('authModal').classList.remove('hidden');
    
    // 5. Restore Login content when closed
    document.getElementById('closeQR').onclick = () => {
        document.getElementById('authModal').classList.add('hidden');
        setTimeout(() => modalBox.innerHTML = window.originalAuthContent, 300);
    };
}