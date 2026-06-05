import joblib
import pandas as pd
import numpy as np
import logging
from config import Config

logger = logging.getLogger(__name__)

class ResaleModel:
    """Handles resale price prediction"""
    
    def __init__(self):
        self.model = None
        self.model_columns = None
        self.is_loaded = False
    
    def load_model(self):
        """Load the trained model and columns"""
        try:
            self.model = joblib.load(Config.MODEL_PATH)
            self.model_columns = joblib.load(Config.MODEL_COLUMNS_PATH)
            self.is_loaded = True
            logger.info("✓ ML model loaded successfully")
            return True
        except Exception as e:
            logger.error(f"Error loading model: {str(e)}")
            raise
    
    def predict(self, features_dict):
        """
        Predict resale value
        
        Args:
            features_dict: Dictionary of features for prediction
        
        Returns:
            float: Predicted resale value
        """
        if not self.is_loaded:
            raise ValueError("Model not loaded")
        
        # Create feature vector with zeros
        row = {col: 0 for col in self.model_columns}
        
        # Update with provided features
        for key, value in features_dict.items():
            if key in row:
                row[key] = value
        
        # Make prediction
        X = pd.DataFrame([row])
        pred_log = self.model.predict(X)[0]
        resale_value = round(np.exp(pred_log) * Config.RESALE_MULTIPLIER, 2)
        
        return resale_value