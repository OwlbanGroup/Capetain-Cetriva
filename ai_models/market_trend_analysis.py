import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import yfinance as yf
import time


def download_data(ticker, period='1y', interval='1d', max_retries=3, retry_delay=10):

    for attempt in range(max_retries):
        try:
            data = yf.download(
                ticker,
                period=period,
                interval=interval,
            )
            if data.empty:
                raise ValueError("Downloaded data is empty")
            data.dropna(inplace=True)
            return data
        except Exception as e:
            print(
                f"Attempt {attempt + 1} failed to download data for {ticker}: {e}"
            )
            if attempt < max_retries - 1:
                time.sleep(retry_delay)
            else:
                print("Max retries reached. Using fallback sample data.")
                # Create fallback sample data
                dates = pd.date_range(end=pd.Timestamp.today(), periods=252)
                sample_data = pd.DataFrame(
                    {
                        "Adj Close": np.random.normal(
                            loc=100, scale=5, size=len(dates)
                        )
                    },
                    index=dates,
                )
                return sample_data


def feature_engineering(data):

    data["Return"] = data["Adj Close"].pct_change()
    data["Volatility"] = data["Return"].rolling(window=5).std()
    data["Momentum"] = data["Adj Close"] - data["Adj Close"].shift(5)
    data["Target"] = np.where(
        data["Adj Close"].shift(-1) > data["Adj Close"], 1, 0
    )
    data.dropna(inplace=True)
    return data


def train_model(data):

    features = ["Return", "Volatility", "Momentum"]
    X = data[features]
    y = data["Target"]
    X_train, X_test, y_train, y_test = train_test_split(
        X, y, test_size=0.2, random_state=42
    )
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X_train, y_train)
    y_pred = model.predict(X_test)
    print(classification_report(y_test, y_pred))
    return model


def main():

    ticker = "GLD"  # SPDR Gold Shares ETF as proxy for gold market
    data = download_data(ticker)
    data = feature_engineering(data)
    _model = train_model(data)


if __name__ == "__main__":
    main()
