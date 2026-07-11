SELECT company,
       COUNT(*) AS total_jobs
FROM api_jobs
GROUP BY company
ORDER BY total_jobs DESC;

SELECT searched_role,
       COUNT(*) AS total_jobs
FROM api_jobs
GROUP BY searched_role
ORDER BY total_jobs DESC;

SELECT location,
       COUNT(*) AS total_jobs
FROM api_jobs
GROUP BY location
ORDER BY total_jobs DESC;

SELECT job_title,
       COUNT(*) AS frequency
FROM api_jobs
GROUP BY job_title
ORDER BY frequency DESC
LIMIT 10;

SELECT job_type,
       COUNT(*) AS total_jobs
FROM api_jobs
GROUP BY job_type;

SELECT category,
       COUNT(*) AS total_jobs
FROM api_jobs
GROUP BY category
ORDER BY total_jobs DESC;

SELECT company,
       COUNT(*) AS total_jobs
FROM api_jobs
GROUP BY company
ORDER BY total_jobs DESC
LIMIT 10;


SELECT location,
       COUNT(*) AS total_jobs
FROM api_jobs
GROUP BY location
ORDER BY total_jobs DESC
LIMIT 10;

SELECT job_title,
       COUNT(*) AS total_jobs
FROM api_jobs
GROUP BY job_title
ORDER BY total_jobs DESC
LIMIT 10;

SELECT searched_role,
       company,
       COUNT(*) AS jobs
FROM api_jobs
GROUP BY searched_role, company
ORDER BY searched_role, jobs DESC;

SELECT category,
       COUNT(*) AS total_jobs
FROM api_jobs
GROUP BY category
ORDER BY total_jobs DESC;

SELECT job_title,
       company,
       posted_date
FROM api_jobs
ORDER BY posted_date DESC
LIMIT 10
;