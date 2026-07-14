

SELECT
    a.company,
    s.skill,
    COUNT(*) AS demand
FROM api_jobs a
JOIN job_skills s
ON a.job_id = s.job_id
GROUP BY a.company, s.skill
ORDER BY demand DESC;


SELECT
    skill,
    COUNT(*) AS total_jobs
FROM job_skills
GROUP BY skill
ORDER BY total_jobs DESC;



SELECT
    skill,
    COUNT(*) AS demand
FROM job_skills
WHERE searched_role = 'Data Engineer'
GROUP BY skill
ORDER BY demand DESC;



SELECT
    skill,
    COUNT(*) AS demand
FROM job_skills
WHERE skill IN ('AWS', 'Azure', 'GCP')
GROUP BY skill
ORDER BY demand DESC;