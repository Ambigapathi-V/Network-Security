from networksecurity.constants.training_pipeline import SAVED_MODEL_DIR,MODEL_FILE_NAME
import os
import sys
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

class NetworkModel:
    def __init__(self,preprocessor,model):
        try:
            self.preprocessor = preprocessor
            self.model = model
        except Exception as e:
            logging.error(f"Error initializing NetworkModel: {str(e)}")
            raise NetworkSecurityException(f"Error initializing NetworkModel: {str(e)}")
        
    def predict(self,x):
        try:
            x = self.preprocessor.transform(x)
            prediction = self.model.predict(x)
            return prediction
        except Exception as e:
            logging.error(f"Error predicting with NetworkModel: {str(e)}")
            raise NetworkSecurityException(f"Error predicting with NetworkModel: {str(e)}")
    