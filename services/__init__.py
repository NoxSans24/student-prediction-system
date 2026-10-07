from .auth_service import AuthService
from .student_service import StudentService
from .academic_service import AcademicRecordService
from .analytics_service import AnalyticsService
from .risk_service import RiskService
from .prediction_service import MLService
from .insight_service import InsightService

__all__ = [
    'AuthService',
    'StudentService',
    'AcademicRecordService',
    'AnalyticsService',
    'RiskService',
    'MLService',
    'InsightService'
]
