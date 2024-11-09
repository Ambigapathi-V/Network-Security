from networksecurity.entity.artifact_entity import ClassificationMetricArtifact
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from sklearn.metrics import f1_score as sklearn_f1_score, precision_score as sklearn_precision_score, recall_score as sklearn_recall_score
import sys

def get_classification_score(y_true, y_pred) -> ClassificationMetricArtifact:
    """
    Calculate classification metrics and create ClassificationMetricArtifact.
    
    Parameters:
    y_true (list): Ground truth labels.
    y_pred (list): Predicted labels.
    
    Returns:
    ClassificationMetricArtifact: An object containing classification metrics.
    """
    try:
        f1 = sklearn_f1_score(y_true, y_pred)
        precision = sklearn_precision_score(y_true, y_pred)
        recall = sklearn_recall_score(y_true, y_pred)
        
        classification_metrics = ClassificationMetricArtifact(f1_score=f1, precision_score=precision, recall_score=recall)
        return classification_metrics
    except Exception as e:
        logging.error(f"An error occurred: {str(e)}")
        raise NetworkSecurityException(f"Error in get_classification_score: {str(e)}", sys)
