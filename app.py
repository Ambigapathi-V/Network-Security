from fastapi import FastAPI, File, UploadFile, Request, Response
from fastapi.responses import RedirectResponse
from fastapi.templating import Jinja2Templates
from uvicorn import run as app_run
import pandas as pd
import os
import certifi
from dotenv import load_dotenv
from pymongo import MongoClient
from fastapi.middleware.cors import CORSMiddleware
from networksecurity.exception.exception import NetworkSecurityException
from networksecurity.logging.logger import logging
from networksecurity.pipeline.training_pipeline import TrainingPipeline
from networksecurity.utils.ml_utlils.model.estimator import NetworkModel
from networksecurity.utils.main_utlis.utils import load_object
from networksecurity.constants.training_pipeline import *

# Initialize MongoDB client
ca = certifi.where()
load_dotenv()
mongo_db_url = os.getenv('MONGO_DB_URL')
client = MongoClient(mongo_db_url, tlsCAFile=ca)
database = client[DATA_INGESTION_DATABASE_NAME]
COLLECTION = database[DATA_INGESTION_COLLECTION_NAME]

# FastAPI app setup
app = FastAPI()
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=['*'],
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*'],
)

templates = Jinja2Templates(directory="./templates")

@app.get("/", tags=['authentication'])
async def index():
    return RedirectResponse(url="/docs")

@app.get("/train")
async def train_route():
    try:
        train_pipeline = TrainingPipeline()
        train_pipeline.run_pipeline()
        return {"message": "Training completed successfully."}
    except Exception as e:
        logging.error(f"Training failed: {str(e)}")
        raise NetworkSecurityException(f"Training failed: {str(e)}")

@app.post("/predict")
async def predict_route(request: Request, file: UploadFile = File(...)):
    try:
        # Validate file type
        if not file.filename.endswith('.csv'):
            raise NetworkSecurityException(f"Invalid file type. Please upload a CSV file.", "File is not a CSV.")

        # Read the uploaded CSV file
        df = pd.read_csv(file.file)

        # Load preprocessor and model
        preprocessor = load_object("final_model/preprocessor.pkl")
        final_model = load_object("final_model/model.pkl")

        # Create the network model
        network_model = NetworkModel(preprocessor=preprocessor, model=final_model)
        
        # Predict and add prediction to the dataframe
        y_pred = network_model.predict(df)
        df['prediction'] = y_pred

        # Save the results
        df.to_csv("prediction_output/output.csv")

        # Optionally insert prediction results into MongoDB
        COLLECTION.insert_many(df.to_dict('records'))

        # Render the result table in HTML
        table_html = df.to_html()

        # Return the HTML response
        return templates.TemplateResponse("table.html", {"request": request, 'table': table_html})
    
    except Exception as e:
        logging.error(f"Prediction failed: {str(e)}")
        raise NetworkSecurityException(f"Prediction failed: {str(e)}")

if __name__ == "__main__":
    app_run(app, host="localhost", port=8000)
