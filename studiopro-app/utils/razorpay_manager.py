import razorpay
import os

# You would normally get these from environment variables
RAZORPAY_KEY_ID = os.getenv("RAZORPAY_KEY_ID", "rzp_test_placeholder")
RAZORPAY_KEY_SECRET = os.getenv("RAZORPAY_KEY_SECRET", "secret_placeholder")

client = razorpay.Client(auth=(RAZORPAY_KEY_ID, RAZORPAY_KEY_SECRET))

def create_razorpay_order(amount_in_inr, receipt_id):
    """
    Creates a Razorpay order.
    Amount should be in INR (pass 10 for ₹10). 
    Razorpay expects amount in paise (10 INR = 1000 paise).
    """
    data = {
        "amount": amount_in_inr * 100,
        "currency": "INR",
        "receipt": receipt_id,
        "payment_capture": 1 # Auto capture
    }
    try:
        order = client.order.create(data=data)
        return order
    except Exception as e:
        print(f"Razorpay Error: {e}")
        return None

def verify_payment(payment_id, order_id, signature):
    """Verifies the payment signature."""
    try:
        client.utility.verify_payment_signature({
            'razorpay_order_id': order_id,
            'razorpay_payment_id': payment_id,
            'razorpay_signature': signature
        })
        return True
    except Exception:
        return False
