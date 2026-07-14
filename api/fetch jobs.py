import logging
import requests
import json
import pandas as pd
from api_config import APP_ID, API_KEY
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(levelname)s - %(message)s"
)
#url = f"https://api.adzuna.com/v1/api/jobs/in/search/1?app_id={APP_ID}&app_key={API_KEY}&results_per_page=20&what=Data Engineer"
job_roles = [
    "Data Engineer",
    "Data Scientist",
    "Machine Learning Engineer",
    "AI Engineer",
    "Data Analyst",
    "Business Intelligence Developer",
    "Cloud Engineer",
    "Big Data Engineer",
    "Data Architect",
    "Analytics Engineer"
]
all_jobs = []
for role in job_roles:

    url = f"https://api.adzuna.com/v1/api/jobs/in/search/1?app_id={APP_ID}&app_key={API_KEY}&results_per_page=20&what={role}"
    response = requests.get(url)
    #print(response.status_code)
    logging.info(f"{role} API Status: {response.status_code}")

    data = response.json()

    for job in data["results"]:
        all_jobs.append({"job_id": job.get("id"),"searched_role": role,
         "job_title": job.get("title"),
          "company": job.get("company", {}).get("display_name"),
          "location": job.get("location", {}).get("display_name"),
          "category": job.get("category", {}).get("label"),
          "job_type": job.get("contract_time"),
          "posted_date": job.get("created"),
          "description": job.get("description"),
          "redirect_url": job.get("redirect_url")})

       
print("Length of all_jobs:", len(all_jobs))
# Convert list into DataFrame
df = pd.DataFrame(all_jobs)

# Display first 5 rows
print("\nFirst 5 Jobs:")
print(df.head())

# Display dataset information
#print("\nShape of DataFrame:")
#print(df.shape)

logging.info(f"Dataset Shape: {df.shape}")

print("\nColumn Names:")
print(df.columns)

# Save the data as CSV
import os
from pathlib import Path

# Ensure output directory exists (relative to this script)
out_dir = Path(__file__).resolve().parent.joinpath("..", "data").resolve()
out_dir.mkdir(parents=True, exist_ok=True)
csv_path = out_dir.joinpath("api_jobs.csv")
df.to_csv(csv_path, index=False)

#print(f"\n✅ API data saved successfully to: {csv_path}")
logging.info(f"CSV saved successfully at {csv_path}")