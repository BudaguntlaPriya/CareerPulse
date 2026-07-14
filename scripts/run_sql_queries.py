from pathlib import Path
import pandas as pd
from sqlalchemy import create_engine

# DB config (matches existing scripts)
username = "postgres"
password = "Priya2107"
host = "localhost"
port = "5432"
database = "careerpulse_db"

engine = create_engine(f"postgresql://{username}:{password}@{host}:{port}/{database}")

sql_file = Path(__file__).resolve().parent.parent.joinpath("sql", "advanced_queries.sql")
if not sql_file.exists():
    print(f"SQL file not found: {sql_file}")
    raise SystemExit(1)

content = sql_file.read_text()
# split on semicolon and keep non-empty statements
queries = [q.strip() for q in content.split(";") if q.strip()]

for i, q in enumerate(queries, start=1):
    print(f"\n=== Query {i} ===")
    print(q)
    print("--- Results ---")
    try:
        df = pd.read_sql_query(q, engine)
        if df.empty:
            print("(no rows)")
        else:
            # Show up to 20 rows
            print(df.head(20).to_string(index=False))
            print(f"Rows: {len(df)}")
    except Exception as e:
        print("Error executing query:", e)
