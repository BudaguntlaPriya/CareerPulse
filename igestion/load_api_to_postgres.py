import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path

# Load API data
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

# Clear old data
with engine.begin() as connection:
    connection.execute(text("TRUNCATE TABLE api_jobs"))

print("📥 Loading API jobs data into database...")

df.to_sql("api_jobs", engine, if_exists="append", index=False)

print(f"✅ Successfully loaded {len(df)} jobs into the 'api_jobs' table!")