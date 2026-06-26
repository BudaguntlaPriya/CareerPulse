CREATE TABLE jobs (
    job_id INT PRIMARY KEY,
    job_title VARCHAR(100),
    company VARCHAR(100),
    location VARCHAR(100),
    salary_lpa INT,
    experience INT,
    skills TEXT,
    job_type VARCHAR(50),
    posted_date DATE
);