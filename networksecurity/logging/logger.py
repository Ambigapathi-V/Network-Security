import logging
import os
from datetime import datetime

# Set up logging
LOG_FILE = f"{datetime.now().strftime('%m_%d_%Y_%H_%M_%S')}.log"
log_dir = os.path.join(os.getcwd(), "logs")

# Create the directory if it doesn't exist
os.makedirs(log_dir, exist_ok=True)

LOG_FILE_PATH = os.path.join(log_dir, LOG_FILE)

logging.basicConfig(
    level=logging.INFO,
    format='[ %(asctime)s ] %(lineno)s %(name)s - %(levelname)s %(message)s',
    filename=LOG_FILE_PATH
)
