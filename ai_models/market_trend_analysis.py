import pandas as pd
import numpy as np
from sklearn.ensemble import RandomForestClassifier
from sklearn.model_selection import train_test_split
from sklearn.metrics import classification_report
import yfinance as yf
import time


class MarketTrendAnalysis:
    def __init__(self, ticker="GLD"):
        self.ticker = ticker
        self.model = None
        self.data = None

    def download_data(self, period='1y', interval='1d', max_retries=3, retry_delay=10):
        for attempt in range(max_retries):
            try:
                data = yf.download(
                    self.ticker,
                    period=period,
                    interval=interval,
                )
                if data.empty:
                    raise ValueError("Downloaded data is empty")
                data.dropna(inplace=True)
                self.data = data
                return data
            except Exception as e:
                print(
                    f"Attempt {attempt + 1} failed to download data for {self.ticker}: {e}"
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
                                loc=100,
                                scale=5,
                                size=len(dates),
                            )
                        },
                        index=dates,
                    )
                    self.data = sample_data
                    return sample_data

    def feature_engineering(self):
        if self.data is None:
            raise ValueError("Data not loaded. Call download_data() first.")
        data = self.data.copy()
        data["Return"] = data["Adj Close"].pct_change()
        data["Volatility"] = data["Return"].rolling(window=5).std()
        data["Momentum"] = data["Adj Close"] - data["Adj Close"].shift(5)
        data["Target"] = np.where(
            data["Adj Close"].shift(-1) > data["Adj Close"], 1, 0
        )
        data.dropna(inplace=True)
        self.data = data
        return data

    def train_model(self):
        if self.data is None:
            raise ValueError("Data not prepared. Call feature_engineering() first.")
        features = ["Return", "Volatility", "Momentum"]
        X = self.data[features]
        y = self.data["Target"]
        model = RandomForestClassifier(n_estimators=100, random_state=42)
        if len(X) < 2:
            # Train on entire dataset without splitting if data is minimal
            model.fit(X, y)
            self.model = model
            return model
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=0.2, random_state=42
        )
        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)
        print(classification_report(y_test, y_pred))
        self.model = model
        return model
            
    def reinforce_learning_placeholder(self):
        """
        Placeholder method for reinforcement learning integration.
        This method can be expanded to include reinforcement learning algorithms
        such as Q-learning, policy gradients, or other advanced techniques.
        """
        print("Reinforcement learning integration placeholder.")


def main():
    analysis = MarketTrendAnalysis()
    analysis.download_data()
    analysis.feature_engineering()
    analysis.train_model()
    analysis.reinforce_learning_placeholder()


if __name__ == "__main__":
    main()
