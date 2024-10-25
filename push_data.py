import os
import json
import sys
import certifi
import pandas as pd
import pymongo
from dotenv import load_dotenv
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging

# Load environment variables from a .env file
load_dotenv()

# Retrieve the MongoDB URL from the environment variable
MONGO_DB_URL = os.getenv('MONGO_DB_URL')
if not MONGO_DB_URL:
    raise ValueError("MongoDB URL not found in environment variables.")

class NetworkDataExtract:
    def __init__(self):
        """Initialize the MongoDB client."""
        try:
            self.mongo_client = pymongo.MongoClient(MONGO_DB_URL, tlsCAFile=certifi.where())
            logging.info("Connected to MongoDB successfully.")
        except Exception as e:
            logging.error(f"Failed to connect to MongoDB: {str(e)}")
            raise NetworkSecurityException(f"Failed to connect to MongoDB: {str(e)}", sys)

    def cv_to_json_convertor(self, file_path):
        """Convert a CSV file to a list of JSON records."""
        try:
            if not os.path.isfile(file_path):
                raise FileNotFoundError(f"The file {file_path} does not exist.")
                
            data = pd.read_csv(file_path)
            data.reset_index(drop=True, inplace=True)
            records = list(json.loads(data.T.to_json()).values())
            logging.info(f"Converted CSV to JSON with {len(records)} records.")
            return records
        except Exception as e:
            logging.error(f"Error converting CSV to JSON: {str(e)}")
            raise NetworkSecurityException(f"Error converting CSV to JSON: {str(e)}", sys)

    def insert_data_mongodb(self, records, database, collection):
        """Insert records into a specified MongoDB collection."""
        try:
            db = self.mongo_client[database]  # Access the specified database
            coll = db[collection]  # Access the specified collection
            result = coll.insert_many(records)  # Insert records into the collection
            logging.info(f"Inserted {len(records)} records into the MongoDB collection: {collection}.")
            return len(records), result.inserted_ids  # Return the number of records inserted and their IDs
        except Exception as e:
            logging.error(f"Error inserting records into MongoDB: {str(e)}")
            raise NetworkSecurityException(f"Error inserting records into MongoDB: {str(e)}", sys)

    def close_connection(self):
        """Close the MongoDB client connection."""
        self.mongo_client.close()
        logging.info("MongoDB connection closed.")

if __name__ == '__main__':
    # Define file path, database name, and collection name
    FILE_PATH = "Network_Data/phisingData.csv"   # Make sure this path is correct
    DATABASE = "KAVINAI"
    COLLECTION = 'NetworkData'  # Changed to uppercase for consistency

    # Create an instance of the NetworkDataExtract class
    try:
        network_data_extractor = NetworkDataExtract()

        # Convert CSV to JSON records
        records = network_data_extractor.cv_to_json_convertor(FILE_PATH)

        # Print the results
        print(records)

        # Insert records into MongoDB and get the number of records inserted
        num_of_records, inserted_ids = network_data_extractor.insert_data_mongodb(records, DATABASE, COLLECTION)

        # Print the number of records inserted
        print(f'Inserted {num_of_records} records into the MongoDB collection: {COLLECTION}.')
        print(f'Inserted IDs: {inserted_ids}')
    
    except NetworkSecurityException as nse:
        print(f"NetworkSecurityException: {nse}")
    except Exception as e:
        print(f"An unexpected error occurred: {str(e)}")
    finally:
        # Close the MongoDB connection
        network_data_extractor.close_connection()
