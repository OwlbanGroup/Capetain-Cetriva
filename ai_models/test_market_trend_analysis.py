import unittest
import pandas as pd
import numpy as np
from ai_models import market_trend_analysis as mta


class TestMarketTrendAnalysis(unittest.TestCase):
    def test_download_data_success(self):
        # Test downloading real data (may depend on network)
        data = mta.download_data(
            'AAPL',
            period='5d',
            interval='1d',
            max_retries=1,
        )
        self.assertFalse(data.empty)
        self.assertIn('Adj Close', data.columns)

    def test_download_data_fallback(self):
        # Test fallback data generation by forcing failure
        original_download = mta.yf.download

        def fail_download(*args, **kwargs):
            raise Exception("Forced failure")

        mta.yf.download = fail_download
        data = mta.download_data('FAKE', max_retries=1, retry_delay=0)
        mta.yf.download = original_download

        self.assertFalse(data.empty)
        self.assertIn('Adj Close', data.columns)
        self.assertEqual(len(data), 252)

    def test_feature_engineering(self):
        # Create sample data
        dates = pd.date_range('2023-01-01', periods=10)
        prices = np.linspace(100, 110, 10)
        df = pd.DataFrame({'Adj Close': prices}, index=dates)

        fe_df = mta.feature_engineering(df)
        self.assertIn('Return', fe_df.columns)
        self.assertIn('Volatility', fe_df.columns)
        self.assertIn('Momentum', fe_df.columns)
        self.assertIn('Target', fe_df.columns)
        self.assertFalse(fe_df.isnull().values.any())

    def test_train_model(self):
        # Create sample data with features and target
        dates = pd.date_range('2023-01-01', periods=100)
        prices = np.linspace(100, 110, 100)
        df = pd.DataFrame({'Adj Close': prices}, index=dates)
        df = mta.feature_engineering(df)

        model = mta.train_model(df)
        self.assertIsNotNone(model)
        self.assertTrue(hasattr(model, 'predict'))

        # Test prediction shape
        features = ['Return', 'Volatility', 'Momentum']
        X = df[features]
        preds = model.predict(X)
        self.assertEqual(len(preds), len(df))

    def test_feature_engineering_edge_cases(self):
        # Test feature engineering with constant prices (zero returns and momentum)
        dates = pd.date_range('2023-01-01', periods=10)
        prices = np.full(10, 100.0)
        df = pd.DataFrame({'Adj Close': prices}, index=dates)

        fe_df = mta.feature_engineering(df)
        self.assertTrue((fe_df['Return'] == 0).all())
        self.assertTrue((fe_df['Momentum'] == 0).all())
        self.assertFalse(fe_df['Volatility'].isnull().any())

    def test_train_model_with_minimal_data(self):
        # Test training model with minimal data (should handle small datasets)
        dates = pd.date_range('2023-01-01', periods=6)
        prices = np.linspace(100, 105, 6)
        df = pd.DataFrame({'Adj Close': prices}, index=dates)
        df = mta.feature_engineering(df)

        model = mta.train_model(df)
        self.assertIsNotNone(model)
        self.assertTrue(hasattr(model, 'predict'))

        features = ['Return', 'Volatility', 'Momentum']
        X = df[features]
        preds = model.predict(X)
        self.assertEqual(len(preds), len(df))


if __name__ == '__main__':
    unittest.main()
