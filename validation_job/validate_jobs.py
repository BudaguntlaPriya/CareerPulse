import sys
import pandas as pd
from pathlib import Path

# Ensure project root is on sys.path so imports like `utils` resolve when
# running this script directly (script's directory is added to sys.path[0]).
project_root = Path(__file__).resolve().parent.parent
if str(project_root) not in sys.path:
    sys.path.insert(0, str(project_root))

from utils.logger import logger

try:
    logger.info("=" * 50)
    logger.info("CareerPulse Data Validation Started")
    logger.info("=" * 50)

    # -------------------------------
    # Load API Dataset
    # -------------------------------
    csv_path = Path(__file__).resolve().parent.parent / "data" / "api_jobs.csv"
    df = pd.read_csv(csv_path)

    initial_records = len(df)
    logger.info(f"Total Records Loaded: {initial_records}")

    # -------------------------------
    # Duplicate Job IDs
    # -------------------------------
    duplicate_count = df.duplicated(subset=["job_id"]).sum()

    if duplicate_count > 0:
        logger.warning(f"Duplicate Job IDs Found: {duplicate_count}")
    else:
        logger.info("No Duplicate Job IDs Found.")

    # Remove duplicates
    df = df.drop_duplicates(subset=["job_id"])

    # -------------------------------
    # Missing Values
    # -------------------------------
    missing_company = df["company"].isnull().sum()
    missing_title = df["job_title"].isnull().sum()
    missing_location = df["location"].isnull().sum()
    missing_description = df["description"].isnull().sum()

    logger.info(f"Missing Company Values: {missing_company}")
    logger.info(f"Missing Job Title Values: {missing_title}")
    logger.info(f"Missing Location Values: {missing_location}")
    logger.info(f"Missing Description Values: {missing_description}")

    if (
        missing_company > 0
        or missing_title > 0
        or missing_location > 0
        or missing_description > 0
    ):
        logger.warning("Dataset contains missing values.")

    # -------------------------------
    # Remove Invalid Records
    # -------------------------------
    df = df.dropna(subset=["job_title", "company"])

    # -------------------------------
    # Convert Date
    # -------------------------------
    df["posted_date"] = pd.to_datetime(
        df["posted_date"],
        errors="coerce"
    )

    invalid_dates = df["posted_date"].isnull().sum()

    if invalid_dates > 0:
        logger.warning(f"Invalid Dates Found: {invalid_dates}")
    else:
        logger.info("No Invalid Dates Found.")

    # Remove invalid dates
    df = df.dropna(subset=["posted_date"])

    # -------------------------------
    # Final Dataset Statistics
    # -------------------------------
    removed_records = initial_records - len(df)

    logger.info("-" * 50)
    logger.info(f"Records Removed During Validation: {removed_records}")
    logger.info(f"Valid Records Remaining: {len(df)}")

    # -------------------------------
    # Save Clean Dataset
    # -------------------------------
    clean_path = (
        Path(__file__).resolve().parent.parent
        / "data"
        / "clean_api_jobs.csv"
    )

    df.to_csv(clean_path, index=False)

    logger.info("Validation Completed Successfully.")
    logger.info(f"Clean Dataset Saved At: {clean_path}")
    logger.info("=" * 50)

except Exception as e:
    logger.error(f"Validation Failed: {e}")