import mysql.connector
from mysql.connector import Error
import logging
from config import Config

logger = logging.getLogger(__name__)

class DatabaseConnection:
    """MySQL database connection handler"""
    
    def __init__(self):
        self.connection = None
    
    def connect(self):
        """Establish database connection"""
        try:
            self.connection = mysql.connector.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DATABASE
            )
            logger.info("Database connection established")
            return self.connection
        except Error as e:
            logger.error(f"Database connection error: {e}")
            raise
    
    def disconnect(self):
        """Close database connection"""
        if self.connection and self.connection.is_connected():
            self.connection.close()
            logger.info("Database connection closed")
    
    def get_connection(self):
        """Get current connection"""
        if self.connection is None or not self.connection.is_connected():
            self.connect()
        return self.connection
    
    def execute_query(self, query, params=None):
        """Execute a query"""
        try:
            cursor = self.get_connection().cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return cursor
        except Error as e:
            logger.error(f"Query execution error: {e}")
            self.connection.rollback()
            raise
    
    def fetch_one(self, query, params=None):
        """Fetch one result"""
        try:
            cursor = self.get_connection().cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result
        except Error as e:
            logger.error(f"Fetch one error: {e}")
            raise
    
    def fetch_all(self, query, params=None):
        """Fetch all results"""
        try:
            cursor = self.get_connection().cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            results = cursor.fetchall()
            cursor.close()
            return results
        except Error as e:
            logger.error(f"Fetch all error: {e}")
            raise

# Global database instance
db = DatabaseConnection()
