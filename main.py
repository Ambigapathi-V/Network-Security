from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.components.data_validation import DataValidation
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys
from networksecurity.entity.config_entity import DataIngestionConfig, DataValidationConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

if __name__ == '__main__':
    try:
        # Step 1: Initialize Configuration for the Training Pipeline
        logging.info("Initializing training pipeline configuration...")
        training_pipeline_config = TrainingPipelineConfig()
        
        # Step 2: Configure Data Ingestion
        logging.info("Initializing data ingestion configuration...")
        data_ingestion_config = DataIngestionConfig(training_pipeline_config)
        data_ingestion = DataIngestion(data_ingestion_config=data_ingestion_config)
        
        # Step 3: Start Data Ingestion Process
        logging.info("Starting the data ingestion process...")
        data_ingestion_artifact = data_ingestion.initiate_data_ingestion()
        logging.info("Data ingestion completed successfully.")
        
        # Step 4: Configure Data Validation
        logging.info("Initializing data validation configuration...")
        data_validation_config = DataValidationConfig(training_pipeline_config)
        data_validation = DataValidation(data_ingestion_artifact, data_validation_config)
        
        # Step 5: Start Data Validation Process
        logging.info("Starting the data validation process...")
        data_validation_artifact = data_validation.initiate_data_validation()
        logging.info("Data validation completed successfully.")
        
        # Step 6: Log Artifacts for Verification
        logging.info(f"Data Ingestion Artifact: {data_ingestion_artifact}")
        logging.info(f"Data Validation Artifact: {data_validation_artifact}")
        
        # Step 7: Print Artifact Details for Immediate Review
        print("Data Ingestion Artifact:", data_ingestion_artifact)
        print("Data Validation Artifact:", data_validation_artifact)

    except Exception as e:
        logging.error(f"An error occurred in the main pipeline: {e}")
        raise NetworkSecurityException(e, sys)
