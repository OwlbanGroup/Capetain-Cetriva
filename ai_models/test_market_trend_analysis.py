import unittest
import pandas as pd
import numpy as np
from ai_models.market_trend_analysis import MarketTrendAnalysis


class TestMarketTrendAnalysis(unittest.TestCase):

    def test_download_data_success(self):
        mta_instance = MarketTrendAnalysis()
        data = mta_instance.download_data(max_retries=1, retry_delay=0)
        self.assertIsNotNone(data)
        self.assertFalse(data.empty)

    def test_download_data_fallback(self):
        mta_instance = MarketTrendAnalysis(ticker="FAKE")
        data = mta_instance.download_data(max_retries=1, retry_delay=0)
        self.assertIsNotNone(data)
        self.assertFalse(data.empty)

    def test_feature_engineering(self):
        mta_instance = MarketTrendAnalysis()
        df = pd.DataFrame({
            "Adj Close": [100, 102, 101, 103, 105, 107, 106]
        })
        mta_instance.data = df
        fe_df = mta_instance.feature_engineering()
        self.assertIn("Return", fe_df.columns)
        self.assertIn("Volatility", fe_df.columns)
        self.assertIn("Momentum", fe_df.columns)
        self.assertIn("Target", fe_df.columns)

    def test_feature_engineering_edge_cases(self):
        mta_instance = MarketTrendAnalysis()
        df = pd.DataFrame({
            "Adj Close": [100, 100, 100, 100, 100]
        })
        mta_instance.data = df
        fe_df = mta_instance.feature_engineering()
        self.assertTrue((fe_df["Return"] == 0).all())
        self.assertTrue((fe_df["Volatility"] == 0).all())
        self.assertTrue((fe_df["Momentum"] == 0).all())

    def test_train_model(self):
        mta_instance = MarketTrendAnalysis()
        df = pd.DataFrame({
            "Adj Close": [100, 102, 101, 103, 105, 107, 106]
        })
        mta_instance.data = df
        mta_instance.feature_engineering()
        model = mta_instance.train_model()
        self.assertIsNotNone(model)

    def test_train_model_with_minimal_data(self):
        mta_instance = MarketTrendAnalysis()
        df = pd.DataFrame({
            "Adj Close": [100, 102]
        })
        mta_instance.data = df
        mta_instance.feature_engineering()
        model = mta_instance.train_model()
        self.assertIsNotNone(model)


if __name__ == "__main__":
    unittest.main()
