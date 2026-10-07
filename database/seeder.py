import mysql.connector
from mysql.connector import Error
from config import Config
from werkzeug.security import generate_password_hash
import random
from datetime import datetime, timedelta
import logging

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class DatabaseSeeder:
    """Seed database with initial data"""
    
    def __init__(self):
        self.connection = None
    
    def connect(self):
        """Connect to database"""
        try:
            self.connection = mysql.connector.connect(
                host=Config.MYSQL_HOST,
                user=Config.MYSQL_USER,
                password=Config.MYSQL_PASSWORD,
                database=Config.MYSQL_DATABASE
            )
            logger.info("Connected to database for seeding")
            return True
        except Error as e:
            logger.error(f"Connection error: {e}")
            return False
    
    def execute(self, query, params=None):
        """Execute query"""
        try:
            cursor = self.connection.cursor()
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            self.connection.commit()
            return True
        except Error as e:
            logger.error(f"Query error: {e}")
            self.connection.rollback()
            return False
    
    def fetch_one(self, query, params=None):
        """Fetch one result"""
        try:
            cursor = self.connection.cursor(dictionary=True)
            if params:
                cursor.execute(query, params)
            else:
                cursor.execute(query)
            result = cursor.fetchone()
            cursor.close()
            return result
        except Error as e:
            logger.error(f"Fetch error: {e}")
            return None
    
    def seed_users(self):
        """Seed default users"""
        logger.info("Seeding users...")
        
        users = [
            {
                'username': 'admin',
                'email': 'admin@example.com',
                'password': 'admin123',
                'role': 'admin'
            },
            {
                'username': 'analyst',
                'email': 'analyst@example.com',
                'password': 'analyst123',
                'role': 'analyst'
            }
        ]
        
        for user in users:
            # Check if user exists
            check_query = "SELECT id FROM users WHERE username = %s"
            existing = self.fetch_one(check_query, (user['username'],))
            
            if existing:
                logger.info(f"User '{user['username']}' already exists, skipping")
                continue
            
            # Create user
            password_hash = generate_password_hash(user['password'], method='pbkdf2:sha256')
            insert_query = """
                INSERT INTO users (username, email, password_hash, role)
                VALUES (%s, %s, %s, %s)
            """
            if self.execute(insert_query, (user['username'], user['email'], password_hash, user['role'])):
                logger.info(f"✓ Created user: {user['username']} ({user['role']})")
            else:
                logger.error(f"✗ Failed to create user: {user['username']}")
    
    def seed_students(self, count=150):
        """Seed student data"""
        logger.info(f"Seeding {count} students...")
        
        majors = ['Informatics', 'Information Systems', 'Computer Engineering', 
                  'Information Technology', 'Data Science']
        
        for i in range(1, count + 1):
            student_id = f"202400{str(i).zfill(3)}"
            name = f"Mahasiswa_{i}"
            major = random.choice(majors)
            semester = random.randint(1, 8)
            
            # Check if student exists
            check_query = "SELECT id FROM students WHERE student_id = %s"
            existing = self.fetch_one(check_query, (student_id,))
            
            if existing:
                logger.debug(f"Student {student_id} already exists")
                continue
            
            insert_query = """
                INSERT INTO students (student_id, name, major, current_semester)
                VALUES (%s, %s, %s, %s)
            """
            self.execute(insert_query, (student_id, name, major, semester))
        
        logger.info(f"✓ Seeded {count} students")
    
    def seed_academic_records(self):
        """Seed academic records for students"""
        logger.info("Seeding academic records...")
        
        # Get all students
        query = "SELECT id, current_semester FROM students"
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query)
        students = cursor.fetchall()
        cursor.close()
        
        count = 0
        for student in students:
            student_id = student['id']
            current_semester = student['current_semester']
            
            # Create records for semesters 1 to current_semester
            for semester in range(1, current_semester + 1):
                # Check if record exists
                check_query = """
                    SELECT id FROM academic_records 
                    WHERE student_id = %s AND semester = %s
                """
                existing = self.fetch_one(check_query, (student_id, semester))
                
                if existing:
                    continue
                
                # Generate realistic academic data
                gpa = round(random.uniform(2.0, 4.0), 2)
                attendance = round(random.uniform(70, 100), 2)
                assignment_score = round(random.uniform(60, 100), 2)
                midterm_score = round(random.uniform(60, 100), 2)
                final_score = round(random.uniform(60, 100), 2)
                study_hours = round(random.uniform(2, 15), 2)
                
                # Determine academic status
                if gpa >= 3.5:
                    academic_status = 'Excellent'
                elif gpa >= 3.0:
                    academic_status = 'Good'
                elif gpa >= 2.5:
                    academic_status = 'Satisfactory'
                else:
                    academic_status = 'Poor'
                
                insert_query = """
                    INSERT INTO academic_records 
                    (student_id, semester, gpa, attendance, assignment_score, 
                     midterm_score, final_score, study_hours, academic_status)
                    VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
                """
                self.execute(insert_query, (
                    student_id, semester, gpa, attendance, assignment_score,
                    midterm_score, final_score, study_hours, academic_status
                ))
                count += 1
        
        logger.info(f"✓ Seeded {count} academic records")
    
    def seed_risk_assessments(self):
        """Seed risk assessments"""
        logger.info("Seeding risk assessments...")
        
        # Get all students
        query = "SELECT id FROM students"
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query)
        students = cursor.fetchall()
        cursor.close()
        
        risk_levels = ['LOW', 'MEDIUM', 'HIGH']
        count = 0
        
        for student in students:
            student_id = student['id']
            risk_level = random.choices(risk_levels, weights=[50, 35, 15])[0]
            
            gpa_risk = random.uniform(0, 3) if risk_level != 'LOW' else random.uniform(0, 1)
            attendance_risk = random.uniform(0, 3) if risk_level != 'LOW' else random.uniform(0, 1)
            score_trend_risk = random.uniform(0, 3) if risk_level != 'LOW' else random.uniform(0, 1)
            study_hours_risk = random.uniform(0, 3) if risk_level != 'LOW' else random.uniform(0, 1)
            
            insert_query = """
                INSERT INTO risk_assessments 
                (student_id, risk_level, gpa_risk, attendance_risk, 
                 score_trend_risk, study_hours_risk)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            self.execute(insert_query, (
                student_id, risk_level, gpa_risk, attendance_risk,
                score_trend_risk, study_hours_risk
            ))
            count += 1
        
        logger.info(f"✓ Seeded {count} risk assessments")
    
    def seed_prediction_results(self):
        """Seed sample prediction results"""
        logger.info("Seeding prediction results...")
        
        # Get academic records
        query = """
            SELECT ar.id, ar.student_id, ar.semester, ar.gpa
            FROM academic_records ar
            WHERE ar.semester < (SELECT MAX(current_semester) FROM students)
            LIMIT 100
        """
        cursor = self.connection.cursor(dictionary=True)
        cursor.execute(query)
        records = cursor.fetchall()
        cursor.close()
        
        models = ['LinearRegression', 'RandomForest', 'GradientBoosting']
        count = 0
        
        for record in records:
            student_id = record['student_id']
            semester = record['semester'] + 1
            actual_gpa = record['gpa']
            
            # Check if prediction exists
            check_query = """
                SELECT id FROM prediction_results 
                WHERE student_id = %s AND semester = %s
            """
            existing = self.fetch_one(check_query, (student_id, semester))
            
            if existing:
                continue
            
            predicted_gpa = round(random.uniform(2.0, 4.0), 2)
            model_used = random.choice(models)
            mae = round(abs(predicted_gpa - actual_gpa), 4)
            rmse = round(mae * 1.2, 4)
            r_squared = round(random.uniform(0.7, 0.95), 4)
            
            insert_query = """
                INSERT INTO prediction_results 
                (student_id, semester, predicted_gpa, actual_gpa, model_used, mae, rmse, r_squared)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """
            self.execute(insert_query, (
                student_id, semester, predicted_gpa, actual_gpa, 
                model_used, mae, rmse, r_squared
            ))
            count += 1
        
        logger.info(f"✓ Seeded {count} prediction results")
    
    def run(self, count=150):
        """Run all seeders"""
        if not self.connect():
            logger.error("Failed to connect to database")
            return False
        
        try:
            logger.info("=" * 50)
            logger.info("Starting database seeding...")
            logger.info("=" * 50)
            
            self.seed_users()
            self.seed_students(count)
            self.seed_academic_records()
            self.seed_risk_assessments()
            self.seed_prediction_results()
            
            logger.info("=" * 50)
            logger.info("✓ Database seeding completed successfully!")
            logger.info("=" * 50)
            logger.info("\nDefault credentials:")
            logger.info("  Admin:    admin / admin123")
            logger.info("  Analyst:  analyst / analyst123")
            logger.info("=" * 50)
            
            return True
        except Exception as e:
            logger.error(f"Seeding error: {e}")
            return False
        finally:
            if self.connection and self.connection.is_connected():
                self.connection.close()

if __name__ == '__main__':
    seeder = DatabaseSeeder()
    seeder.run(count=150)
