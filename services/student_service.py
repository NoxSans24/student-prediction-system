from database import db
import logging
from config import Config

logger = logging.getLogger(__name__)

class StudentService:
    """Student management service"""
    
    @staticmethod
    def get_all_students(page=1, limit=None):
        """Get all students with pagination"""
        if limit is None:
            limit = Config.ITEMS_PER_PAGE
        
        offset = (page - 1) * limit
        
        try:
            query = """
                SELECT id, student_id, name, major, current_semester, created_at
                FROM students
                ORDER BY name ASC
                LIMIT %s OFFSET %s
            """
            students = db.fetch_all(query, (limit, offset))
            
            # Get total count
            count_query = "SELECT COUNT(*) as total FROM students"
            count_result = db.fetch_one(count_query)
            total = count_result['total'] if count_result else 0
            
            return students, total
        except Exception as e:
            logger.error(f"Get all students error: {e}")
            return [], 0
    
    @staticmethod
    def get_student_by_id(student_id):
        """Get single student by ID"""
        try:
            query = """
                SELECT id, student_id, name, major, current_semester, created_at
                FROM students
                WHERE id = %s
            """
            student = db.fetch_one(query, (student_id,))
            return student
        except Exception as e:
            logger.error(f"Get student error: {e}")
            return None
    
    @staticmethod
    def get_student_by_student_id(student_id):
        """Get student by student_id (unique identifier)"""
        try:
            query = """
                SELECT id, student_id, name, major, current_semester, created_at
                FROM students
                WHERE student_id = %s
            """
            student = db.fetch_one(query, (student_id,))
            return student
        except Exception as e:
            logger.error(f"Get student by student_id error: {e}")
            return None
    
    @staticmethod
    def create_student(student_id, name, major, current_semester):
        """Create new student"""
        try:
            # Validate semester
            if current_semester < 1:
                return False, "Semester must be >= 1"
            
            query = """
                INSERT INTO students (student_id, name, major, current_semester)
                VALUES (%s, %s, %s, %s)
            """
            db.execute_query(query, (student_id, name, major, current_semester))
            logger.info(f"Student created: {student_id}")
            return True, "Student created successfully"
        except Exception as e:
            logger.error(f"Create student error: {e}")
            return False, str(e)
    
    @staticmethod
    def update_student(student_id, name=None, major=None, current_semester=None):
        """Update student information"""
        try:
            updates = []
            params = []
            
            if name is not None:
                updates.append("name = %s")
                params.append(name)
            if major is not None:
                updates.append("major = %s")
                params.append(major)
            if current_semester is not None:
                if current_semester < 1:
                    return False, "Semester must be >= 1"
                updates.append("current_semester = %s")
                params.append(current_semester)
            
            if not updates:
                return False, "No updates provided"
            
            params.append(student_id)
            query = f"UPDATE students SET {', '.join(updates)} WHERE id = %s"
            db.execute_query(query, params)
            logger.info(f"Student updated: {student_id}")
            return True, "Student updated successfully"
        except Exception as e:
            logger.error(f"Update student error: {e}")
            return False, str(e)
    
    @staticmethod
    def delete_student(student_id):
        """Delete student and related records"""
        try:
            query = "DELETE FROM students WHERE id = %s"
            db.execute_query(query, (student_id,))
            logger.info(f"Student deleted: {student_id}")
            return True, "Student deleted successfully"
        except Exception as e:
            logger.error(f"Delete student error: {e}")
            return False, str(e)
    
    @staticmethod
    def search_students(keyword, page=1):
        """Search students by name or student_id"""
        if not keyword:
            return [], 0
        
        limit = Config.ITEMS_PER_PAGE
        offset = (page - 1) * limit
        search_term = f"%{keyword}%"
        
        try:
            query = """
                SELECT id, student_id, name, major, current_semester, created_at
                FROM students
                WHERE name LIKE %s OR student_id LIKE %s
                ORDER BY name ASC
                LIMIT %s OFFSET %s
            """
            students = db.fetch_all(query, (search_term, search_term, limit, offset))
            
            count_query = """
                SELECT COUNT(*) as total FROM students
                WHERE name LIKE %s OR student_id LIKE %s
            """
            count_result = db.fetch_one(count_query, (search_term, search_term))
            total = count_result['total'] if count_result else 0
            
            return students, total
        except Exception as e:
            logger.error(f"Search students error: {e}")
            return [], 0
    
    @staticmethod
    def filter_students(major=None, semester=None, page=1):
        """Filter students by major and/or semester"""
        limit = Config.ITEMS_PER_PAGE
        offset = (page - 1) * limit
        
        try:
            conditions = []
            params = []
            
            if major:
                conditions.append("major = %s")
                params.append(major)
            if semester:
                conditions.append("current_semester = %s")
                params.append(semester)
            
            where_clause = " WHERE " + " AND ".join(conditions) if conditions else ""
            
            query = f"""
                SELECT id, student_id, name, major, current_semester, created_at
                FROM students
                {where_clause}
                ORDER BY name ASC
                LIMIT %s OFFSET %s
            """
            params.extend([limit, offset])
            
            students = db.fetch_all(query, params)
            
            count_query = f"SELECT COUNT(*) as total FROM students {where_clause}"
            count_result = db.fetch_one(count_query, params[:-2])
            total = count_result['total'] if count_result else 0
            
            return students, total
        except Exception as e:
            logger.error(f"Filter students error: {e}")
            return [], 0
    
    @staticmethod
    def get_majors():
        """Get list of all majors"""
        try:
            query = "SELECT DISTINCT major FROM students ORDER BY major ASC"
            results = db.fetch_all(query)
            return [row['major'] for row in results]
        except Exception as e:
            logger.error(f"Get majors error: {e}")
            return []
