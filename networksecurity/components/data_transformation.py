import sys
import os
import numpy as np
import pandas as pd
from sklearn.impute import KNNImputer
from sklearn.pipeline import Pipeline

from networksecurity.constants.training_pipeline import TARGET_COLUMN
from networksecurity.constants.training_pipeline import DATA_TRANSFORMATION_IMPUTER_PARAMS
from networksecurity.entity.artifact_entity import (
    DataTransformationArtifact,
    DataValidationArtifact
)
from networksecurity.entity.config_entity import DataTransformationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.utils.main_utlis.utils import save_numpy_array_data,save_object
 
class DataTransformation:
    def __init__(self, data_validation_artifact: DataValidationArtifact,
                 data_transformation_config: DataTransformationConfig):
        try:
            self.data_validation_artifact = data_validation_artifact
            self.data_transformation_config = data_transformation_config
            
        except Exception as e:
            logging.error(f"Error initializing DataTransformation: {e}")
            raise NetworkSecurityException(f"Error initializing DataTransformation: {e}")
    
    @staticmethod
    def read_data( file_path: str) -> pd.DataFrame:
        try:
            logging.info(f"Loading data from: {file_path}")
            data = pd.read_csv(file_path)
            return data
            
        except Exception as e:
            logging.error(f"Error loading data: {e}")
            raise NetworkSecurityException(f"Error loading data: {e}")
        
    def get_data_transformer_object(cls)->Pipeline:
        """
        It creates and returns a pipeline object for data transformation.
        The pipeline includes the following steps:
        1. KNNImputer: Imputes missing values using k-nearest neighbors.
        
        Args:
         Cls : DataTransformation class instance.

        Returns:
            A pipeline object for data transformation.
        """
        logging.info("Creating data transformation pipeline...")
        try: 
            imputer:KNNImputer = KNNImputer(**DATA_TRANSFORMATION_IMPUTER_PARAMS)
            logging.info("Data transformation pipeline created successfully.")
            processor = Pipeline([('imputer', imputer)]) # Adding the imputer step to the pipeline.])
            return processor # Returning the created pipeline object.
        except Exception as e:
            logging.error(f"Error creating data transformation pipeline: {e}")
            raise NetworkSecurityException(f"Error creating data transformation pipeline: {e}")
    def initiate_data_transformation(self) -> DataTransformationArtifact:
        logging.info("Initiating data transformation...")
        try:
            train_df = DataTransformation.read_data(self.data_validation_artifact.valid_train_file_path)
            test_df = DataTransformation.read_data(self.data_validation_artifact.valid_test_file_path)
            
            
            ## Training DataFrame
            input_feature_train_df = train_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_train_df = train_df[TARGET_COLUMN]
            target_feature_train_df = target_feature_train_df.replace(-1,0)
            
            ## Test DataFrame
            input_feature_test_df = test_df.drop(columns=[TARGET_COLUMN], axis=1)
            target_feature_test_df = test_df[TARGET_COLUMN]
            target_feature_test_df = target_feature_test_df.replace(-1,0)
            
            
            preprocessor = self.get_data_transformer_object()
            
            preprocessor_object = preprocessor.fit(input_feature_train_df)
            
            transformed_input_train_feature = preprocessor_object.transform(input_feature_train_df)
            transformed_input_test_feature = preprocessor_object.transform(input_feature_test_df)
            
            train_arr = np.c_[transformed_input_train_feature, np.array(target_feature_train_df)]
            test_arr = np.c_[transformed_input_test_feature, np.array(target_feature_test_df)]
            
            #save the numpy arrays
            save_numpy_array_data(self.data_transformation_config.transformed_train_file_path, array = train_arr,)
            save_numpy_array_data(self.data_transformation_config.transformed_test_file_path, array = test_arr,)
            save_object(self.data_transformation_config.transformed_object_file_path, preprocessor_object)

            save_object("final_model/preprocessor.pkl", preprocessor_object)
            #preprare artifacts
            
            data_transformation_artifacts = DataTransformationArtifact(
                transformed_train_file_path=self.data_transformation_config.transformed_train_file_path,
                transformed_test_file_path=self.data_transformation_config.transformed_test_file_path,
                transformed_object_file_path=self.data_transformation_config.transformed_object_file_path
            )
            return data_transformation_artifacts # Returning the created data transformation artifacts.
            
        except Exception as e:
   
            raise NetworkSecurityException(e,sys)