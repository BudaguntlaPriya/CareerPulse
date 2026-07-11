import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path

# Load API dataset
csv_path = Path(__file__).resolve().parent.parent / "data" / "api_jobs.csv"
df = pd.read_csv(csv_path)

# PostgreSQL Connection
username = "postgres"
password = "Priya2107"
host = "localhost"
port = "5432"
database = "careerpulse_db"

engine = create_engine(
    f"postgresql://{username}:{password}@{host}:{port}/{database}"
)

print("✅ Connected to PostgreSQL")

# Drop old table if it exists
with engine.begin() as connection:
    connection.execute(text("DROP TABLE IF EXISTS api_jobs"))

print("🗑 Old table removed")

# Create new table automatically and insert data
df.to_sql(
    "api_jobs",
    engine,
    if_exists="replace",
    index=False
)

print(f"✅ Successfully loaded {len(df)} jobs into PostgreSQL!")