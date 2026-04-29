import sqlite3
import bcrypt
import sys
import os

# Add the parent directory to sys.path
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.db_manager import get_connection
from backend.auth import validate_email, validate_password

def update_profile(user_id, username, email):
    """Updates user's username and email."""
    if not validate_email(email):
        return False, "Invalid email format."

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("UPDATE users SET username = ?, email = ? WHERE user_id = ?", 
                       (username, email, user_id))
        conn.commit()
        return True, "Profile updated successfully."
    except Exception as e:
        if "UNIQUE constraint failed: users.username" in str(e):
            return False, "Username already exists."
        elif "UNIQUE constraint failed: users.email" in str(e):
            return False, "Email already exists."
        else:
            return False, f"Update failed: {str(e)}"
    finally:
        conn.close()

def update_password(user_id, current_password, new_password):
    """Updates user's password after verifying current password."""
    if not validate_password(new_password):
        return False, "New password does not meet strength requirements."

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("SELECT password_hash FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        
        if not row or not bcrypt.checkpw(current_password.encode('utf-8'), row['password_hash'].encode('utf-8')):
            return False, "Incorrect current password."

        # Hash the new password
        new_password_hash = bcrypt.hashpw(new_password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')
        
        cursor.execute("UPDATE users SET password_hash = ? WHERE user_id = ?", (new_password_hash, user_id))
        conn.commit()
        return True, "Password updated successfully."
    except Exception as e:
        return False, f"Password update failed: {str(e)}"
    finally:
        conn.close()

def get_user_by_id(user_id):
    """Fetches full user data by ID."""
    conn = get_connection()
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM users WHERE user_id = ?", (user_id,))
    user = cursor.fetchone()
    conn.close()
    return user

def get_credits(user_id):
    """Fetches the current credit balance for the user."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("SELECT credits FROM users WHERE user_id = ?", (user_id,))
        row = cursor.fetchone()
        return row['credits'] if row else 0
    except Exception:
        return 0
    finally:
        conn.close()

def add_credits(user_id, amount):
    """Adds the specified amount of credits to the user's balance."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET credits = credits + ? WHERE user_id = ?", (amount, user_id))
        conn.commit()
        return True
    except Exception:
        return False
    finally:
        conn.close()

def deduct_credit(user_id):
    """Deducts 1 credit from the user's balance."""
    conn = get_connection()
    cursor = conn.cursor()
    try:
        cursor.execute("UPDATE users SET credits = credits - 1 WHERE user_id = ? AND credits > 0", (user_id,))
        conn.commit()
        return cursor.rowcount > 0
    except Exception:
        return False
    finally:
        conn.close()
