import sys
from networksecurity.logging import logger

class NetworkSecurityException(Exception):
    """Custom exception class to capture file name and line number of errors."""
    
    def __init__(self, message: str, error_details: sys):
        """
        Initializes NetworkSecurityException with the error message and details.
        
        Args:
            message (str): Description of the error.
            error_details (sys): System module to extract exception traceback info.
        """
        super().__init__(message)  # Pass message to the base Exception class
        self.message = message
        
        # Extract traceback details
        _, _, traceback = error_details.exc_info()
        self.line_number = traceback.tb_lineno
        self.file_name = traceback.tb_frame.f_code.co_filename
        
    def __str__(self):
        """
        Returns a formatted error message with file name, line number, and error details.
        """
        return (
            f"Error occurred in script: [{self.file_name}] "
            f"at line number: [{self.line_number}] "
            f"with message: [{self.message}]"
        )
