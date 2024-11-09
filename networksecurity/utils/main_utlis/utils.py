import yaml
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
import os, sys
import numpy as np
# import dill
import pickle
from sklearn.model_selection import GridSearchCV
from sklearn.metrics import r2_score

def read_yaml_file(file_path: str) -> dict:
    try:
        with open(file_path, 'rb') as yaml_file:  # Changed 'rb' to 'r'
            return yaml.safe_load(yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def write_yaml_file(file_path: str, content: object, replace: bool = False) -> None:
    try:
        if replace and os.path.exists(file_path):  # Fixed typo in if statement
            os.remove(file_path)
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'w') as yaml_file:
            yaml.dump(content, yaml_file)
    except Exception as e:
        raise NetworkSecurityException(e, sys)
    
def save_numpy_array_data(file_path:str, array: np.ndarray) :
    '''
    Save numpy array to file
    
    File_path: Str location where the numpy array needs to be saved
    array: Numpy array to be saved
        
    '''
    try:
        dir_path = os.path.dirname(file_path)
        os.makedirs(dir_path, exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            np.save(file_obj, array)
    
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
def save_object(file_path:str , obj : object)->None:
    '''
    Save object to file
    
    File_path: Str location where the object needs to be saved
    obj: Object to be saved
        
    '''
    try:
        logging.info(f'Saving object to {file_path}')
        os.makedirs(os.path.dirname(file_path), exist_ok=True)
        with open(file_path, 'wb') as file_obj:
            pickle.dump(obj, file_obj)
        logging.info(f'Object saved to {file_path}')
    
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
def load_object(file_path:str) -> object:
    '''
    Load object from file
    
    file_path: Str location where the object needs to be loaded
    
    Returns
    Object loaded from file
    
    '''
    try:
        logging.info(f'Loading object from {file_path}')
        if not os.path.exists(file_path):
            raise FileNotFoundError(f'File {file_path} does not exist')
        with open(file_path, 'rb') as file_obj:
            print(file_obj)
            return pickle.load(file_obj)
    
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
    
def load_numpy_array_data(file_path:str) -> np.ndarray:
    '''
    Load numpy array from file
    
    file_path: Str location where the numpy array needs to be loaded
    
    Returns
    Numpy array loaded from file
    
    '''
    try:
        logging.info(f'Loading numpy array from {file_path}')
        with open(file_path, 'rb') as file_obj:
            return np.load(file_obj)
    
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e
def evaluate_models(X_train, y_train,X_test,y_test,models,param):
    try:
        report = {}

        for i in range(len(list(models))):
            model = list(models.values())[i]
            para=param[list(models.keys())[i]]

            gs = GridSearchCV(model,para,cv=3)
            gs.fit(X_train,y_train)

            model.set_params(**gs.best_params_)
            model.fit(X_train,y_train)

            #model.fit(X_train, y_train)  # Train model

            y_train_pred = model.predict(X_train)

            y_test_pred = model.predict(X_test)

            train_model_score = r2_score(y_train, y_train_pred)

            test_model_score = r2_score(y_test, y_test_pred)

            report[list(models.keys())[i]] = test_model_score

        return report
    
    except Exception as e:
        raise NetworkSecurityException(e, sys) from e