# Initial Design Document — CareerPulse

## Business Problem

Job seekers often lack visibility into hiring trends, required skills, and salary patterns across industries.

## Solution

CareerPulse provides a centralized analytics platform for understanding job market trends using historical and live job data.

## Key Questions Answered

* Which companies are hiring most?
* Which skills are trending?
* Which locations have more opportunities?
* What salary ranges exist for different roles?

## Architecture

Synthetic Dataset + Job API
↓
Python Ingestion Layer
↓
PostgreSQL Data Warehouse
↓
dbt Transformations
↓
Streamlit Dashboard


## Tech Stack

| Layer                | Technology                     |
| -------------------- | ------------------------------ |
| Programming Language | Python                         |
| Data Source          | Synthetic Dataset + Adzuna API |
| Data Processing      | Pandas                         |
| Database / Warehouse | PostgreSQL                     |
| Query Language       | SQL                            |
| Transformation       | dbt                            |
| Visualization        | Streamlit                      |
| Version Control      | Git + GitHub                   |
| Containerization     | Docker                         |


## Expected Insights

* Top hiring companies
* Most demanded skills
* Salary trends
* Location-wise hiring trends
