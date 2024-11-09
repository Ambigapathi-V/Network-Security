from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.components.data_transformation import DataTransformation
from networksecurity.components.model_trainer import ModelTrainer
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys
from networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig, DataTransformationConfig,ModelTrainerConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

if __name__ == '__main__':
    try:
        logging.info("Starting the training pipeline execution...")

        # Initialize configurations
        training_pipeline_config = TrainingPipelineConfig()
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        
        # Data ingestion
        data_ingestion = DataIngestion(data_ingestion_config)
        logging.info("Data ingestion started")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data ingestion completed")
        print(f"Data Ingestion Artifact: {data_ingestion_artifact}")

        # Data validation
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        logging.info("Data validation started")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data validation completed")
        print(f"Data Validation Artifact: {data_validation_artifact}")

        # Data transformation
        logging.info("Data transformation started")
        data_transformation_config = DataTransformationConfig(training_pipeline_config)
        data_transformation = DataTransformation(data_validation_artifact, data_transformation_config)
        data_transformation_artifact = data_transformation.initiate_data_transformation()
        logging.info("Data transformation completed")
        print(f"Data Transformation Artifact: {data_transformation_artifact}")
        
        # Model training
        model_trainer_config = ModelTrainerConfig(training_pipeline_config)
        model_trainer = ModelTrainer(data_transformation_artifact=data_transformation_artifact, model_trainer_config=model_trainer_config)
        logging.info("Model training started")
        model_artifact = model_trainer.initiate_model_trainer()
        logging.info("Model training completed")
        print(f"Model Artifact: {model_artifact}")

    except Exception as e:
        logging.error(f"Error occurred during the pipeline execution: {e}")
        raise NetworkSecurityException(str(e), sys)
