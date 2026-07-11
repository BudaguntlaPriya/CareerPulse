# CareerPulse — Job Market Intelligence Pipeline

## Project Overview
CareerPulse is a Job Market Intelligence Pipeline designed to analyze hiring trends, skill demand, salary insights, and location-based opportunities.

## Problem Statement
Students and job seekers often struggle to understand:
- Which skills are in demand
- Which companies are hiring
- Salary trends
- Location-based opportunities

## Project Goals
- Build end-to-end DE pipeline
- Analyze job market trends
- Study salary insights
- Track skill demand

## Tech Stack
- Python
- PostgreSQL
- SQL
- dbt
- Streamlit
- Docker

## Architecture
Dataset + API  
↓  
Python Ingestion  
↓  
PostgreSQL  
↓  
dbt  
↓  
Dashboard

## Week 1 Progress 



- Created the CareerPulse GitHub repository.
- Set up the project folder structure.
- Configured the Python development environment in VS Code.
- Selected PostgreSQL as the project database.
- Designed the project architecture.
- Generated a synthetic job market dataset with 1000 records.
- Created project documentation:
  - Initial Design Document
  - Tech Stack
  - Learning Notes
  - Status Report


## 📅 Week 2 Progress

- Installed PostgreSQL and pgAdmin.
- Created the `careerpulse_db` database.
- Created the `jobs` table.
- Connected Python with PostgreSQL using SQLAlchemy.
- Loaded the synthetic dataset into PostgreSQL.
- Verified successful data insertion using SQL queries.
## Week 3 Progress

- Connected to the Adzuna Jobs API.
- Retrieved live job market data using REST API.
- Parsed nested JSON responses.
- Transformed raw data into a Pandas DataFrame.
- Loaded live API data into PostgreSQL.
- Verified successful data insertion using SQL queries.
