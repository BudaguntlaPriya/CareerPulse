import requests
import json
import pandas as pd
from api_config import APP_ID, API_KEY
url = f"https://api.adzuna.com/v1/api/jobs/in/search/1?app_id={APP_ID}&app_key={API_KEY}&results_per_page=20&what=Data Engineer"
response = requests.get(url)
print(response.status_code)
data = response.json()

print(type(data))
print(data.keys())
# Create an empty list
jobs = []

# Extract required fields from each job
for job in data["results"]:

    jobs.append({

        "job_id": job.get("id"),

        "job_title": job.get("title"),

        "company": job.get("company", {}).get("display_name"),

        "location": job.get("location", {}).get("display_name"),

        "category": job.get("category", {}).get("label"),

        "job_type": job.get("contract_time"),

        "posted_date": job.get("created"),

        "description": job.get("description"),

        "redirect_url": job.get("redirect_url")

    })

# Convert list into DataFrame
df = pd.DataFrame(jobs)

# Display first 5 rows
print("\nFirst 5 Jobs:")
print(df.head())

# Display dataset information
print("\nShape of DataFrame:")
print(df.shape)

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

print(f"\n✅ API data saved successfully to: {csv_path}")
if __name__ == "__main__":
    print("\nFirst 5 Jobs:")
    print(df.head())

    print("\nShape of DataFrame:")
    print(df.shape)

    print("\nColumn Names:")
    print(df.columns)

    print(f"\n✅ API data saved successfully to: {csv_path}")
