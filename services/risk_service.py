from database import db
from config import Config
import logging

logger = logging.getLogger(__name__)

class RiskService:
    """Risk assessment and early warning system"""
    
    @staticmethod
    def assess_risk(student_id):
        """
        Assess academic risk for a student based on multiple factors
        Returns: LOW, MEDIUM, HIGH
        """
        try:
            # Get latest academic record
            latest_record = db.fetch_one("""
                SELECT gpa, attendance, assignment_score, midterm_score, 
                       final_score, study_hours, semester
                FROM academic_records
                WHERE student_id = %s
                ORDER BY semester DESC
                LIMIT 1
            """, (student_id,))
            
            if not latest_record:
                return None
            
            # Get previous record for trend analysis
            prev_record = db.fetch_one("""
                SELECT gpa, attendance, assignment_score, midterm_score, 
                       final_score, study_hours
                FROM academic_records
                WHERE student_id = %s
                ORDER BY semester DESC
                LIMIT 1 OFFSET 1
            """, (student_id,))
            
            risk_scores = {}
            
            # GPA Risk
            current_gpa = latest_record['gpa']
            if current_gpa < Config.RISK_GPA_MEDIUM_THRESHOLD:
                risk_scores['gpa'] = 3.0  # High
            elif current_gpa < Config.RISK_GPA_LOW_THRESHOLD:
                risk_scores['gpa'] = 1.5  # Medium
            else:
                risk_scores['gpa'] = 0.0  # Low
            
            # GPA Trend Risk
            if prev_record:
                gpa_change = current_gpa - prev_record['gpa']
                if gpa_change < -0.5:
                    risk_scores['gpa_trend'] = 3.0  # Significant decline
                elif gpa_change < -0.2:
                    risk_scores['gpa_trend'] = 1.5  # Moderate decline
                else:
                    risk_scores['gpa_trend'] = 0.0  # Stable or improving
            else:
                risk_scores['gpa_trend'] = 0.0
            
            # Attendance Risk
            attendance = latest_record['attendance']
            if attendance < Config.RISK_ATTENDANCE_THRESHOLD - 15:
                risk_scores['attendance'] = 3.0  # High
            elif attendance < Config.RISK_ATTENDANCE_THRESHOLD:
                risk_scores['attendance'] = 1.5  # Medium
            else:
                risk_scores['attendance'] = 0.0  # Low
            
            # Score Risk (assignment, midterm, final)
            assignment = latest_record['assignment_score']
            midterm = latest_record['midterm_score']
            final = latest_record['final_score']
            avg_score = (assignment + midterm + final) / 3
            
            if avg_score < Config.RISK_SCORE_THRESHOLD:
                risk_scores['scores'] = 3.0  # High
            elif avg_score < Config.RISK_SCORE_THRESHOLD + 10:
                risk_scores['scores'] = 1.5  # Medium
            else:
                risk_scores['scores'] = 0.0  # Low
            
            # Study Hours Risk
            study_hours = latest_record['study_hours']
            if study_hours < 5:
                risk_scores['study_hours'] = 2.0  # Medium
            else:
                risk_scores['study_hours'] = 0.0  # Low
            
            # Calculate overall risk level
            avg_risk = sum(risk_scores.values()) / len(risk_scores)
            
            if avg_risk >= 2.0:
                risk_level = 'HIGH'
            elif avg_risk >= 1.0:
                risk_level = 'MEDIUM'
            else:
                risk_level = 'LOW'
            
            return {
                'risk_level': risk_level,
                'gpa_risk': risk_scores.get('gpa', 0),
                'attendance_risk': risk_scores.get('attendance', 0),
                'score_trend_risk': risk_scores.get('scores', 0),
                'study_hours_risk': risk_scores.get('study_hours', 0),
                'scores': risk_scores
            }
        except Exception as e:
            logger.error(f"Assess risk error: {e}")
            return None
    
    @staticmethod
    def save_risk_assessment(student_id, risk_data):
        """Save risk assessment to database"""
        try:
            query = """
                INSERT INTO risk_assessments 
                (student_id, risk_level, gpa_risk, attendance_risk, 
                 score_trend_risk, study_hours_risk)
                VALUES (%s, %s, %s, %s, %s, %s)
            """
            db.execute_query(query, (
                student_id,
                risk_data['risk_level'],
                risk_data.get('gpa_risk', 0),
                risk_data.get('attendance_risk', 0),
                risk_data.get('score_trend_risk', 0),
                risk_data.get('study_hours_risk', 0)
            ))
            logger.info(f"Risk assessment saved for student {student_id}")
            return True
        except Exception as e:
            logger.error(f"Save risk assessment error: {e}")
            return False
    
    @staticmethod
    def assess_all_students():
        """Assess risk for all students and save results"""
        try:
            students = db.fetch_all("SELECT id FROM students")
            count = 0
            
            for student in students:
                risk_data = RiskService.assess_risk(student['id'])
                if risk_data:
                    RiskService.save_risk_assessment(student['id'], risk_data)
                    count += 1
            
            logger.info(f"Risk assessment completed for {count} students")
            return count
        except Exception as e:
            logger.error(f"Assess all students error: {e}")
            return 0
    
    @staticmethod
    def get_latest_risk_assessment(student_id):
        """Get latest risk assessment for a student"""
        try:
            query = """
                SELECT id, student_id, risk_level, gpa_risk, attendance_risk,
                       score_trend_risk, study_hours_risk, assessment_date
                FROM risk_assessments
                WHERE student_id = %s
                ORDER BY assessment_date DESC
                LIMIT 1
            """
            assessment = db.fetch_one(query, (student_id,))
            return assessment
        except Exception as e:
            logger.error(f"Get latest risk assessment error: {e}")
            return None
    
    @staticmethod
    def get_risk_distribution():
        """Get distribution of risk levels across all students"""
        try:
            query = """
                SELECT risk_level, COUNT(*) as count
                FROM risk_assessments
                WHERE id IN (
                    SELECT MAX(id) FROM risk_assessments GROUP BY student_id
                )
                GROUP BY risk_level
            """
            results = db.fetch_all(query)
            
            distribution = {'LOW': 0, 'MEDIUM': 0, 'HIGH': 0}
            for row in results:
                distribution[row['risk_level']] = row['count']
            
            return distribution
        except Exception as e:
            logger.error(f"Get risk distribution error: {e}")
            return {'LOW': 0, 'MEDIUM': 0, 'HIGH': 0}
    
    @staticmethod
    def get_high_risk_students(limit=10):
        """Get students with high risk"""
        try:
            query = """
                SELECT DISTINCT ra.student_id, s.name, s.student_id, ra.risk_level,
                       ra.gpa_risk, ra.attendance_risk, ra.assessment_date
                FROM risk_assessments ra
                JOIN students s ON ra.student_id = s.id
                WHERE ra.id IN (
                    SELECT MAX(id) FROM risk_assessments GROUP BY student_id
                )
                AND ra.risk_level = 'HIGH'
                ORDER BY ra.assessment_date DESC
                LIMIT %s
            """
            students = db.fetch_all(query, (limit,))
            return students
        except Exception as e:
            logger.error(f"Get high risk students error: {e}")
            return []
    
    @staticmethod
    def get_risk_history(student_id):
        """Get risk assessment history for a student"""
        try:
            query = """
                SELECT id, risk_level, gpa_risk, attendance_risk,
                       score_trend_risk, study_hours_risk, assessment_date
                FROM risk_assessments
                WHERE student_id = %s
                ORDER BY assessment_date DESC
                LIMIT 10
            """
            history = db.fetch_all(query, (student_id,))
            return history
        except Exception as e:
            logger.error(f"Get risk history error: {e}")
            return []
