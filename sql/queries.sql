SELECT COUNT(*) FROM jobs;

SELECT company, COUNT(*) AS total_jobs
FROM jobs
GROUP BY company
ORDER BY total_jobs DESC
LIMIT 10;

SELECT location, COUNT(*) AS total_jobs
FROM jobs
GROUP BY location
ORDER BY total_jobs DESC;

SELECT job_title, AVG(salary_lpa) AS avg_salary
FROM jobs
GROUP BY job_title;


SELECT experience, AVG(salary_lpa) AS avg_salary
FROM jobs
GROUP BY experience
ORDER BY experience;


SELECT job_title, company, salary_lpa
FROM jobs
ORDER BY salary_lpa DESC
LIMIT 10;

SELECT job_type, COUNT(*) AS total_jobs
FROM jobs
GROUP BY job_type;