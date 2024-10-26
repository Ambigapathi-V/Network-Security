from networksecurity.entity.artifact_entity import DataIngestionArtifact, DataValidationArtifact
from networksecurity.entity.config_entity import DataValidationConfig
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.constants.training_pipeline import SCHEMA_FILE_PATH
from networksecurity.utils.main_utlis.utils import read_yaml_file, write_yaml_file
from scipy.stats import ks_2samp
import pandas as pd
import os, sys

class DataValidation:
    def __init__(self, data_ingestion_artifact: DataIngestionArtifact,
                 data_validation_config: DataValidationConfig):
        try:
            # Store artifacts and config objects for data ingestion and validation
            self.data_ingestion_artifact = data_ingestion_artifact
            self.data_validation_config = data_validation_config
            self._schema_config = read_yaml_file(SCHEMA_FILE_PATH)  # Load schema configuration
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)
    
    @staticmethod
    def read_data(filepath) -> pd.DataFrame:
        """Reads a CSV file from the specified path."""
        try:
            return pd.read_csv(filepath)
        except Exception as e:
            raise NetworkSecurityException(e, sys) 
        
    def validate_number_of_columns(self, dataframe: pd.DataFrame) -> bool:
        """Validates if the number of columns in the dataframe matches the schema configuration."""
        try:
            number_of_columns = len(self._schema_config["features"])
            logging.info(f"Required number of columns: {number_of_columns}")
            logging.info(f"Dataframe has columns: {len(dataframe.columns)}")
            if len(dataframe.columns) == number_of_columns:
                logging.info("Number of columns match.")
                return True
            return False
        except Exception as e:
            raise NetworkSecurityException(e, sys)

    def validate_numerical_columns(self, dataframe: pd.DataFrame) -> bool:
        """Checks if all specified numerical columns are present in the dataframe."""
        try:
            numerical_columns = self._schema_config["numerical_columns"]
            missing_columns = [col for col in numerical_columns if col not in dataframe.columns]
            if missing_columns:
                logging.error(f"Missing numerical columns: {missing_columns}")
                return False
            logging.info("All numerical columns are present.")
            return True
        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def detect_dataset_drift(self, base_df: pd.DataFrame, current_df: pd.DataFrame, threshold=0.05) -> bool:
        """
        Checks for data drift between the base and current datasets using the KS test.
        """
        try:
            status = True
            report = {}
            for column in base_df.columns:
                d1 = base_df[column]
                d2 = current_df[column]
                is_same_dist = ks_2samp(d1, d2)
                is_found = is_same_dist.pvalue < threshold  # True if drift is detected
                if is_found:
                    status = False  # Update status if any drift is found

                report.update({column: {
                    "p_value": float(is_same_dist.pvalue),
                    "drift_status": is_found
                }})

            drift_report_file_path = self.data_validation_config.drift_report_file_path
            
            # Save drift report
            dir_path = os.path.dirname(drift_report_file_path)
            os.makedirs(dir_path, exist_ok=True)  
            write_yaml_file(file_path=drift_report_file_path, content=report)
                
            return status  # Return False if drift was detected in any feature

        except Exception as e:
            raise NetworkSecurityException(e, sys)
        
    def initiate_data_validation(self) -> DataValidationArtifact:
        """Initiates the data validation process by validating schemas, columns, and detecting drift."""
        try:
            train_file_path = self.data_ingestion_artifact.trained_file_path
            test_file_path = self.data_ingestion_artifact.testing_file_path
            
            # Step 1: Read data
            train_dataframe = self.read_data(train_file_path)
            test_dataframe = self.read_data(test_file_path)

            # Step 2: Validate number of columns in both train and test sets
            if not self.validate_number_of_columns(train_dataframe):
                raise NetworkSecurityException("Train dataframe does not contain all required columns.", sys)
            
            if not self.validate_number_of_columns(test_dataframe):
                raise NetworkSecurityException("Test dataframe does not contain all required columns.", sys)
            
            # Step 3: Validate presence of numerical columns in both train and test sets
            if not self.validate_numerical_columns(train_dataframe):
                raise NetworkSecurityException("Train dataframe does not contain all required numerical columns.", sys)

            if not self.validate_numerical_columns(test_dataframe):
                raise NetworkSecurityException("Test dataframe does not contain all required numerical columns.", sys)
            
            # Step 4: Check for data drift
            status = self.detect_dataset_drift(base_df=train_dataframe, current_df=test_dataframe)
            
            # Step 5: Save validated datasets
            os.makedirs(os.path.dirname(self.data_validation_config.valid_train_file_path), exist_ok=True)
            train_dataframe.to_csv(self.data_validation_config.valid_train_file_path, index=False, header=True)
            test_dataframe.to_csv(self.data_validation_config.valid_test_file_path, index=False, header=True)
            
            # Step 6: Prepare the DataValidationArtifact
            data_validation_artifact = DataValidationArtifact(
                validation_status=status,
                valid_train_file_path=self.data_validation_config.valid_train_file_path,
                valid_test_file_path=self.data_validation_config.valid_test_file_path,
                invalid_train_file_path=None,
                invalid_test_file_path=None,
                drift_report_file_path=self.data_validation_config.drift_report_file_path,
            )
            
            logging.info("Data validation completed successfully.")
            return data_validation_artifact
            
        except Exception as e:
            raise NetworkSecurityException(e, sys)
