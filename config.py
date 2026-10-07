import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    """Base configuration"""
    FLASK_ENV = os.getenv('FLASK_ENV', 'development')
    DEBUG = os.getenv('FLASK_DEBUG', False)
    SECRET_KEY = os.getenv('SECRET_KEY', 'dev-key-change-in-production')
    
    # MySQL
    MYSQL_HOST = os.getenv('MYSQL_HOST', 'localhost')
    MYSQL_USER = os.getenv('MYSQL_USER', 'root')
    MYSQL_PASSWORD = os.getenv('MYSQL_PASSWORD', '')
    MYSQL_DATABASE = os.getenv('MYSQL_DATABASE', 'student_performance_analytics')
    
    # Session
    SESSION_TYPE = os.getenv('SESSION_TYPE', 'filesystem')
    PERMANENT_SESSION_LIFETIME = int(os.getenv('PERMANENT_SESSION_LIFETIME', 1800))
    SESSION_PERMANENT = False
    SESSION_USE_SIGNER = True
    
    # Risk Engine Thresholds (configurable)
    RISK_GPA_LOW_THRESHOLD = 3.0
    RISK_GPA_MEDIUM_THRESHOLD = 2.5
    RISK_ATTENDANCE_THRESHOLD = 75.0
    RISK_SCORE_THRESHOLD = 60.0
    
    # ML Configuration
    ML_TRAIN_TEST_SPLIT = 0.2
    ML_RANDOM_STATE = 42
    
    # Pagination
    ITEMS_PER_PAGE = 20
