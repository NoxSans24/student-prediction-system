from flask import Flask, render_template, request, jsonify, session, redirect, url_for
from flask_session import Session
from config import Config
from database import db
from services import AuthService, StudentService, AcademicRecordService, AnalyticsService, RiskService, MLService, InsightService
import logging
from functools import wraps

app = Flask(__name__)
app.config.from_object(Config)
Session(app)

# Logging setup
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Initialize database connection
@app.before_request
def init_db():
    if db.connection is None:
        db.connect()

@app.teardown_appcontext
def close_db(error):
    pass

# Authentication decorator
def login_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        return f(*args, **kwargs)
    return decorated_function

def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        if 'user_id' not in session:
            return redirect(url_for('login'))
        if session.get('role') != 'admin':
            return jsonify({'success': False, 'error': {'code': 'unauthorized', 'message': 'Admin access required'}}), 403
        return f(*args, **kwargs)
    return decorated_function

# ==================== AUTH ROUTES ====================

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        password = data.get('password')
        
        success, user = AuthService.authenticate_user(username, password)
        
        if success:
            session['user_id'] = user['id']
            session['username'] = user['username']
            session['role'] = user['role']
            return jsonify({'success': True, 'redirect': url_for('dashboard')})
        else:
            return jsonify({'success': False, 'error': {'code': 'auth_failed', 'message': 'Invalid credentials'}}), 401
    
    return render_template('auth/login.html')

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        data = request.get_json()
        username = data.get('username')
        email = data.get('email')
        password = data.get('password')
        
        if AuthService.user_exists(username):
            return jsonify({'success': False, 'error': {'code': 'user_exists', 'message': 'Username already exists'}}), 400
        
        success, message = AuthService.register_user(username, email, password)
        
        if success:
            return jsonify({'success': True, 'message': message})
        else:
            return jsonify({'success': False, 'error': {'code': 'register_failed', 'message': message}}), 400
    
    return render_template('auth/register.html')

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

# ==================== DASHBOARD ROUTE ====================

@app.route('/')
@app.route('/dashboard')
@login_required
def dashboard():
    try:
        # Get KPI data
        total_students = AnalyticsService.get_total_students_count()
        at_risk = AnalyticsService.get_at_risk_count()
        gpa_stats = AnalyticsService.get_gpa_statistics()
        att_stats = AnalyticsService.get_attendance_statistics()
        
        # Get chart data
        gpa_trend = AnalyticsService.get_gpa_trend()
        gpa_dist = AnalyticsService.get_gpa_distribution()
        gpa_by_major = AnalyticsService.get_gpa_by_major()
        att_vs_gpa = AnalyticsService.get_attendance_vs_gpa_data()
        
        # Get insights
        insights = InsightService.generate_all_insights()
        
        # Get high risk students
        from services.risk_service import RiskService
        high_risk = RiskService.get_high_risk_students(5)
        
        return render_template('dashboard/dashboard.html', 
                            total_students=total_students,
                            at_risk=at_risk,
                            gpa_stats=gpa_stats,
                            att_stats=att_stats,
                            gpa_trend=gpa_trend,
                            gpa_dist=gpa_dist,
                            gpa_by_major=gpa_by_major,
                            att_vs_gpa=att_vs_gpa,
                            insights=insights,
                            high_risk=high_risk)
    except Exception as e:
        logger.error(f"Dashboard error: {e}")
        return render_template('errors/500.html', error=str(e)), 500

# ==================== STUDENTS ROUTES ====================

@app.route('/students')
@login_required
def students():
    try:
        page = request.args.get('page', 1, type=int)
        search = request.args.get('search', '')
        major = request.args.get('major')
        semester = request.args.get('semester', type=int)
        
        if search:
            students_list, total = StudentService.search_students(search, page)
        elif major or semester:
            students_list, total = StudentService.filter_students(major, semester, page)
        else:
            students_list, total = StudentService.get_all_students(page)
        
        majors = StudentService.get_majors()
        
        return render_template('students/students.html',
                            students=students_list,
                            total=total,
                            page=page,
                            majors=majors,
                            search=search)
    except Exception as e:
        logger.error(f"Students list error: {e}")
        return render_template('errors/500.html', error=str(e)), 500

@app.route('/api/students', methods=['POST'])
@admin_required
def create_student():
    try:
        data = request.get_json()
        success, message = StudentService.create_student(
            data.get('student_id'),
            data.get('name'),
            data.get('major'),
            data.get('current_semester')
        )
        
        if success:
            return jsonify({'success': True, 'message': message})
        else:
            return jsonify({'success': False, 'error': {'code': 'create_failed', 'message': message}}), 400
    except Exception as e:
        logger.error(f"Create student error: {e}")
        return jsonify({'success': False, 'error': {'code': 'error', 'message': str(e)}}), 500

@app.route('/api/students/<int:student_id>', methods=['PUT'])
@admin_required
def update_student(student_id):
    try:
        data = request.get_json()
        success, message = StudentService.update_student(
            student_id,
            name=data.get('name'),
            major=data.get('major'),
            current_semester=data.get('current_semester')
        )
        
        if success:
            return jsonify({'success': True, 'message': message})
        else:
            return jsonify({'success': False, 'error': {'code': 'update_failed', 'message': message}}), 400
    except Exception as e:
        logger.error(f"Update student error: {e}")
        return jsonify({'success': False, 'error': {'code': 'error', 'message': str(e)}}), 500

@app.route('/api/students/<int:student_id>', methods=['DELETE'])
@admin_required
def delete_student(student_id):
    try:
        success, message = StudentService.delete_student(student_id)
        
        if success:
            return jsonify({'success': True, 'message': message})
        else:
            return jsonify({'success': False, 'error': {'code': 'delete_failed', 'message': message}}), 400
    except Exception as e:
        logger.error(f"Delete student error: {e}")
        return jsonify({'success': False, 'error': {'code': 'error', 'message': str(e)}}), 500

# ==================== ANALYTICS ROUTES ====================

@app.route('/analytics')
@login_required
def analytics():
    try:
        gpa_trend = AnalyticsService.get_gpa_trend()
        gpa_dist = AnalyticsService.get_gpa_distribution()
        gpa_by_major = AnalyticsService.get_gpa_by_major()
        gpa_by_semester = AnalyticsService.get_gpa_by_semester()
        att_vs_gpa = AnalyticsService.get_attendance_vs_gpa_data()
        study_vs_gpa = AnalyticsService.get_study_hours_vs_gpa_data()
        score_analysis = AnalyticsService.get_score_analysis()
        corr_matrix = AnalyticsService.get_correlation_matrix()
        
        return render_template('analytics/analytics.html',
                            gpa_trend=gpa_trend,
                            gpa_dist=gpa_dist,
                            gpa_by_major=gpa_by_major,
                            gpa_by_semester=gpa_by_semester,
                            att_vs_gpa=att_vs_gpa,
                            study_vs_gpa=study_vs_gpa,
                            score_analysis=score_analysis,
                            corr_matrix=corr_matrix)
    except Exception as e:
        logger.error(f"Analytics error: {e}")
        return render_template('errors/500.html', error=str(e)), 500

# ==================== PREDICTION ROUTES ====================

@app.route('/prediction')
@login_required
def prediction():
    metadata = MLService.get_model_metadata()
    return render_template('prediction/prediction.html', model_metadata=metadata)

@app.route('/api/predict', methods=['POST'])
@login_required
def predict():
    try:
        data = request.get_json() or {}
        student_id = data.get('student_id')
        semester = data.get('semester')
        
        # If semester is not provided, look up from student profile or default to 1
        if (semester is None or semester == '') and student_id:
            try:
                student = StudentService.get_student_by_id(int(student_id))
                if student:
                    semester = student.get('current_semester', 1)
            except Exception:
                semester = 1
        if semester is None or semester == '':
            semester = 1
        else:
            semester = int(semester)
            
        attendance = float(data.get('attendance', 0))
        assignment_score = float(data.get('assignment_score', 0))
        midterm_score = float(data.get('midterm_score', 0))
        final_score = float(data.get('final_score', 0))
        study_hours = float(data.get('study_hours', 0))
        
        result, error = MLService.predict_gpa(
            semester,
            attendance,
            assignment_score,
            midterm_score,
            final_score,
            study_hours
        )
        
        if error:
            return jsonify({'success': False, 'error': {'code': 'prediction_failed', 'message': error}}), 400
            
        # If student_id is provided, persist prediction
        if student_id:
            try:
                MLService.save_prediction(int(student_id), semester, result['predicted_gpa'], result.get('model'))
            except Exception as save_err:
                logger.warning(f"Failed to auto-save prediction: {save_err}")
                
        return jsonify({
            'success': True,
            'prediction': {
                'predicted_gpa': result['predicted_gpa'],
                'model_used': result.get('model', 'LinearRegression'),
                'r_squared': result.get('r2', 0.95),
                'mae': result.get('mae', 0.04),
                'rmse': result.get('rmse', 0.05),
                'performance_category': result.get('performance_category', 'Good')
            },
            'data': result
        })
    except Exception as e:
        logger.error(f"Prediction error: {e}")
        return jsonify({'success': False, 'error': {'code': 'error', 'message': str(e)}}), 500

# ==================== RISK ROUTES ====================

@app.route('/risk')
@login_required
def risk():
    try:
        risk_dist = RiskService.get_risk_distribution()
        high_risk = RiskService.get_high_risk_students(20)
        
        return render_template('risk/risk.html',
                             risk_distribution=risk_dist,
                             high_risk_students=high_risk)
    except Exception as e:
        logger.error(f"Risk page error: {e}")
        return render_template('errors/500.html', error=str(e)), 500

# ==================== API ROUTES ====================

@app.route('/api/students/list', methods=['GET'])
@login_required
def get_students_list():
    try:
        students = db.fetch_all("SELECT id, student_id, name, major, current_semester FROM students ORDER BY name ASC")
        return jsonify({'success': True, 'students': students or []})
    except Exception as e:
        logger.error(f"Get students list error: {e}")
        return jsonify({'success': False, 'error': {'code': 'error', 'message': str(e)}}), 500

@app.route('/api/predictions/history', methods=['GET'])
@login_required
def get_prediction_history():
    try:
        query = """
            SELECT pr.id, pr.student_id, s.name as student_name, s.student_id as student_code,
                   pr.semester, pr.predicted_gpa, pr.actual_gpa, pr.model_used,
                   pr.mae, pr.rmse, pr.r_squared, pr.prediction_date
            FROM prediction_results pr
            JOIN students s ON pr.student_id = s.id
            ORDER BY pr.prediction_date DESC
            LIMIT 50
        """
        predictions = db.fetch_all(query)
        clean_preds = []
        for p in (predictions or []):
            clean_preds.append({
                'id': p['id'],
                'student_id': p['student_id'],
                'student_name': p['student_name'],
                'student_code': p['student_code'],
                'semester': p['semester'],
                'predicted_gpa': float(p['predicted_gpa']) if p['predicted_gpa'] is not None else 0.0,
                'actual_gpa': float(p['actual_gpa']) if p['actual_gpa'] is not None else None,
                'model_used': p['model_used'],
                'mae': float(p['mae']) if p['mae'] is not None else 0.0,
                'rmse': float(p['rmse']) if p['rmse'] is not None else 0.0,
                'r_squared': float(p['r_squared']) if p['r_squared'] is not None else 0.0,
                'prediction_date': p['prediction_date'].strftime('%Y-%m-%d %H:%M') if p['prediction_date'] else None
            })
        return jsonify({'success': True, 'predictions': clean_preds})
    except Exception as e:
        logger.error(f"Get prediction history error: {e}")
        return jsonify({'success': False, 'error': {'code': 'error', 'message': str(e)}}), 500

@app.route('/api/analytics/summary', methods=['GET'])
@login_required
def get_analytics_summary():
    try:
        total_students = AnalyticsService.get_total_students_count()
        at_risk = AnalyticsService.get_at_risk_count()
        gpa_stats = AnalyticsService.get_gpa_statistics()
        att_stats = AnalyticsService.get_attendance_statistics()
        gpa_trend = AnalyticsService.get_gpa_trend()
        gpa_dist = AnalyticsService.get_gpa_distribution()
        gpa_by_major = AnalyticsService.get_gpa_by_major()
        gpa_by_semester = AnalyticsService.get_gpa_by_semester()
        att_vs_gpa = AnalyticsService.get_attendance_vs_gpa_data()
        study_vs_gpa = AnalyticsService.get_study_hours_vs_gpa_data()
        score_analysis = AnalyticsService.get_score_analysis()
        corr_matrix = AnalyticsService.get_correlation_matrix()
        
        return jsonify({
            'success': True,
            'analytics': {
                'total_students': total_students,
                'at_risk': at_risk,
                'gpa_stats': gpa_stats,
                'attendance_stats': att_stats,
                'gpa_trend': gpa_trend,
                'gpa_distribution': gpa_dist,
                'gpa_by_major': gpa_by_major,
                'gpa_by_semester': gpa_by_semester,
                'attendance_vs_gpa': att_vs_gpa,
                'study_hours_vs_gpa': study_vs_gpa,
                'score_analysis': score_analysis,
                'correlation_matrix': corr_matrix
            }
        })
    except Exception as e:
        logger.error(f"Analytics summary error: {e}")
        return jsonify({'success': False, 'error': {'code': 'error', 'message': str(e)}}), 500

@app.route('/api/risk/assessment', methods=['GET'])
@login_required
def get_risk_assessment_api():
    try:
        query = """
            SELECT ra.id, ra.student_id, s.student_id, s.name, s.major,
                   ra.risk_level, ra.gpa_risk, ra.attendance_risk,
                   ra.score_trend_risk, ra.study_hours_risk, ra.assessment_date
            FROM risk_assessments ra
            JOIN students s ON ra.student_id = s.id
            ORDER BY 
                CASE ra.risk_level 
                    WHEN 'HIGH' THEN 1 
                    WHEN 'MEDIUM' THEN 2 
                    WHEN 'LOW' THEN 3 
                    ELSE 4 
                END,
                ra.assessment_date DESC
        """
        records = db.fetch_all(query)
        assessments = []
        for r in (records or []):
            assessments.append({
                'id': r['id'],
                'student_id': r['student_id'],
                'name': r['name'],
                'major': r['major'],
                'risk_level': r['risk_level'],
                'gpa_risk': float(r['gpa_risk']) if r['gpa_risk'] is not None else 0.0,
                'attendance_risk': float(r['attendance_risk']) if r['attendance_risk'] is not None else 0.0,
                'score_trend_risk': float(r['score_trend_risk']) if r['score_trend_risk'] is not None else 0.0,
                'study_hours_risk': float(r['study_hours_risk']) if r['study_hours_risk'] is not None else 0.0,
                'assessment_date': r['assessment_date'].strftime('%Y-%m-%d') if r['assessment_date'] else None
            })
        return jsonify({'success': True, 'assessments': assessments})
    except Exception as e:
        logger.error(f"Risk assessment API error: {e}")
        return jsonify({'success': False, 'error': {'code': 'error', 'message': str(e)}}), 500

@app.route('/api/ml/train', methods=['POST'])
@admin_required
def train_ml():
    try:
        metadata = MLService.train_models()
        
        if metadata is None:
            return jsonify({'success': False, 'error': {'code': 'training_failed', 'message': 'Training failed'}}), 400
        
        return jsonify({'success': True, 'data': metadata})
    except Exception as e:
        logger.error(f"ML training error: {e}")
        return jsonify({'success': False, 'error': {'code': 'error', 'message': str(e)}}), 500

@app.route('/api/risk/assess-all', methods=['POST'])
@admin_required
def assess_all_risk():
    try:
        count = RiskService.assess_all_students()
        return jsonify({'success': True, 'data': {'assessed': count}})
    except Exception as e:
        logger.error(f"Risk assessment error: {e}")
        return jsonify({'success': False, 'error': {'code': 'error', 'message': str(e)}}), 500

# ==================== ERROR HANDLERS ====================

@app.errorhandler(404)
def not_found(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def internal_error(error):
    return render_template('errors/500.html', error=str(error)), 500

if __name__ == '__main__':
    import os
    debug = os.getenv('FLASK_DEBUG', 'False') == 'True'
    port = int(os.getenv('PORT', 5000))
    app.run(debug=debug, host='0.0.0.0', port=port)
