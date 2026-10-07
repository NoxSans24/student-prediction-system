import pandas as pd
import numpy as np
from database import db
import logging

logger = logging.getLogger(__name__)

class AnalyticsService:
    """Analytics and data analysis service"""
    
    @staticmethod
    def get_gpa_statistics():
        """Get GPA statistics across all students"""
        try:
            records = db.fetch_all("""
                SELECT gpa FROM academic_records WHERE gpa IS NOT NULL
            """)
            
            if not records:
                return None
            
            gpas = [r['gpa'] for r in records]
            
            return {
                'mean': float(np.mean(gpas)),
                'median': float(np.median(gpas)),
                'std': float(np.std(gpas)),
                'min': float(np.min(gpas)),
                'max': float(np.max(gpas)),
                'count': len(gpas)
            }
        except Exception as e:
            logger.error(f"Get GPA statistics error: {e}")
            return None
    
    @staticmethod
    def get_gpa_distribution():
        """Get GPA distribution by categories"""
        try:
            records = db.fetch_all("""
                SELECT gpa FROM academic_records WHERE gpa IS NOT NULL
            """)
            
            if not records:
                return {}
            
            gpas = [r['gpa'] for r in records]
            
            excellent = len([g for g in gpas if g >= 3.5])
            good = len([g for g in gpas if 3.0 <= g < 3.5])
            average = len([g for g in gpas if 2.5 <= g < 3.0])
            poor = len([g for g in gpas if g < 2.5])
            
            return {
                'Excellent': excellent,
                'Good': good,
                'Average': average,
                'Poor': poor
            }
        except Exception as e:
            logger.error(f"Get GPA distribution error: {e}")
            return {}
    
    @staticmethod
    def get_gpa_by_semester():
        """Get average GPA by semester"""
        try:
            records = db.fetch_all("""
                SELECT semester, AVG(gpa) as avg_gpa, COUNT(*) as count
                FROM academic_records
                WHERE gpa IS NOT NULL
                GROUP BY semester
                ORDER BY semester ASC
            """)
            
            result = {}
            for r in records:
                result[f"S{r['semester']}"] = {
                    'avg_gpa': float(r['avg_gpa']) if r['avg_gpa'] else 0,
                    'count': r['count']
                }
            
            return result
        except Exception as e:
            logger.error(f"Get GPA by semester error: {e}")
            return {}
    
    @staticmethod
    def get_gpa_by_major():
        """Get average GPA by major"""
        try:
            records = db.fetch_all("""
                SELECT s.major, AVG(ar.gpa) as avg_gpa, COUNT(*) as count
                FROM academic_records ar
                JOIN students s ON ar.student_id = s.id
                WHERE ar.gpa IS NOT NULL
                GROUP BY s.major
                ORDER BY avg_gpa DESC
            """)
            
            result = {}
            for r in records:
                result[r['major']] = {
                    'avg_gpa': float(r['avg_gpa']) if r['avg_gpa'] else 0,
                    'count': r['count']
                }
            
            return result
        except Exception as e:
            logger.error(f"Get GPA by major error: {e}")
            return {}
    
    @staticmethod
    def get_gpa_trend(student_id=None):
        """Get GPA trend over semesters"""
        try:
            if student_id:
                query = """
                    SELECT semester, gpa
                    FROM academic_records
                    WHERE student_id = %s AND gpa IS NOT NULL
                    ORDER BY semester ASC
                """
                records = db.fetch_all(query, (student_id,))
            else:
                query = """
                    SELECT semester, AVG(gpa) as gpa
                    FROM academic_records
                    WHERE gpa IS NOT NULL
                    GROUP BY semester
                    ORDER BY semester ASC
                """
                records = db.fetch_all(query)
            
            result = {}
            for r in records:
                result[f"S{r['semester']}"] = float(r['gpa']) if r['gpa'] else 0
            
            return result
        except Exception as e:
            logger.error(f"Get GPA trend error: {e}")
            return {}
    
    @staticmethod
    def get_attendance_statistics():
        """Get attendance statistics"""
        try:
            records = db.fetch_all("""
                SELECT attendance FROM academic_records WHERE attendance IS NOT NULL
            """)
            
            if not records:
                return None
            
            attendances = [r['attendance'] for r in records]
            
            return {
                'mean': float(np.mean(attendances)),
                'median': float(np.median(attendances)),
                'std': float(np.std(attendances)),
                'min': float(np.min(attendances)),
                'max': float(np.max(attendances))
            }
        except Exception as e:
            logger.error(f"Get attendance statistics error: {e}")
            return None
    
    @staticmethod
    def get_correlation_matrix():
        """Get correlation matrix between features and GPA"""
        try:
            records = db.fetch_all("""
                SELECT gpa, attendance, assignment_score, midterm_score, 
                       final_score, study_hours
                FROM academic_records
                WHERE gpa IS NOT NULL
            """)
            
            if not records or len(records) < 2:
                return {}
            
            df = pd.DataFrame(records)
            df = df.dropna()
            
            if df.empty:
                return {}
            
            corr_matrix = df.corr().round(3)
            
            return corr_matrix.to_dict()
        except Exception as e:
            logger.error(f"Get correlation matrix error: {e}")
            return {}
    
    @staticmethod
    def get_attendance_vs_gpa_data():
        """Get attendance vs GPA scatter plot data"""
        try:
            records = db.fetch_all("""
                SELECT attendance, gpa
                FROM academic_records
                WHERE attendance IS NOT NULL AND gpa IS NOT NULL
            """)
            
            return records
        except Exception as e:
            logger.error(f"Get attendance vs GPA error: {e}")
            return []
    
    @staticmethod
    def get_study_hours_vs_gpa_data():
        """Get study hours vs GPA scatter plot data"""
        try:
            records = db.fetch_all("""
                SELECT study_hours, gpa
                FROM academic_records
                WHERE study_hours IS NOT NULL AND gpa IS NOT NULL
            """)
            
            return records
        except Exception as e:
            logger.error(f"Get study hours vs GPA error: {e}")
            return []
    
    @staticmethod
    def get_score_analysis():
        """Get score analysis (assignment, midterm, final vs GPA)"""
        try:
            records = db.fetch_all("""
                SELECT 
                    AVG(assignment_score) as avg_assignment,
                    AVG(midterm_score) as avg_midterm,
                    AVG(final_score) as avg_final,
                    AVG(gpa) as avg_gpa
                FROM academic_records
                WHERE assignment_score IS NOT NULL
            """)
            
            if records and records[0]:
                return {
                    'assignment': float(records[0]['avg_assignment']) if records[0]['avg_assignment'] else 0,
                    'midterm': float(records[0]['avg_midterm']) if records[0]['avg_midterm'] else 0,
                    'final': float(records[0]['avg_final']) if records[0]['avg_final'] else 0,
                    'gpa': float(records[0]['avg_gpa']) if records[0]['avg_gpa'] else 0
                }
            
            return {}
        except Exception as e:
            logger.error(f"Get score analysis error: {e}")
            return {}
    
    @staticmethod
    def get_total_students_count():
        """Get total number of students"""
        try:
            result = db.fetch_one("SELECT COUNT(*) as count FROM students")
            return result['count'] if result else 0
        except Exception as e:
            logger.error(f"Get total students error: {e}")
            return 0
    
    @staticmethod
    def get_at_risk_count():
        """Get count of at-risk students (latest assessment)"""
        try:
            result = db.fetch_one("""
                SELECT COUNT(DISTINCT student_id) as count
                FROM risk_assessments
                WHERE risk_level = 'HIGH'
                AND id IN (
                    SELECT MAX(id) FROM risk_assessments GROUP BY student_id
                )
            """)
            return result['count'] if result else 0
        except Exception as e:
            logger.error(f"Get at-risk count error: {e}")
            return 0
