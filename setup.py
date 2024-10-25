from setuptools import find_namespace_packages, setup
from typing import List

def get_requirements() -> List[str]:
    """
    This function reads the requirements.txt file and returns a list of dependencies.
    """
    requirements = []
    try:
        with open("requirements.txt", "r") as file:
            # Read the requirements.txt file
            lines = file.readlines()
            # Process each line
            for line in lines:
                requirement = line.strip()
                # Ignore empty lines and -e .
                if requirement and requirement != "-e .":
                    requirements.append(requirement)
    except FileNotFoundError:
        print("requirements.txt file not found.")
    
    return requirements

setup(
    name="NetworkSecurity",
    version="0.0.1",
    author="Ambigapathi",
    author_email="ambigapathikavin2@.com",
    packages=find_namespace_packages(),
    install_requires=get_requirements(),
    
)