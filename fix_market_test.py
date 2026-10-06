with open('ai_models/test_market_trend_analysis.py', 'r') as f:
    content = f.read()

# Add pytest import after pandas import
content = content.replace(
    'import pandas as pd\n',
    'import pandas as pd\nimport pytest\n',
    1
)

# Add requires_torch marker to the class
content = content.replace(
    'class TestMarketTrendAnalysis(unittest.TestCase):',
    '@pytest.mark.requires_torch\nclass TestMarketTrendAnalysis(unittest.TestCase):',
    1
)

with open('ai_models/test_market_trend_analysis.py', 'w') as f:
    f.write(content)

print('Added pytest import and requires_torch marker')
