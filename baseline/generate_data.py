"""
Generate sample dataset matching the research paper's data structure.
Based on the paper's analysis, we create a dataset with area, rooms, and price columns.
"""
import pandas as pd
import numpy as np

# Set seed for reproducibility
np.random.seed(42)

# Generate 46 records (inferred from paper's pie chart output)
data = {
    'area': np.random.randint(1000, 5000, 46),
    'rooms': np.random.choice([1, 2, 3, 4, 5], 46, p=[0.02, 0.13, 0.54, 0.28, 0.03]),
    'price': np.random.randint(169900, 700000, 46)
}

df = pd.DataFrame(data)
df.to_csv('data.csv', index=False)
print(f"Generated data.csv with {len(df)} records")
print(df.head())
print(f"\nStatistics:")
print(df.describe())

