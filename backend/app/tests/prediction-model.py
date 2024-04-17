import yfinance as yf
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler, OneHotEncoder
from sklearn.compose import ColumnTransformer
import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense, Dropout
import matplotlib.pyplot as plt

def fetch_data(symbols, start_date, end_date):
    data = {symbol: yf.download(symbol, start=start_date, end=end_date) for symbol in symbols}
    for symbol in data:
        data[symbol]['Symbol'] = symbol
    combined_data = pd.concat(data.values())
    return combined_data

def preprocess_data(data):
    data['Daily Return'] = data.groupby('Symbol')['Close'].pct_change()
    data.dropna(inplace=True)
    features = ['Symbol', 'Open', 'High', 'Low', 'Volume', 'Daily Return']
    target = 'Close'
    
    preprocessor = ColumnTransformer(transformers=[
        ('num', StandardScaler(), ['Open', 'High', 'Low', 'Volume', 'Daily Return']),
        ('cat', OneHotEncoder(), ['Symbol'])
    ])
    X = preprocessor.fit_transform(data[features])
    y = data[target].values
    return X, y

def build_model(input_shape):
    model = Sequential([
        LSTM(50, return_sequences=True, input_shape=input_shape),
        Dropout(0.2),
        LSTM(50),
        Dropout(0.2),
        Dense(1)
    ])
    model.compile(optimizer='adam', loss='mean_squared_error')
    return model

def plot_predictions(actual, predicted):
    plt.figure(figsize=(10, 5))
    plt.plot(actual, label='Actual Prices')
    plt.plot(predicted, label='Predicted Prices', alpha=0.7)
    plt.title('Actual vs Predicted Prices')
    plt.xlabel('Time')
    plt.ylabel('Price')
    plt.legend()
    plt.show()


def main():
    symbols = [
    'AAPL', 'MSFT', 'AMZN', 'GOOGL', 'META', 'BRK-B', 'JNJ', 'V', 'PG', 'JPM',
    'TSLA', 'NVDA', 'DIS', 'NFLX', 'PFE', 'KO', 'NKE', 'XOM', 'CVX', 'CSCO',
    'INTC', 'WMT', 'T', 'VZ', 'UNH', 'HD', 'MCD', 'BA', 'MMM', 'CAT',
    'GS', 'IBM', 'MRK', 'GE', 'F', 'GM', 'ADBE', 'CRM', 'ORCL', 'ABT',
    'BAC', 'C', 'GILD', 'LLY', 'MDT', 'AMGN', 'MO', 'PEP', 'TMO', 'DHR'
]
    start_date = '2020-01-01'
    end_date = '2024-01-01'
    
   
    data = fetch_data(symbols, start_date, end_date)
    X, y = preprocess_data(data)
    
    
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    
    
    X_train = X_train.reshape((X_train.shape[0], 1, X_train.shape[1]))
    X_test = X_test.reshape((X_test.shape[0], 1, X_test.shape[1]))
    
    
    model = build_model((X_train.shape[1], X_train.shape[2]))
    model.fit(X_train, y_train, epochs=50, validation_data=(X_test, y_test), verbose=1)
    
    predictions = model.predict(X_test)
    plot_predictions(y_test, predictions)
    mse = tf.keras.losses.MeanSquaredError()
    print(f'Test MSE: {mse(y_test, predictions).numpy()}')

if __name__ == '__main__':
    main()
