import pandas as pd

# Load dataset
df = pd.read_csv("../job_market_dataset (1).csv")

# Show first 5 rows
print("First 5 Rows:")
print(df.head())

# Shape
print("\nShape:")
print(df.shape)

# Columns
print("\nColumns:")
print(df.columns)

# Missing values
print("\nMissing Values:")
print(df.isnull().sum())