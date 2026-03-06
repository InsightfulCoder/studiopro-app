import re
import bcrypt
import sys
import os

# Add the parent directory to sys.path to allow imports from other folders
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from database.db_manager import get_connection

def validate_email(email):
    """Validates the email format."""
    return re.match(r"[^@]+@[^@]+\.[^@]+", email)

def validate_password(password):
    """
    Validates password strength:
    - Minimum 8 characters
    - At least one uppercase letter
    - At least one lowercase letter
    - At least one number
    - At least one special character
    """
    if len(password) < 8:
        return False
    if not re.search(r"[A-Z]", password):
        return False
    if not re.search(r"[a-z]", password):
        return False
    if not re.search(r"[0-9]", password):
        return False
    if not re.search(r"[!@#$%^&*(),.?\":{}|<>]", password):
        return False
    return True

def register_user(username, email, password):
    """Registers a new user in the database."""
    if not validate_email(email):
        return False, "Invalid email format."
    
    if not validate_password(password):
        return False, "Password must be at least 8 characters long and include uppercase, lowercase, numbers, and special characters."

    # Hash the password
    password_hash = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

    conn = get_connection()
    cursor = conn.cursor()

    try:
        cursor.execute("INSERT INTO users (username, email, password_hash) VALUES (?, ?, ?)", 
                       (username, email, password_hash))
        conn.commit()
        return True, "User registered successfully."
    except Exception as e:
        if "UNIQUE constraint failed: users.username" in str(e):
            return False, "Username already exists."
        elif "UNIQUE constraint failed: users.email" in str(e):
            return False, "Email already exists."
        else:
            return False, f"Registration failed: {str(e)}"
    finally:
        conn.close()

def authenticate_user(username_or_email, password):
    """Authenticates a user."""
    conn = get_connection()
    cursor = conn.cursor()

    cursor.execute("SELECT * FROM users WHERE username = ? OR email = ?", (username_or_email, username_or_email))
    user = cursor.fetchone()
    conn.close()

    if user and bcrypt.checkpw(password.encode('utf-8'), user['password_hash'].encode('utf-8')):
        return True, user
    return False, "Invalid username/email or password."

if __name__ == "__main__":
    # Simple test
    # Note: This will fail if the script is run directly due to relative import of db_manager
    # Testing should ideally be done through a separate test script or the main app
    pass
