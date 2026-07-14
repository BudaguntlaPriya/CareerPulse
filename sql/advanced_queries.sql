-- Query 1: Top 10 most frequent skills across all job postings (skill popularity)
SELECT

    skill,
    COUNT(*) AS total_jobs
FROM job_skills
GROUP BY skill
ORDER BY total_jobs DESC
LIMIT 10;


-- Query 2: Companies with the most job postings that mention the 'Python' skill
SELECT
    a.company,
    COUNT(*) AS total_jobs
FROM api_jobs a
JOIN job_skills s
ON a.job_id = s.job_id
WHERE s.skill = 'Python'
GROUP BY a.company

ORDER BY total_jobs DESC;

-- Query 3: Skill counts grouped by the searched role (skill distribution per role)
SELECT
    s.searched_role,
    s.skill,
    COUNT(*) AS total_jobs
FROM job_skills s
GROUP BY
    s.searched_role,
    s.skill
ORDER BY

    s.searched_role,
    total_jobs DESC;

-- Query 4: Counts of cloud platform skills (AWS, Azure, GCP) across job postings
SELECT
    skill,
    COUNT(*) AS total_jobs
FROM job_skills

WHERE skill IN ('AWS','Azure','GCP')
GROUP BY skill
ORDER BY total_jobs DESC;


-- Query 5: Top 10 companies by number of job postings
SELECT
    company,
    COUNT(*) AS total_jobs
FROM api_jobs
GROUP BY company
ORDER BY total_jobs DESC
LIMIT 10;


-- Query 6: Number of extracted skill records per searched role (how many skills mentioned per role)
SELECT
    searched_role,
    COUNT(*) AS total_skills
FROM job_skills
GROUP BY searched_role
ORDER BY total_skills DESC;

-- Query 7: For each company, counts of each skill (company × skill frequency)
SELECT
    a.company,
    s.skill,
    COUNT(*) AS total_jobs
FROM api_jobs a
JOIN job_skills s

ON a.job_id = s.job_id
GROUP BY
    a.company,
    s.skill
ORDER BY
    a.company,
    total_jobs DESC;