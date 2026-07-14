import sys
from pathlib import Path
import pandas as pd

# Ensure project root is on PYTHONPATH so `utils.logger` can be imported
PROJECT_ROOT = Path(__file__).resolve().parent.parent
if str(PROJECT_ROOT) not in sys.path:
    sys.path.insert(0, str(PROJECT_ROOT))

from utils.logger import logger


try:
    logger.info("=" * 50)
    logger.info("CareerPulse Skill Extraction Started")
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

    logger.info(f"Loaded {len(df)} job records.")

    # -------------------------------
    # Skills Dictionary
    # -------------------------------
    skills = [
        "Python",
        "SQL",
        "Spark",
        "Hadoop",
        "Kafka",
        "Airflow",
        "Docker",
        "Kubernetes",
        "AWS",
        "Azure",
        "GCP",
        "Snowflake",
        "Databricks",
        "Tableau",
        "Power BI",
        "TensorFlow",
        "PyTorch",
        "Machine Learning",
        "Deep Learning",
        "Pandas",
        "NumPy",
        "ETL",
        "Data Warehouse",
        "PostgreSQL",
        "MySQL",
        "MongoDB",
        "Redis",
        "Linux",
        "Git",
        "Java",
        "Scala"
    ]

    logger.info(f"Searching for {len(skills)} predefined skills.")

    # -------------------------------
    # Extract Skills
    # -------------------------------
    records = []

    for _, row in df.iterrows():

        description = str(row["description"]).lower()

        for skill in skills:

            if skill.lower() in description:

                records.append({

                    "job_id": row["job_id"],
                    "searched_role": row["searched_role"],
                    "company": row["company"],
                    "job_title": row["job_title"],
                    "skill": skill

                })

    skills_df = pd.DataFrame(records)

    logger.info(f"Extracted {len(skills_df)} skill records.")

    # -------------------------------
    # Save Skills Dataset
    # -------------------------------
    output = data_dir / "job_skills.csv"

    skills_df.to_csv(output, index=False)

    logger.info(f"Skills dataset saved at: {output}")

    logger.info("Skill Extraction Completed Successfully.")
    logger.info("=" * 50)

except Exception as e:
    logger.error(f"Skill Extraction Failed: {e}")