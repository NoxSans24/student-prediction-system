from werkzeug.security import generate_password_hash, check_password_hash
from database import db
import logging

logger = logging.getLogger(__name__)

class AuthService:
    """Authentication service for user login/registration"""
    
    @staticmethod
    def register_user(username, email, password, role='analyst'):
        """Register new user"""
        try:
            password_hash = generate_password_hash(password, method='pbkdf2:sha256')
            query = """
                INSERT INTO users (username, email, password_hash, role)
                VALUES (%s, %s, %s, %s)
            """
            db.execute_query(query, (username, email, password_hash, role))
            logger.info(f"User registered: {username}")
            return True, "User registered successfully"
        except Exception as e:
            logger.error(f"Registration error: {e}")
            return False, str(e)
    
    @staticmethod
    def authenticate_user(username, password):
        """Authenticate user by username and password"""
        try:
            query = "SELECT id, username, role, password_hash FROM users WHERE username = %s"
            user = db.fetch_one(query, (username,))
            
            if user and check_password_hash(user['password_hash'], password):
                return True, user
            else:
                logger.warning(f"Authentication failed for: {username}")
                return False, None
        except Exception as e:
            logger.error(f"Authentication error: {e}")
            return False, None
    
    @staticmethod
    def get_user_by_id(user_id):
        """Get user information by ID"""
        try:
            query = "SELECT id, username, email, role FROM users WHERE id = %s"
            user = db.fetch_one(query, (user_id,))
            return user
        except Exception as e:
            logger.error(f"Get user error: {e}")
            return None
    
    @staticmethod
    def user_exists(username):
        """Check if user exists"""
        try:
            query = "SELECT id FROM users WHERE username = %s"
            user = db.fetch_one(query, (username,))
            return user is not None
        except Exception as e:
            logger.error(f"User exists check error: {e}")
            return False
