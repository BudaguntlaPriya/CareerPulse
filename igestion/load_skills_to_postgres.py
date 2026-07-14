import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path
from utils.logger import logger

try:
    logger.info("=" * 50)
    logger.info("CareerPulse - Loading Skills into PostgreSQL")
    logger.info("=" * 50)

    # -------------------------------
    # Load Skills Dataset
    # -------------------------------
    csv_path = Path(__file__).resolve().parent.parent / "data" / "job_skills.csv"

    df = pd.read_csv(csv_path)

    logger.info(f"Loaded {len(df)} skill records from {csv_path.name}")

    # -------------------------------
    # PostgreSQL Connection
    # -------------------------------
    username = "postgres"
    password = "Priya2107"
    host = "localhost"
    port = "5432"
    database = "careerpulse_db"

    engine = create_engine(
        f"postgresql://{username}:{password}@{host}:{port}/{database}"
    )

    logger.info("Connected to PostgreSQL successfully.")

    # -------------------------------
    # Remove Old Table
    # -------------------------------
    with engine.begin() as connection:
        connection.execute(text("DROP TABLE IF EXISTS job_skills"))

    logger.info("Old job_skills table removed successfully.")

    # -------------------------------
    # Load Skills Data
    # -------------------------------
    df.to_sql(
        "job_skills",
        engine,
        if_exists="replace",
        index=False
    )

    logger.info(f"Successfully loaded {len(df)} skill records into job_skills table.")

    # -------------------------------
    # Verify Data Load
    # -------------------------------
    with engine.connect() as connection:
        result = connection.execute(text("SELECT COUNT(*) FROM job_skills"))
        total_rows = result.scalar()

    logger.info(f"Verification Successful: {total_rows} rows found in job_skills table.")

    logger.info("Skills Loading Completed Successfully.")
    logger.info("=" * 50)

except Exception as e:
    logger.error(f"Failed to load job_skills into PostgreSQL: {e}")