from dataclasses import dataclass

@dataclass

class DataIngestionArtifact:
    trained_file_path : str
    testing_file_path : str