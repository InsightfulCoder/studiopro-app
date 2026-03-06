import sys
import os
import uuid
from datetime import datetime

# Add the parent directory to sys.path to allow imports from other folders
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.db_manager import get_connection

def log_image_history(user_id, original_path, processed_path, style):
    """Logs the image processing event in the database."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            INSERT INTO image_history (user_id, original_image_path, processed_image_path, style_applied)
            VALUES (?, ?, ?, ?)
        ''', (user_id, original_path, processed_path, style))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error logging image history: {e}")
        return False
    finally:
        conn.close()

def create_order(user_id, amount, payment_method="Razorpay"):
    """Creates a pending transaction record."""
    conn = get_connection()
    cursor = conn.cursor()
    order_id = f"ORDER_{uuid.uuid4().hex[:8].upper()}"
    try:
        cursor.execute('''
            INSERT INTO transactions (transaction_id, user_id, amount, payment_status, payment_method)
            VALUES (?, ?, ?, ?, ?)
        ''', (order_id, user_id, amount, "PENDING", payment_method))
        conn.commit()
        return order_id
    except Exception as e:
        print(f"Error creating order: {e}")
        return None
    finally:
        conn.close()

def update_payment_status(order_id, status):
    """Updates the status of a transaction."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute('''
            UPDATE transactions SET payment_status = ? WHERE transaction_id = ?
        ''', (status, order_id))
        conn.commit()
        return True
    except Exception as e:
        print(f"Error updating payment status: {e}")
        return False
    finally:
        conn.close()
