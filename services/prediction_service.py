import pandas as pd
import numpy as np
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.model_selection import train_test_split
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import os
import json
from database import db
from config import Config
import logging

logger = logging.getLogger(__name__)

class MLService:
    """Machine Learning service for GPA prediction"""
    
    MODEL_DIR = 'ml/models'
    
    @staticmethod
    def prepare_training_data():
        """Prepare data for model training"""
        try:
            records = db.fetch_all("""
                SELECT semester, attendance, assignment_score, midterm_score,
                       final_score, study_hours, gpa
                FROM academic_records
                WHERE gpa IS NOT NULL
                AND attendance IS NOT NULL
                AND assignment_score IS NOT NULL
                AND midterm_score IS NOT NULL
                AND final_score IS NOT NULL
                AND study_hours IS NOT NULL
            """)
            
            if len(records) < 10:
                logger.warning(f"Insufficient data for training: {len(records)} records")
                return None, None
            
            df = pd.DataFrame(records)
            
            X = df[['semester', 'attendance', 'assignment_score', 'midterm_score', 
                   'final_score', 'study_hours']]
            y = df['gpa']
            
            return X, y
        except Exception as e:
            logger.error(f"Prepare training data error: {e}")
            return None, None
    
    @staticmethod
    def train_models():
        """Train multiple models and compare performance"""
        try:
            X, y = MLService.prepare_training_data()
            
            if X is None or y is None:
                return None
            
            # Split data
            X_train, X_test, y_train, y_test = train_test_split(
                X, y, test_size=Config.ML_TRAIN_TEST_SPLIT, 
                random_state=Config.ML_RANDOM_STATE
            )
            
            models = {
                'LinearRegression': LinearRegression(),
                'RandomForestRegressor': RandomForestRegressor(
                    n_estimators=100, 
                    random_state=Config.ML_RANDOM_STATE
                ),
                'GradientBoostingRegressor': GradientBoostingRegressor(
                    n_estimators=100,
                    random_state=Config.ML_RANDOM_STATE
                )
            }
            
            results = {}
            
            for name, model in models.items():
                try:
                    # Train
                    model.fit(X_train, y_train)
                    
                    # Predict
                    y_pred = model.predict(X_test)
                    
                    # Evaluate
                    mae = mean_absolute_error(y_test, y_pred)
                    rmse = np.sqrt(mean_squared_error(y_test, y_pred))
                    r2 = r2_score(y_test, y_pred)
                    
                    results[name] = {
                        'mae': float(mae),
                        'rmse': float(rmse),
                        'r2': float(r2),
                        'model': model
                    }
                    
                    logger.info(f"{name}: MAE={mae:.4f}, RMSE={rmse:.4f}, R2={r2:.4f}")
                except Exception as e:
                    logger.error(f"Error training {name}: {e}")
                    continue
            
            if not results:
                return None
            
            # Find best model
            best_model_name = max(results, key=lambda x: results[x]['r2'])
            best_model_data = results[best_model_name]
            
            # Save best model
            os.makedirs(MLService.MODEL_DIR, exist_ok=True)
            model_path = os.path.join(MLService.MODEL_DIR, 'best_model.joblib')
            joblib.dump(best_model_data['model'], model_path)
            
            # Save metadata
            metadata = {
                'best_model': best_model_name,
                'mae': best_model_data['mae'],
                'rmse': best_model_data['rmse'],
                'r2': best_model_data['r2'],
                'training_samples': len(X_train),
                'test_samples': len(X_test),
                'features': X.columns.tolist(),
                'all_results': {k: {
                    'mae': v['mae'],
                    'rmse': v['rmse'],
                    'r2': v['r2']
                } for k, v in results.items()}
            }
            
            metadata_path = os.path.join(MLService.MODEL_DIR, 'metadata.json')
            with open(metadata_path, 'w') as f:
                json.dump(metadata, f, indent=2)
            
            logger.info(f"Best model: {best_model_name}")
            logger.info(f"Model saved to {model_path}")
            
            return metadata
        except Exception as e:
            logger.error(f"Train models error: {e}")
            return None
    
    @staticmethod
    def load_best_model():
        """Load best trained model"""
        try:
            model_path = os.path.join(MLService.MODEL_DIR, 'best_model.joblib')
            
            if not os.path.exists(model_path):
                logger.warning("No trained model found")
                return None
            
            model = joblib.load(model_path)
            return model
        except Exception as e:
            logger.error(f"Load model error: {e}")
            return None
    
    @staticmethod
    def get_model_metadata():
        """Get model metadata"""
        try:
            metadata_path = os.path.join(MLService.MODEL_DIR, 'metadata.json')
            
            if not os.path.exists(metadata_path):
                return None
            
            with open(metadata_path, 'r') as f:
                metadata = json.load(f)
            
            return metadata
        except Exception as e:
            logger.error(f"Get metadata error: {e}")
            return None
    
    @staticmethod
    def predict_gpa(semester, attendance, assignment_score, midterm_score, 
                   final_score, study_hours):
        """Predict GPA for given inputs"""
        try:
            model = MLService.load_best_model()
            metadata = MLService.get_model_metadata()
            
            if model is None or metadata is None:
                return None, "Model not trained yet"
            
            # Validate inputs
            if not (0 <= attendance <= 100):
                return None, "Attendance must be between 0 and 100"
            if not (0 <= assignment_score <= 100):
                return None, "Assignment score must be between 0 and 100"
            if not (0 <= midterm_score <= 100):
                return None, "Midterm score must be between 0 and 100"
            if not (0 <= final_score <= 100):
                return None, "Final score must be between 0 and 100"
            if study_hours < 0:
                return None, "Study hours cannot be negative"
            if semester < 1:
                return None, "Semester must be >= 1"
            
            # Prepare input
            X = np.array([[semester, attendance, assignment_score, midterm_score, 
                          final_score, study_hours]])
            
            # Predict
            predicted_gpa = model.predict(X)[0]
            
            # Clamp to valid range
            predicted_gpa = max(0, min(4, predicted_gpa))
            
            return {
                'predicted_gpa': float(predicted_gpa),
                'performance_category': MLService._get_performance_category(predicted_gpa),
                'model': metadata['best_model'],
                'mae': metadata['mae'],
                'rmse': metadata['rmse'],
                'r2': metadata['r2']
            }, None
        except Exception as e:
            logger.error(f"Predict GPA error: {e}")
            return None, str(e)
    
    @staticmethod
    def _get_performance_category(gpa):
        """Get performance category based on GPA"""
        if gpa >= 3.5:
            return 'Excellent'
        elif gpa >= 3.0:
            return 'Good'
        elif gpa >= 2.5:
            return 'Average'
        else:
            return 'Poor'
    
    @staticmethod
    def save_prediction(student_id, semester, predicted_gpa, model_name=None):
        """Save prediction result to database"""
        try:
            metadata = MLService.get_model_metadata()
            
            if metadata is None:
                return False
            
            query = """
                INSERT INTO prediction_results
                (student_id, semester, predicted_gpa, model_used, 
                 mae, rmse, r_squared)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            db.execute_query(query, (
                student_id,
                semester,
                predicted_gpa,
                model_name or metadata['best_model'],
                metadata['mae'],
                metadata['rmse'],
                metadata['r2']
            ))
            
            return True
        except Exception as e:
            logger.error(f"Save prediction error: {e}")
            return False
    
    @staticmethod
    def get_prediction_history(student_id, limit=10):
        """Get prediction history for a student"""
        try:
            query = """
                SELECT id, student_id, semester, predicted_gpa, actual_gpa,
                       model_used, mae, rmse, r_squared, prediction_date
                FROM prediction_results
                WHERE student_id = %s
                ORDER BY prediction_date DESC
                LIMIT %s
            """
            results = db.fetch_all(query, (student_id, limit))
            return results
        except Exception as e:
            logger.error(f"Get prediction history error: {e}")
            return []
