
![](https://github.com/Ambigapathi-V/Network-Security/blob/main/img/pexels-pixabay-60504.jpg)

# Network Security Prediction
![GitHub release (latest by date including pre-releases)](https://img.shields.io/github/v/release/Ambigapathi-V/Network-Security?include_prereleases)
![GitHub last commit](https://img.shields.io/github/last-commit/Ambigapathi-V/Network-Security)
![GitHub pull requests](https://img.shields.io/github/issues-pr/Ambigapathi-V/Network-Security)
![GitHub](https://img.shields.io/github/license/Ambigapathi-V/Network-Security)
![contributors](https://img.shields.io/github/contributors/Ambigapathi-V/Network-Security)
![codesize](https://img.shields.io/github/languages/code-size/Ambigapathi-V/Network-Security)


The Network-Security-Prediction project leverages machine learning to predict potential security threats in network traffic. By analyzing network data, the system classifies whether the traffic is normal or potentially malicious, offering valuable insights for organizations looking to safeguard their networks. It uses data preprocessing techniques and a trained model to make predictions based on incoming network traffic data.

This project is designed for cybersecurity professionals, network administrators, and organizations seeking automated solutions to identify and mitigate network security threats before they escalate. It helps in real-time monitoring of network traffic, making it easier to detect abnormal patterns that could indicate cyber-attacks

## Badges


[![MIT License](https://img.shields.io/badge/License-MIT-green.svg)](https://choosealicense.com/licenses/mit/)
[![Build Status](https://img.shields.io/github/workflow/status/yourusername/your-repository-name/CI)](https://github.com/Ambigapathi-V/Network-Security/issues)
[![Python Version](https://img.shields.io/pypi/pyversions/your-project-name)](https://pypi.org/project/your-project-name/)


## Features

- **CSV File Upload**: Users can upload CSV files for prediction.
- **Prediction Results**: Displays the results of predictions on uploaded data.
- **MongoDB Integration**: Optionally stores prediction results in a MongoDB database.
- **Web Interface**: Simple, user-friendly web interface to interact with the model.
- **Real-Time Prediction**: Uses pre-trained model to make real-time predictions.
- **Error Handling**: Handles common file errors and prediction failures gracefully.
- **Model Retraining**: Allows for periodic retraining of the model with updated data.
- **Cross-platform Support**: Accessible on any platform with a modern web browser.
- **Light/Dark Mode Toggle**: Users can switch between light and dark mode for the web interface.
## Demo

Since this project is API-based, the demo showcases how to interact with the API using tools like **Postman** or **cURL** for sending requests and receiving predictions.

1. **Uploading a CSV File for Prediction**:
   - Use the `POST /predict` API endpoint to upload a CSV file containing network data.
   - The response will include predictions for each data entry.

2. **Retrieving Predictions**:
   - Example API response: 
     ```json
     {
       "predictions": [1, 0, 1, 1, 0],
       "status": "success",
       "message": "Predictions completed successfully."
     }
     ```

3. **Storing Prediction Results**:
   - The results can be stored in **MongoDB** (optional), which can be viewed or accessed via MongoDB clients.

### Example Demo Using cURL

You can run the following command to test the API:
```bash
curl -X 'POST' \
  'http://localhost:8000/predict' \
  -F 'file=@yourfile.csv' 
  ```
## Screenshots

![App Screenshot](https://github.com/Ambigapathi-V/Network-Security/blob/main/img/image.png)


## Codes and Resources Used
- **Editor Used:** Visual Studio Code
- **Python Version :**  3.10

## Python packages Used
- **FastAPI:** FastAPI is a modern, fast (high-performance), web framework for building
- **Scikit-learn :** scikit-learn is a machine learning library for Python that provides a wide range of algorithms for classification
- **Pandas:** The pandas library provides data structures and functions to efficiently handle structured data, including

- **PyMongo:** PyMongo is a Python driver for MongoDB. It allows Python developers to work with MongoDB using Python.
- **Uvicorn:** Uvicorn is a lightning-fast ASGI server. It is the
- **MongoDB:** MongoDB is a NoSQL database that stores data in JSON-like documents.


## Data

The data used for traing model was collected udemy Complete machine learning course Krish nailk course.

## Source Data
- **Source:**  udemy Complete machine learning course Krish nailk course (https://www.udemy.com/course/machine-learning-and-data-science-with-python/)
- **Data Type:** CSV
- **Data Size:** 11000 records
- **Data Description:** The data contains information about students, including their age, gender, performance etc.

## Data Ingestion
- **Data Ingestion Method:** Get the data from the MongoDB database and load it into a Pandas DataFrame.
- **Data Drift** : The data drift is handled by using the concept of data normalization and feature scaling.

## Data Preprocessing


  - **Handling Missing Values:** Fill missing values with the mean of the column.
  - **Handling Categorical Variables:** Convert categorical variables into numerical format using one-hot encoding or label encoding.
  - **Scaling /Normalizing Features:** Scale/normalize features using StandardScaler or MinMaxScaler.
  - **Splitting Data:** Split the data into training and testing sets.

## Code Structure
  ```bash
  ├── main.py
  ├── setup.py
  ├── app.py.py
  ├── networksecurity
  │   ├── cloud
  │   ├── constants
  │   ├── entity
  │   ├── logging
  │   ├── utils
  │   ├── exception
  │   ├── config
  │   ├── components
  │   │   ├── data_ingestion.py
  │   │   ├── data_transformation.py
  │   │   ├── data_validation.py
  │   │   ├── model_training.py
  │   ├── Pipeline
  │   │   ├── data_ingestion_pipeline.py
  │   │   ├── data_transformation_pipeline.py
  │   │   ├── data_validation_pipeline.py
  │   │   ├── model_training_pipeline.py
  ```
## Result and Evaluation
- **Model Evaluation Metrics:** Accuracy, Precision, Recall, F1-score, AUC-ROC, refer dagshub hub for more details.
link to dagshub - https://dagshub.com/Ambigapathi-V/Network-Security

## Training the Model
### Making a Prediction Request

To make a prediction using the API, follow this example:

1. **Upload a CSV File for Prediction**

   Use the `/predict` endpoint to upload a CSV file and receive predictions.

   ```python
   import requests

   # Replace with the correct URL if running on a different server
   url = "http://localhost:8000/predict"

   # Upload your CSV file for prediction
   with open("path_to_your_file.csv", "rb") as file:
       response = requests.post(url, files={"file": file})

   # Display the response
   if response.status_code == 200:
       print("Prediction Results:", response.json())
   else:
       print("Prediction failed:", response.text)
    ```

2 .**Training the Model**

Use the /train endpoint to start the training pipeline.
## Environment Variables

Set Up Environment Variables Create a .env file to add your MongoDB URL and other environment variables:

    MONGO_DB_URL=your_mongo_db_url
## API Reference

#### Train Model

```http
  GET /train
```

| Parameter | Type     | Description                |
| :-------- | :------- | :------------------------- |
| `None` | `N/A` |  This endpoint does not require any parameters. |

#### Get item

```http
  POST /predict
```

| Parameter | Type     | Description                       |
| :-------- | :------- | :-------------------------------- |
| `file`      | `UploadFile` | **Required**. A CSV file containing data for which predictions are needed. Ensure the file matches the model's expected input columns. |




## License

[MIT](https://choosealicense.com/licenses/mit/)


## Authors

- [@Ambigapathi-V](https://github.com/Ambigapathi-V)


## Contributing

Contributions are always welcome!

If you'd like to contribute to the Network Security Prediction API project, please follow these steps:

1. Fork the repository.
2. Create a new branch for your feature or bugfix:

   ```bash
   git checkout -b feature-name

3. Commit your changes:


   ```bash
    git commit -am 'Add new feature'


4. Push to the branch:

   ``` bash 
    git push origin feature-name


## Feedback

If you have any feedback, please reach out to us at ambigapathikavin@gmail.com

