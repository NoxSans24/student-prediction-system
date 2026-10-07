import os
import json
import joblib
import numpy as np
import logging
from database import db

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MLPredictor:
    """Make predictions using trained models"""
    
    def __init__(self):
        self.models_dir = os.path.join(os.path.dirname(__file__), 'models')
        self.model = None
        self.scaler = None
        self.metadata = None
        self.load_model()
    
    def load_model(self):
        """Load trained model and scaler"""
        try:
            metadata_path = os.path.join(self.models_dir, 'model_metadata.json')
            
            if not os.path.exists(metadata_path):
                logger.warning("Model metadata not found. Train models first.")
                return False
            
            with open(metadata_path, 'r') as f:
                self.metadata = json.load(f)
            
            model_name = self.metadata['model_name'].lower()
            model_path = os.path.join(self.models_dir, f'{model_name}_model.joblib')
            scaler_path = os.path.join(self.models_dir, 'scaler.joblib')
            
            self.model = joblib.load(model_path)
            self.scaler = joblib.load(scaler_path)
            
            logger.info(f"Loaded model: {self.metadata['model_name']}")
            return True
            
        except Exception as e:
            logger.error(f"Error loading model: {e}")
            return False
    
    def is_model_available(self):
        """Check if model is available"""
        return self.model is not None and self.scaler is not None
    
    def predict(self, attendance, assignment_score, midterm_score, final_score, study_hours):
        """Make prediction for given features"""
        
        if not self.is_model_available():
            logger.error("Model not available")
            return None
        
        try:
            features = np.array([[
                attendance,
                assignment_score,
                midterm_score,
                final_score,
                study_hours
            ]])
            
            features_scaled = self.scaler.transform(features)
            predicted_gpa = self.model.predict(features_scaled)[0]
            
            predicted_gpa = float(np.clip(predicted_gpa, 0, 4.0))
            
            result = {
                'predicted_gpa': predicted_gpa,
                'model_used': self.metadata['model_name'],
                'mae': self.metadata['mae'],
                'rmse': self.metadata['rmse'],
                'r_squared': self.metadata['r2']
            }
            
            logger.info(f"Prediction made: {predicted_gpa:.2f}")
            return result
            
        except Exception as e:
            logger.error(f"Prediction error: {e}")
            return None
    
    def predict_and_save(self, student_id, semester, attendance, assignment_score, 
                         midterm_score, final_score, study_hours):
        """Make prediction and save to database"""
        
        prediction = self.predict(
            attendance, assignment_score, midterm_score, final_score, study_hours
        )
        
        if prediction is None:
            return False
        
        try:
            query = """
                INSERT INTO prediction_results 
                (student_id, semester, predicted_gpa, model_used, mae, rmse, r_squared)
                VALUES (%s, %s, %s, %s, %s, %s, %s)
            """
            
            db.execute_query(query, (
                student_id,
                semester,
                prediction['predicted_gpa'],
                prediction['model_used'],
                prediction['mae'],
                prediction['rmse'],
                prediction['r_squared']
            ))
            
            logger.info(f"Prediction saved for student {student_id}")
            return True
            
        except Exception as e:
            logger.error(f"Error saving prediction: {e}")
            return False
    
    def get_model_info(self):
        """Get model information"""
        if not self.is_model_available():
            return None
        
        return {
            'model_name': self.metadata['model_name'],
            'mae': self.metadata['mae'],
            'rmse': self.metadata['rmse'],
            'r_squared': self.metadata['r2']
        }


predictor = MLPredictor()

def predict_gpa(attendance, assignment_score, midterm_score, final_score, study_hours):
    """Predict GPA for given features"""
    return predictor.predict(
        attendance, assignment_score, midterm_score, final_score, study_hours
    )

def save_prediction(student_id, semester, attendance, assignment_score,
                    midterm_score, final_score, study_hours):
    """Predict and save to database"""
    return predictor.predict_and_save(
        student_id, semester, attendance, assignment_score,
        midterm_score, final_score, study_hours
    )

def get_model_info():
    """Get current model information"""
    return predictor.get_model_info()

def is_model_ready():
    """Check if model is ready for predictions"""
    return predictor.is_model_available()
