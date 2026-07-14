import pandas as pd
from sqlalchemy import create_engine, text
from pathlib import Path
from utils.logger import logger

try:
    logger.info("=" * 50)
    logger.info("CareerPulse - Loading API Jobs into PostgreSQL")
    logger.info("=" * 50)

    # -------------------------------
    # Load Dataset
    # -------------------------------
    data_dir = Path(__file__).resolve().parent.parent / "data"

    clean_csv_path = data_dir / "clean_api_jobs.csv"
    raw_csv_path = data_dir / "api_jobs.csv"

    if clean_csv_path.exists():
        logger.info("Using validated dataset.")
        csv_path = clean_csv_path
    else:
        logger.warning("Validated dataset not found. Using raw API dataset.")
        csv_path = raw_csv_path

    df = pd.read_csv(csv_path)

    logger.info(f"Loaded {len(df)} records from {csv_path.name}")

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
        connection.execute(text("DROP TABLE IF EXISTS api_jobs"))

    logger.info("Old api_jobs table removed successfully.")

    # -------------------------------
    # Load Data
    # -------------------------------
    df.to_sql(
        "api_jobs",
        engine,
        if_exists="replace",
        index=False
    )

    logger.info(f"Successfully loaded {len(df)} records into api_jobs table.")

    # -------------------------------
    # Verify Load
    # -------------------------------
    with engine.connect() as connection:
        result = connection.execute(text("SELECT COUNT(*) FROM api_jobs"))
        total_rows = result.scalar()

    logger.info(f"Verification Successful: {total_rows} rows found in api_jobs table.")

    logger.info("API Jobs Loading Completed Successfully.")
    logger.info("=" * 50)

except Exception as e:
    logger.error(f"Failed to load API jobs into PostgreSQL: {e}")