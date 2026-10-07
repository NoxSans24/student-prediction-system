from database import db
import logging

logger = logging.getLogger(__name__)

class AcademicRecordService:
    """Academic records management"""
    
    @staticmethod
    def create_record(student_id, semester, gpa, attendance, assignment_score, 
                     midterm_score, final_score, study_hours, academic_status=None):
        """Create academic record for a student"""
        try:
            # Validate data
            if not (0 <= gpa <= 4):
                return False, "GPA must be between 0 and 4"
            if not (0 <= attendance <= 100):
                return False, "Attendance must be between 0 and 100"
            if not (0 <= assignment_score <= 100):
                return False, "Assignment score must be between 0 and 100"
            if not (0 <= midterm_score <= 100):
                return False, "Midterm score must be between 0 and 100"
            if not (0 <= final_score <= 100):
                return False, "Final score must be between 0 and 100"
            if study_hours < 0:
                return False, "Study hours cannot be negative"
            if semester < 1:
                return False, "Semester must be >= 1"
            
            query = """
                INSERT INTO academic_records 
                (student_id, semester, gpa, attendance, assignment_score, 
                 midterm_score, final_score, study_hours, academic_status)
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """
            db.execute_query(query, (student_id, semester, gpa, attendance, 
                                    assignment_score, midterm_score, final_score, 
                                    study_hours, academic_status))
            logger.info(f"Academic record created for student {student_id}, semester {semester}")
            return True, "Record created successfully"
        except Exception as e:
            logger.error(f"Create record error: {e}")
            return False, str(e)
    
    @staticmethod
    def get_student_records(student_id):
        """Get all academic records for a student"""
        try:
            query = """
                SELECT id, student_id, semester, gpa, attendance, assignment_score,
                       midterm_score, final_score, study_hours, academic_status, created_at
                FROM academic_records
                WHERE student_id = %s
                ORDER BY semester ASC
            """
            records = db.fetch_all(query, (student_id,))
            return records
        except Exception as e:
            logger.error(f"Get student records error: {e}")
            return []
    
    @staticmethod
    def get_record_by_semester(student_id, semester):
        """Get academic record for specific semester"""
        try:
            query = """
                SELECT id, student_id, semester, gpa, attendance, assignment_score,
                       midterm_score, final_score, study_hours, academic_status, created_at
                FROM academic_records
                WHERE student_id = %s AND semester = %s
            """
            record = db.fetch_one(query, (student_id, semester))
            return record
        except Exception as e:
            logger.error(f"Get record by semester error: {e}")
            return None
    
    @staticmethod
    def get_latest_record(student_id):
        """Get latest academic record for a student"""
        try:
            query = """
                SELECT id, student_id, semester, gpa, attendance, assignment_score,
                       midterm_score, final_score, study_hours, academic_status, created_at
                FROM academic_records
                WHERE student_id = %s
                ORDER BY semester DESC
                LIMIT 1
            """
            record = db.fetch_one(query, (student_id,))
            return record
        except Exception as e:
            logger.error(f"Get latest record error: {e}")
            return None
    
    @staticmethod
    def update_record(record_id, **kwargs):
        """Update academic record"""
        try:
            allowed_fields = ['gpa', 'attendance', 'assignment_score', 'midterm_score', 
                            'final_score', 'study_hours', 'academic_status']
            
            updates = []
            params = []
            
            for field, value in kwargs.items():
                if field in allowed_fields and value is not None:
                    # Validate values
                    if field == 'gpa' and not (0 <= value <= 4):
                        return False, "GPA must be between 0 and 4"
                    if field in ['attendance', 'assignment_score', 'midterm_score', 'final_score']:
                        if not (0 <= value <= 100):
                            return False, f"{field} must be between 0 and 100"
                    if field == 'study_hours' and value < 0:
                        return False, "Study hours cannot be negative"
                    
                    updates.append(f"{field} = %s")
                    params.append(value)
            
            if not updates:
                return False, "No valid updates provided"
            
            params.append(record_id)
            query = f"UPDATE academic_records SET {', '.join(updates)} WHERE id = %s"
            db.execute_query(query, params)
            logger.info(f"Record {record_id} updated")
            return True, "Record updated successfully"
        except Exception as e:
            logger.error(f"Update record error: {e}")
            return False, str(e)
    
    @staticmethod
    def delete_record(record_id):
        """Delete academic record"""
        try:
            query = "DELETE FROM academic_records WHERE id = %s"
            db.execute_query(query, (record_id,))
            logger.info(f"Record {record_id} deleted")
            return True, "Record deleted successfully"
        except Exception as e:
            logger.error(f"Delete record error: {e}")
            return False, str(e)
    
    @staticmethod
    def get_all_records():
        """Get all academic records (for analytics)"""
        try:
            query = """
                SELECT id, student_id, semester, gpa, attendance, assignment_score,
                       midterm_score, final_score, study_hours, academic_status
                FROM academic_records
                ORDER BY student_id, semester
            """
            records = db.fetch_all(query)
            return records
        except Exception as e:
            logger.error(f"Get all records error: {e}")
            return []
    
    @staticmethod
    def get_records_by_semester(semester):
        """Get all records for a specific semester"""
        try:
            query = """
                SELECT id, student_id, semester, gpa, attendance, assignment_score,
                       midterm_score, final_score, study_hours
                FROM academic_records
                WHERE semester = %s
                ORDER BY student_id
            """
            records = db.fetch_all(query, (semester,))
            return records
        except Exception as e:
            logger.error(f"Get records by semester error: {e}")
            return []
