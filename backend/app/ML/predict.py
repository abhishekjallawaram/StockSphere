from fastapi import FastAPI, HTTPException, APIRouter
from pydantic import BaseModel
import numpy as np
import pandas as pd
import yfinance as yf
from tensorflow.keras.models import load_model
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
import os

router = APIRouter()

class PredictionRequest(BaseModel):
    symbol: str
    date: str  

def fetch_stock_data(symbol, start_date, end_date):
    """Fetches historical stock data from Yahoo Finance."""
    df = yf.download(symbol, start=start_date, end=end_date)
    return df['Close']

def prepare_data(symbol, end_date):
    """Pre-process the data"""
    start_date = pd.to_datetime(end_date) - pd.Timedelta(days=90)  
    data = fetch_stock_data(symbol, start_date.strftime('%Y-%m-%d'), end_date)
    scaler = MinMaxScaler(feature_range=(0, 1))
    scaled_data = scaler.fit_transform(np.array(data).reshape(-1, 1))
    return scaled_data[-60:].reshape(1, 60, 1), scaler, data

def prediction_data(symbol, start_date, max_days=30):
    """Ensure fetching exactly 10 days of stock data, adjusting for non-trading days."""
    attempt = 1
    days_added = 1
    while attempt <= max_days:
        ending_date = start_date + pd.Timedelta(days=10 + days_added)
        data = fetch_stock_data(symbol, start_date.strftime('%Y-%m-%d'), ending_date.strftime('%Y-%m-%d'))
        if len(data) >= 10:
            return data[:10]  
        days_added += 1 
        attempt += 1
    return pd.Series()  

@router.post("/predict/")
async def predict(request: PredictionRequest):
    symbol = request.symbol
    end_date = request.date
    model_path = os.path.abspath(os.path.join('app/ML/ML-models', symbol, f'{symbol}-model.h5'))
    print("Absolute model path:", model_path)

    if not os.path.exists(model_path):
        raise HTTPException(status_code=404, detail="Model not found")
    
    try:
        model = load_model(model_path)
        scaled_data, scaler, original_data = prepare_data(symbol, end_date)
        predictions = []
        for _ in range(10):
            pred = model.predict(scaled_data)
            scaled_data = np.append(scaled_data.flatten()[1:], pred).reshape(1, 60, 1)
            predictions.append(scaler.inverse_transform(pred).flatten()[0].item())
        starting_date = pd.to_datetime(end_date) + pd.Timedelta(days=1)
        data = prediction_data(symbol, starting_date)
        print(data)

        if len(data) == 10:
            rmse = np.sqrt(mean_squared_error(data, predictions))
            print("RMSE:", rmse)
        else:
            print("Failed to retrieve 10 days of data.")

        return {"predictions": predictions, "rmse": rmse}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))