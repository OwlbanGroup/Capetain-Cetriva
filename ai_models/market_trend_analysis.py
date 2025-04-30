import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import yfinance as yf

def download_data(ticker, period='1y', interval='1d'):
    data = yf.download(ticker, period=period, interval=interval)
    data.dropna(inplace=True)
    return data

def feature_engineering(data):
    data['Return'] = data['Adj Close'].pct_change()
    data['Volatility'] = data['Return'].rolling(window=5).std()
    data['Momentum'] = data['Adj Close'] - data['Adj Close'].shift(5)
    data['Target'] = np.where(data['Adj Close'].shift(-1) > data['Adj Close'], 1, 0)
    data.dropna(inplace=True)
    return data

def train_model(data):
    features = ['Return', 'Volatility', 'Momentum']
    X = data[features]
    y = data['Target']
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    return model

def main():
    ticker = 'GLD'  # SPDR Gold Shares ETF as proxy for gold market
    data = download_data(ticker)
    data = feature_engineering(data)
    model = train_model(data)

if __name__ == "__main__":
    main()
