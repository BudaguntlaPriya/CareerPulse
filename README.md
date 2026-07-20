# 📊 CareerPulse – End-to-End Job Market Intelligence Platform

## Overview

CareerPulse is a Data Engineering project that transforms real-time job postings into actionable market intelligence.

The project collects live job data from the Adzuna API, validates and transforms it through an ETL pipeline, stores the processed data inside a PostgreSQL Data Warehouse using a Star Schema, and presents analytical insights through an interactive Streamlit dashboard.

---

## Features

* Live Adzuna API Integration
* ETL Pipeline
* Data Validation & Cleaning
* Technical Skill Extraction
* PostgreSQL Data Warehouse
* Star Schema Design
* SQL Analytics
* Interactive Streamlit Dashboard
* Plotly Visualizations
* Career Guidance
* Hiring Trend Analysis
* Downloadable Reports

---

## Tech Stack

* Python
* PostgreSQL
* SQL
* Streamlit
* Plotly
* Pandas
* Requests
* SQLAlchemy
* Psycopg2

---

## Project Architecture

```text
Adzuna API
      │
      ▼
Raw Data (api_jobs.csv)
      │
      ▼
Validation & Cleaning
      │
      ▼
clean_api_jobs.csv
      │
      ▼
Skill Extraction
      │
      ▼
job_skills.csv
      │
      ▼
PostgreSQL Data Warehouse
      │
      ▼
Star Schema
      │
      ▼
Streamlit Dashboard
      │
      ▼
Job Market Intelligence
```

---

## Dashboard Modules

### 🏠 Home

* Dashboard KPIs
* Latest Jobs
* Warehouse Summary

### 🔍 Search Jobs

* Role Filter
* Company Filter
* Location Filter
* Download Results

### 🏢 Companies

* Top Hiring Companies
* Company Analytics

### 🎯 Career Guidance

* Required Skills
* Learning Roadmap
* Salary Insights

### 📊 Market Insights

* Pipeline Status
* Warehouse KPIs
* Data Quality Dashboard
* Hiring Trends
* Top Skills
* Top Companies
* Top Locations
* Role Distribution
* Pipeline Summary

---

## Database Schema

### Dimension Tables

* dim_jobs
* dim_skills

### Fact Table

* fact_job_skills

---

## Installation

```bash
git clone https://github.com/your-username/CareerPulse.git

cd CareerPulse

pip install -r requirements.txt

streamlit run portal/app.py
```

---

## Folder Structure

```text
CareerPulse/

api/
analytics/
ingestion/
validation/
warehouse/
portal/

data/
README.md
requirements.txt
```

---

## Future Scope

* Apache Airflow
* Docker
* Cloud Deployment
* Incremental Loading
* Authentication
* Recommendation Engine

---

## Author

**Priya**

B.Tech – AI & Data Science

Data Engineering Project

---

⭐ If you found this project useful, consider giving it a star on GitHub.


