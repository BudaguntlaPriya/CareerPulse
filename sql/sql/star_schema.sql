-- ==========================
-- Dimension: Jobs
-- ==========================

DROP TABLE IF EXISTS dim_jobs;



CREATE TABLE dim_jobs AS
SELECT DISTINCT
    job_id,
    job_title,
    company,
    location,
    category,
    job_type,
    posted_date,
    searched_role,
    redirect_url,
    description
FROM api_jobs;
-- ==========================
-- Dimension: Skills
-- ==========================

DROP TABLE IF EXISTS dim_skills;

CREATE TABLE dim_skills AS
SELECT DISTINCT
    skill
FROM job_skills;

-- Add a surrogate key
ALTER TABLE dim_skills
ADD COLUMN skill_id SERIAL PRIMARY KEY;

-- ==========================
-- Fact Table
-- ==========================

DROP TABLE IF EXISTS fact_job_skills;

CREATE TABLE fact_job_skills AS
SELECT
    js.job_id,
    ds.skill_id
FROM job_skills js
JOIN dim_skills ds
ON js.skill = ds.skill;

---verify the data in the tables

SELECT * FROM dim_jobs LIMIT 5;

SELECT * FROM dim_skills LIMIT 5;

SELECT * FROM fact_job_skills LIMIT 5;