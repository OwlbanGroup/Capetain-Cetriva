"""
Market Trend Analysis Module

This module provides AI-driven market trend analysis using PyTorch neural networks
and reinforcement learning for stock prediction and portfolio optimization.
"""

import os
import sys
import time

sys.path.append(os.path.dirname(os.path.dirname(__file__)))

import numpy as np
import pandas as pd
import torch
import torch.nn as nn
import torch.optim as optim
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from torch.utils.data import DataLoader, TensorDataset
import yfinance as yf

from nvidia_integration import nvidia_integration

ADJ_CLOSE = "Adj Close"


class TrendPredictor(nn.Module):
    """Simple neural network for trend prediction."""

    def __init__(self, input_size=3, hidden_size=64, output_size=2):
        """Initialize the neural network layers."""
        super(TrendPredictor, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.fc2 = nn.Linear(hidden_size, hidden_size)
        self.fc3 = nn.Linear(hidden_size, output_size)
        self.relu = nn.ReLU()
        self.dropout = nn.Dropout(0.2)

    def forward(self, x):
        """Forward pass through the network."""
        x = self.relu(self.fc1(x))
        x = self.dropout(x)
        x = self.relu(self.fc2(x))
        x = self.dropout(x)
        x = self.fc3(x)
        return x


class MarketTrendAnalysis:
    """Class for market trend analysis using AI models."""

    def __init__(self, ticker="GLD"):
        """Initialize with stock ticker."""
        self.ticker = ticker
        self.model = None
        self.data = None

    def download_data(self, period='1y', interval='1d', max_retries=3, retry_delay=10):
        """Download stock data with retries and fallback."""
        for attempt in range(max_retries):
            try:
                data = yf.download(
                    self.ticker,
                    period=period,
                    interval=interval,
                    auto_adjust=False,
                )
                if data.empty:
                    raise ValueError("Downloaded data is empty")
                data.dropna(inplace=True)
                self.data = data
                return data
            except (ValueError, ConnectionError, TimeoutError) as e:
                print(
                    f"Attempt {attempt + 1} failed to download data for {self.ticker}: {e}"
                )
                if attempt < max_retries - 1:
                    time.sleep(retry_delay)
                else:
                    print("Max retries reached. Using fallback sample data.")
                    # Create fallback sample data
                    dates = pd.date_range(end=pd.Timestamp.today(), periods=252)
                    rng = np.random.default_rng(seed=42)
                    sample_data = pd.DataFrame(
                        {
                            ADJ_CLOSE: rng.normal(
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
        """Engineer features from stock data."""
        if self.data is None:
            raise ValueError("Data not loaded. Call download_data() first.")
        data = self.data.copy()
        data["Return"] = data[ADJ_CLOSE].pct_change()
        data["Volatility"] = data["Return"].rolling(window=5).std()
        data["Momentum"] = data[ADJ_CLOSE] - data[ADJ_CLOSE].shift(5)
        data["Target"] = np.where(
            data[ADJ_CLOSE].shift(-1) > data[ADJ_CLOSE], 1, 0
        )
        data.dropna(inplace=True)
        self.data = data
        return data

    def train_model(self, epochs=50, batch_size=32, learning_rate=0.001):
        """Train the trend prediction model using GPU acceleration."""
        if self.data is None:
            raise ValueError("Data not prepared. Call feature_engineering() first.")
        feature_columns = ["Return", "Volatility", "Momentum"]
        features_data = self.data[feature_columns].values.astype(np.float32)
        targets = self.data["Target"].values.astype(np.int64)

        device = nvidia_integration.device
        nvidia_integration.log_project_status("Market Trend Training")

        model = TrendPredictor(input_size=len(feature_columns)).to(device)
        criterion = nn.CrossEntropyLoss()
        optimizer = optim.Adam(model.parameters(), lr=learning_rate, weight_decay=1e-4)

        if len(features_data) < 2:
            # Minimal data: train on all
            features_tensor = torch.tensor(features_data, dtype=torch.float32).to(device)
            targets_tensor = torch.tensor(targets, dtype=torch.long).to(device)
            for _ in range(epochs):
                optimizer.zero_grad()
                outputs = model(features_tensor)
                loss = criterion(outputs, targets_tensor)
                loss.backward()
                optimizer.step()
            self.model = model
            return model

        train_features, test_features, train_targets, test_targets = train_test_split(
            features_data, targets, test_size=0.2, random_state=42
        )

        # Convert to tensors
        train_features_tensor = torch.tensor(train_features, dtype=torch.float32).to(device)
        train_targets_tensor = torch.tensor(train_targets, dtype=torch.long).to(device)
        test_features_tensor = torch.tensor(test_features, dtype=torch.float32).to(device)

        train_dataset = TensorDataset(train_features_tensor, train_targets_tensor)
        train_loader = DataLoader(
            train_dataset, batch_size=batch_size, shuffle=True, num_workers=0
        )

        # Training loop
        for _ in range(epochs):
            model.train()
            for batch_features, batch_targets in train_loader:
                optimizer.zero_grad()
                outputs = model(batch_features)
                loss = criterion(outputs, batch_targets)
                loss.backward()
                optimizer.step()

        # Evaluation
        model.eval()
        with torch.no_grad():
            test_outputs = model(test_features_tensor)
            _, predicted = torch.max(test_outputs, 1)
            predicted = predicted.cpu().numpy()
            print(classification_report(test_targets, predicted))

        self.model = model
        return model
            
    def reinforce_learning_placeholder(self, episodes=100, alpha=0.1, gamma=0.9):
        """
        Basic Q-learning for portfolio optimization (placeholder).
        States: simplified market conditions, actions: buy/sell/hold.
        """
        if self.data is None:
            raise ValueError("Data not prepared. Call feature_engineering() first.")

        device = nvidia_integration.device
        nvidia_integration.log_project_status("RL Training")

        # Simplified Q-table as tensor
        q_table = torch.zeros((10, 3), dtype=torch.float32).to(device)  # 10 states, 3 actions

        for _ in range(episodes):
            state = 0  # Start state
            for i in range(len(self.data) - 1):
                # Choose action (epsilon-greedy)
                if torch.rand(1).item() < 0.1:
                    action = torch.randint(0, 3, (1,)).item()
                else:
                    action = torch.argmax(q_table[state]).item()

                # Simulate reward (simplified)
                reward = 1 if self.data["Target"].iloc[i+1] == action % 2 else -1

                next_state = min(state + 1, 9)
                q_table[state, action] += alpha * (
                    reward + gamma * torch.max(q_table[next_state]) - q_table[state, action]
                )
                state = next_state

        print(f"RL training completed. Q-table shape: {q_table.shape}")


def main():
    analysis = MarketTrendAnalysis()
    analysis.download_data()
    analysis.feature_engineering()
    analysis.train_model()
    analysis.reinforce_learning_placeholder()


if __name__ == "__main__":
    main()
