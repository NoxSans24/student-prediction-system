import pandas as pd
import numpy as np
from database import db
from services.analytics_service import AnalyticsService
import logging

logger = logging.getLogger(__name__)

class InsightService:
    """Automated insight generation from data"""
    
    @staticmethod
    def generate_gpa_insight():
        """Generate GPA trend insight"""
        try:
            stats = AnalyticsService.get_gpa_statistics()
            trend = AnalyticsService.get_gpa_by_semester()
            
            if not stats or not trend:
                return None
            
            semesters = sorted([k for k in trend.keys()])
            if len(semesters) < 2:
                return None
            
            latest_sem = semesters[-1]
            prev_sem = semesters[-2]
            
            latest_gpa = trend[latest_sem]['avg_gpa']
            prev_gpa = trend[prev_sem]['avg_gpa']
            change = latest_gpa - prev_gpa
            change_pct = (change / prev_gpa * 100) if prev_gpa != 0 else 0
            
            if change > 0.1:
                return {
                    'type': 'gpa_improvement',
                    'priority': 'low',
                    'title': 'GPA Improvement',
                    'message': f'Average GPA increased by {change:.2f} ({change_pct:.1f}%) from {prev_sem} to {latest_sem}.',
                    'value': latest_gpa,
                    'change': change
                }
            elif change < -0.1:
                return {
                    'type': 'gpa_decline',
                    'priority': 'high',
                    'title': 'GPA Decline Detected',
                    'message': f'Average GPA decreased by {abs(change):.2f} ({abs(change_pct):.1f}%) from {prev_sem} to {latest_sem}.',
                    'value': latest_gpa,
                    'change': change
                }
            else:
                return {
                    'type': 'gpa_stable',
                    'priority': 'low',
                    'title': 'GPA Stable',
                    'message': f'Average GPA remains stable at {latest_gpa:.2f}.',
                    'value': latest_gpa,
                    'change': 0
                }
        except Exception as e:
            logger.error(f"Generate GPA insight error: {e}")
            return None
    
    @staticmethod
    def generate_distribution_insight():
        """Generate performance distribution insight"""
        try:
            dist = AnalyticsService.get_gpa_distribution()
            
            if not dist:
                return None
            
            total = sum(dist.values())
            if total == 0:
                return None
            
            best_category = max(dist, key=dist.get)
            best_pct = (dist[best_category] / total * 100)
            
            return {
                'type': 'performance_distribution',
                'priority': 'low',
                'title': 'Performance Distribution',
                'message': f'{best_category} performance is most common ({best_pct:.1f}% of students).',
                'value': dist,
                'change': None
            }
        except Exception as e:
            logger.error(f"Generate distribution insight error: {e}")
            return None
    
    @staticmethod
    def generate_attendance_insight():
        """Generate attendance-related insight"""
        try:
            records = db.fetch_all("""
                SELECT COUNT(*) as count, 
                       SUM(CASE WHEN attendance >= 75 THEN 1 ELSE 0 END) as good_attendance
                FROM academic_records
            """)
            
            if not records or not records[0]:
                return None
            
            total = records[0]['count']
            good = records[0]['good_attendance'] or 0
            
            if total == 0:
                return None
            
            good_pct = (good / total * 100)
            
            if good_pct < 70:
                return {
                    'type': 'attendance_concern',
                    'priority': 'high',
                    'title': 'Attendance Concern',
                    'message': f'Only {good_pct:.1f}% of students maintain good attendance (75%+).',
                    'value': good_pct,
                    'change': None
                }
            else:
                return {
                    'type': 'attendance_good',
                    'priority': 'low',
                    'title': 'Good Attendance Rate',
                    'message': f'{good_pct:.1f}% of students maintain good attendance levels.',
                    'value': good_pct,
                    'change': None
                }
        except Exception as e:
            logger.error(f"Generate attendance insight error: {e}")
            return None
    
    @staticmethod
    def generate_score_insight():
        """Generate score analysis insight"""
        try:
            analysis = AnalyticsService.get_score_analysis()
            
            if not analysis:
                return None
            
            scores = [analysis['assignment'], analysis['midterm'], analysis['final']]
            avg_score = np.mean(scores)
            
            if avg_score < 60:
                return {
                    'type': 'low_scores',
                    'priority': 'high',
                    'title': 'Low Average Scores',
                    'message': f'Average performance across assessments is {avg_score:.1f}%, indicating need for improvement.',
                    'value': avg_score,
                    'change': None
                }
            elif avg_score >= 75:
                return {
                    'type': 'strong_scores',
                    'priority': 'low',
                    'title': 'Strong Assessment Performance',
                    'message': f'Students demonstrate strong performance with an average score of {avg_score:.1f}%.',
                    'value': avg_score,
                    'change': None
                }
            else:
                return {
                    'type': 'average_scores',
                    'priority': 'low',
                    'title': 'Average Performance',
                    'message': f'Average assessment score is {avg_score:.1f}%, showing moderate performance.',
                    'value': avg_score,
                    'change': None
                }
        except Exception as e:
            logger.error(f"Generate score insight error: {e}")
            return None
    
    @staticmethod
    def generate_study_hours_insight():
        """Generate study hours insight"""
        try:
            records = db.fetch_all("""
                SELECT AVG(study_hours) as avg_study,
                       SUM(CASE WHEN study_hours >= 5 THEN 1 ELSE 0 END) as adequate_study
                FROM academic_records
            """)
            
            if not records or not records[0]:
                return None
            
            avg_study = records[0]['avg_study']
            
            if avg_study is None:
                return None
            
            if avg_study < 5:
                return {
                    'type': 'low_study_hours',
                    'priority': 'medium',
                    'title': 'Low Study Time',
                    'message': f'Average study hours ({avg_study:.1f}h) is below recommended level.',
                    'value': avg_study,
                    'change': None
                }
            else:
                return {
                    'type': 'adequate_study',
                    'priority': 'low',
                    'title': 'Adequate Study Time',
                    'message': f'Students maintain good study habits with an average of {avg_study:.1f}h per session.',
                    'value': avg_study,
                    'change': None
                }
        except Exception as e:
            logger.error(f"Generate study hours insight error: {e}")
            return None
    
    @staticmethod
    def generate_correlation_insight():
        """Generate correlation insight"""
        try:
            corr_matrix = AnalyticsService.get_correlation_matrix()
            
            if not corr_matrix or 'gpa' not in corr_matrix:
                return None
            
            gpa_corr = corr_matrix['gpa']
            
            # Find strongest correlation with GPA
            strongest = None
            strongest_val = 0
            
            for feature, corr_val in gpa_corr.items():
                if feature != 'gpa' and abs(corr_val) > abs(strongest_val):
                    strongest = feature
                    strongest_val = corr_val
            
            if strongest is None:
                return None
            
            feature_names = {
                'attendance': 'Attendance',
                'assignment_score': 'Assignment Score',
                'midterm_score': 'Midterm Score',
                'final_score': 'Final Score',
                'study_hours': 'Study Hours'
            }
            
            feature_display = feature_names.get(strongest, strongest)
            
            if abs(strongest_val) > 0.5:
                relationship = "strong positive" if strongest_val > 0 else "strong negative"
                return {
                    'type': 'strong_correlation',
                    'priority': 'low',
                    'title': f'{feature_display} Correlation',
                    'message': f'{feature_display} shows {relationship} relationship with GPA (r={strongest_val:.2f}).',
                    'value': strongest_val,
                    'change': None
                }
            elif abs(strongest_val) > 0.3:
                relationship = "moderate positive" if strongest_val > 0 else "moderate negative"
                return {
                    'type': 'moderate_correlation',
                    'priority': 'low',
                    'title': f'{feature_display} Relationship',
                    'message': f'{feature_display} has {relationship} correlation with GPA (r={strongest_val:.2f}).',
                    'value': strongest_val,
                    'change': None
                }
            
            return None
        except Exception as e:
            logger.error(f"Generate correlation insight error: {e}")
            return None
    
    @staticmethod
    def generate_risk_insight():
        """Generate risk assessment insight"""
        try:
            from services.risk_service import RiskService
            dist = RiskService.get_risk_distribution()
            
            if not dist:
                return None
            
            total = sum(dist.values())
            if total == 0:
                return None
            
            high_risk_pct = (dist['HIGH'] / total * 100) if total > 0 else 0
            
            if high_risk_pct > 10:
                return {
                    'type': 'high_risk_alert',
                    'priority': 'high',
                    'title': 'High Risk Alert',
                    'message': f'{high_risk_pct:.1f}% of students are classified as high risk.',
                    'value': high_risk_pct,
                    'change': None
                }
            elif dist['HIGH'] > 0:
                return {
                    'type': 'some_at_risk',
                    'priority': 'medium',
                    'title': 'Some Students At Risk',
                    'message': f'{dist["HIGH"]} students require academic attention.',
                    'value': dist['HIGH'],
                    'change': None
                }
            else:
                return {
                    'type': 'low_risk',
                    'priority': 'low',
                    'title': 'Overall Low Risk',
                    'message': 'Most students show stable academic performance.',
                    'value': high_risk_pct,
                    'change': None
                }
        except Exception as e:
            logger.error(f"Generate risk insight error: {e}")
            return None
    
    @staticmethod
    def generate_all_insights():
        """Generate all insights"""
        try:
            insights = []
            
            gpa_insight = InsightService.generate_gpa_insight()
            if gpa_insight:
                insights.append(gpa_insight)
            
            dist_insight = InsightService.generate_distribution_insight()
            if dist_insight:
                insights.append(dist_insight)
            
            att_insight = InsightService.generate_attendance_insight()
            if att_insight:
                insights.append(att_insight)
            
            score_insight = InsightService.generate_score_insight()
            if score_insight:
                insights.append(score_insight)
            
            study_insight = InsightService.generate_study_hours_insight()
            if study_insight:
                insights.append(study_insight)
            
            corr_insight = InsightService.generate_correlation_insight()
            if corr_insight:
                insights.append(corr_insight)
            
            risk_insight = InsightService.generate_risk_insight()
            if risk_insight:
                insights.append(risk_insight)
            
            # Sort by priority
            priority_order = {'high': 0, 'medium': 1, 'low': 2}
            insights.sort(key=lambda x: priority_order.get(x.get('priority', 'low'), 2))
            
            return insights
        except Exception as e:
            logger.error(f"Generate all insights error: {e}")
            return []
