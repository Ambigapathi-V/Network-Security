from networksecurity.components.data_ingestion import DataIngestion
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import sys
from networksecurity.entity.config_entity import DataIngestionConfig
from networksecurity.entity.config_entity import TrainingPipelineConfig

if __name__ == '__main__':
    try:
        # Initialize configuration for the training pipeline and data ingestion
        trainingpipelineconfig = TrainingPipelineConfig()
        dataingestionconfig = DataIngestionConfig(trainingpipelineconfig)
        
        # Pass the DataIngestionConfig to DataIngestion
        data_ingestion = DataIngestion(data_ingestion_config=dataingestionconfig)
        
        logging.info('Initiating the data ingestion process...')
        
        # Start data ingestion and get the artifact
        dataingestionartifact = data_ingestion.initiate_data_ingestion()
        
        # Print or log the resulting artifact details
        print(dataingestionartifact)
        logging.info('Data ingestion completed successfully.')

    except Exception as e:
        raise NetworkSecurityException(e, sys)
