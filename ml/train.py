import os
import numpy as np
import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.linear_model import LinearRegression
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.metrics import mean_absolute_error, mean_squared_error, r2_score
import joblib
import logging
from database import db
from config import Config

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class MLPreprocessor:
    """Data preprocessing for ML models"""
    
    @staticmethod
    def load_training_data():
        """Load academic records for training"""
        logger.info("Loading training data from database...")
        
        query = """
            SELECT ar.gpa, ar.attendance, ar.assignment_score, 
                   ar.midterm_score, ar.final_score, ar.study_hours
            FROM academic_records ar
            WHERE ar.gpa IS NOT NULL 
            AND ar.attendance IS NOT NULL
            AND ar.assignment_score IS NOT NULL
            AND ar.midterm_score IS NOT NULL
            AND ar.final_score IS NOT NULL
            AND ar.study_hours IS NOT NULL
        """
        
        records = db.fetch_all(query)
        
        if not records:
            logger.warning("No training data found")
            return None, None
        
        df = pd.DataFrame(records)
        
        logger.info(f"Loaded {len(df)} records for training")
        
        return df
    
    @staticmethod
    def prepare_features_and_target(df):
        """Prepare features and target variable"""
        
        X = df[[
            'attendance', 'assignment_score', 'midterm_score', 
            'final_score', 'study_hours'
        ]].values
        
        y = df['gpa'].values
        
        return X, y
    
    @staticmethod
    def split_data(X, y, test_size=0.2, random_state=42):
        """Split data into train and test sets"""
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, random_state=random_state
        )
        
        scaler = StandardScaler()
        X_train_scaled = scaler.fit_transform(X_train)
        X_test_scaled = scaler.transform(X_test)
        
        return X_train_scaled, X_test_scaled, y_train, y_test, scaler


class MLTrainer:
    """Machine Learning model trainer"""
    
    def __init__(self):
        self.models_dir = os.path.join(os.path.dirname(__file__), 'models')
        os.makedirs(self.models_dir, exist_ok=True)
        self.results = {}
    
    def train_linear_regression(self, X_train, X_test, y_train, y_test):
        """Train Linear Regression model"""
        logger.info("Training Linear Regression model...")
        
        model = LinearRegression()
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        self.results['LinearRegression'] = {
            'model': model,
            'mae': mae,
            'rmse': rmse,
            'r2': r2
        }
        
        logger.info(f"Linear Regression - MAE: {mae:.4f}, RMSE: {rmse:.4f}, R²: {r2:.4f}")
        
        return model, mae, rmse, r2
    
    def train_random_forest(self, X_train, X_test, y_train, y_test):
        """Train Random Forest model"""
        logger.info("Training Random Forest model...")
        
        model = RandomForestRegressor(
            n_estimators=100,
            random_state=42,
            n_jobs=-1
        )
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        self.results['RandomForest'] = {
            'model': model,
            'mae': mae,
            'rmse': rmse,
            'r2': r2
        }
        
        logger.info(f"Random Forest - MAE: {mae:.4f}, RMSE: {rmse:.4f}, R²: {r2:.4f}")
        
        return model, mae, rmse, r2
    
    def train_gradient_boosting(self, X_train, X_test, y_train, y_test):
        """Train Gradient Boosting model"""
        logger.info("Training Gradient Boosting model...")
        
        model = GradientBoostingRegressor(
            n_estimators=100,
            random_state=42,
            learning_rate=0.1
        )
        model.fit(X_train, y_train)
        
        y_pred = model.predict(X_test)
        
        mae = mean_absolute_error(y_test, y_pred)
        rmse = np.sqrt(mean_squared_error(y_test, y_pred))
        r2 = r2_score(y_test, y_pred)
        
        self.results['GradientBoosting'] = {
            'model': model,
            'mae': mae,
            'rmse': rmse,
            'r2': r2
        }
        
        logger.info(f"Gradient Boosting - MAE: {mae:.4f}, RMSE: {rmse:.4f}, R²: {r2:.4f}")
        
        return model, mae, rmse, r2
    
    def get_best_model(self):
        """Get best model based on R² score"""
        if not self.results:
            return None
        
        best_model_name = max(
            self.results.keys(),
            key=lambda x: self.results[x]['r2']
        )
        
        best_model_data = self.results[best_model_name]
        
        logger.info(f"Best model: {best_model_name} with R²: {best_model_data['r2']:.4f}")
        
        return best_model_name, best_model_data
    
    def save_best_model(self, model_name, model_data, scaler):
        """Save best model and scaler"""
        model_path = os.path.join(self.models_dir, f'{model_name.lower()}_model.joblib')
        scaler_path = os.path.join(self.models_dir, 'scaler.joblib')
        metadata_path = os.path.join(self.models_dir, 'model_metadata.json')
        
        joblib.dump(model_data['model'], model_path)
        joblib.dump(scaler, scaler_path)
        
        import json
        metadata = {
            'model_name': model_name,
            'mae': float(model_data['mae']),
            'rmse': float(model_data['rmse']),
            'r2': float(model_data['r2'])
        }
        
        with open(metadata_path, 'w') as f:
            json.dump(metadata, f, indent=2)
        
        logger.info(f"Model saved to {model_path}")
        logger.info(f"Scaler saved to {scaler_path}")
        logger.info(f"Metadata saved to {metadata_path}")
    
    def train_all_models(self, X_train, X_test, y_train, y_test):
        """Train all models"""
        logger.info("=" * 50)
        logger.info("Starting model training...")
        logger.info("=" * 50)
        
        self.train_linear_regression(X_train, X_test, y_train, y_test)
        self.train_random_forest(X_train, X_test, y_train, y_test)
        self.train_gradient_boosting(X_train, X_test, y_train, y_test)
        
        logger.info("=" * 50)
        logger.info("Model training completed!")
        logger.info("=" * 50)


def run_training_pipeline():
    """Run complete training pipeline"""
    try:
        logger.info("Starting ML training pipeline...")
        
        df = MLPreprocessor.load_training_data()
        if df is None or len(df) < 10:
            logger.error("Insufficient training data")
            return False
        
        X, y = MLPreprocessor.prepare_features_and_target(df)
        X_train, X_test, y_train, y_test, scaler = MLPreprocessor.split_data(
            X, y,
            test_size=Config.ML_TRAIN_TEST_SPLIT,
            random_state=Config.ML_RANDOM_STATE
        )
        
        trainer = MLTrainer()
        trainer.train_all_models(X_train, X_test, y_train, y_test)
        
        best_model_name, best_model_data = trainer.get_best_model()
        trainer.save_best_model(best_model_name, best_model_data, scaler)
        
        logger.info("ML training pipeline completed successfully!")
        return True
        
    except Exception as e:
        logger.error(f"Training pipeline error: {e}")
        import traceback
        traceback.print_exc()
        return False


if __name__ == '__main__':
    run_training_pipeline()
