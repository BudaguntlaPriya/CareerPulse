import pandas as pd
from sqlalchemy import create_engine, text

# Load dataset
df = pd.read_csv("../job_market_dataset (1).csv")

# PostgreSQL connection
username = "postgres"
password = "Priya2107"
host = "localhost"
port = "5432"
database = "careerpulse_db"

engine = create_engine(
    f"postgresql://{username}:{password}@{host}:{port}/{database}"
)

# Clear existing rows so reruns do not fail on duplicate primary keys
with engine.begin() as connection:
    connection.execute(text("TRUNCATE TABLE jobs RESTART IDENTITY"))

# Insert data into jobs table
df.to_sql("jobs", engine, if_exists="append", index=False)

print("Data loaded successfully!")