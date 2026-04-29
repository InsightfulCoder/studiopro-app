import sys
import os
import uuid
from datetime import datetime

import streamlit as st
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

@st.cache_data(ttl=60)
def get_trial_status(user_id):
    """Returns (is_eligible, count_remaining)"""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT COUNT(*) FROM image_history WHERE user_id = ?", (user_id,))
    count = cursor.fetchone()[0]
    conn.close()
    
    limit = 3
    is_eligible = count < limit
    remaining = max(0, limit - count)
    return is_eligible, remaining

@st.cache_data(ttl=60)
def get_recent_creations(user_id, limit=4):
    """Returns the latest N creations for a user."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute('''
        SELECT processed_image_path, style_applied, processing_date 
        FROM image_history 
        WHERE user_id = ? 
        ORDER BY processing_date DESC 
        LIMIT ?
    ''', (user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@st.cache_data(ttl=60)
def get_recent_activity(user_id, limit=6):
    """Returns recent activities for the timeline."""
    conn = get_connection()
    cursor = conn.cursor()
    # Combining image history and transactions for a full timeline
    cursor.execute('''
        SELECT 'generation' as type, style_applied as detail, processing_date as date 
        FROM image_history WHERE user_id = ?
        UNION ALL
        SELECT 'payment' as type, amount || ' ' || payment_status as detail, transaction_date as date 
        FROM transactions WHERE user_id = ?
        ORDER BY date DESC LIMIT ?
    ''', (user_id, user_id, limit))
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@st.cache_data(ttl=60)
def get_user_stats(user_id):
    """Returns total generations, exports, and credits."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM image_history WHERE user_id = ?", (user_id,))
    generations = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM transactions WHERE user_id = ? AND payment_status='SUCCESS'", (user_id,))
    purchases = cursor.fetchone()[0]
    
    conn.close()
    
    # Just mock some values for now since we don't have a credit system yet
    return {
        "generations": generations,
        "exports": generations, # Assuming every generation is exported for now
        "credits": purchases * 10 
    }

# --- ADMIN FUNCTIONS ---

@st.cache_data(ttl=300)
def get_admin_stats():
    """Returns system-wide statistics for the admin dashboard."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute("SELECT COUNT(*) FROM users")
    total_users = cursor.fetchone()[0]
    
    cursor.execute("SELECT COUNT(*) FROM image_history")
    total_generations = cursor.fetchone()[0]
    
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE payment_status='SUCCESS'")
    total_revenue = cursor.fetchone()[0] or 0.0
    
    # Simple 'Active Today' count based on image history date
    cursor.execute("SELECT COUNT(DISTINCT user_id) FROM image_history WHERE date(processing_date) = date('now')")
    active_today = cursor.fetchone()[0]
    
    conn.close()
    return {
        "total_users": total_users,
        "total_generations": total_generations,
        "total_revenue": total_revenue,
        "active_today": active_today
    }

@st.cache_data(ttl=300)
def get_all_users():
    """Returns all registered users for the admin management table."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT username, email, created_at, last_login FROM users ORDER BY created_at DESC")
    rows = cursor.fetchall()
    conn.close()
    return [dict(row) for row in rows]

@st.cache_data(ttl=300)
def get_all_transactions():
    """Returns all transaction records and summary metrics."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT t.transaction_id, u.username, t.amount, t.payment_status, t.transaction_date, t.payment_method 
        FROM transactions t
        JOIN users u ON t.user_id = u.user_id
        ORDER BY t.transaction_date DESC
    ''')
    rows = cursor.fetchall()
    
    cursor.execute("SELECT SUM(amount) FROM transactions WHERE payment_status='SUCCESS'")
    revenue = cursor.fetchone()[0] or 0.0
    
    cursor.execute("SELECT COUNT(*) FROM transactions WHERE payment_status='SUCCESS'")
    success_count = cursor.fetchone()[0]
    
    conn.close()
    return [dict(row) for row in rows], revenue, success_count

@st.cache_data(ttl=300)
def get_all_activity():
    """Returns all system image activity and popular style metrics."""
    conn = get_connection()
    cursor = conn.cursor()
    
    cursor.execute('''
        SELECT h.image_id, u.username, h.style_applied, h.processing_date 
        FROM image_history h
        JOIN users u ON h.user_id = u.user_id
        ORDER BY h.processing_date DESC
    ''')
    activity = cursor.fetchall()
    
    cursor.execute("SELECT style_applied, COUNT(*) as count FROM image_history GROUP BY style_applied ORDER BY count DESC LIMIT 1")
    popular = cursor.fetchone()
    popular_style = popular[0] if popular else "N/A"
    
    conn.close()
    return [dict(row) for row in activity], popular_style
