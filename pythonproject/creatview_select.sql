DROP VIEW IF EXISTS level;
CREATE VIEW level as
SELECT pe.id, pe.name, sc.subject, sc.score, cl.class,
CASE
    WHEN sc.score >= 80 THEN '优秀'
    WHEN sc.score >= 60 THEN '及格'
    ELSE '不及格'
END as sale_level
FROM personnel pe
RIGHT JOIN score_subject sc on pe.id = sc.id
LEFT JOIN class_name cl on cl.id = pe.id
-- WHERE sc.score > 59
;

SELECT
    class,
    subject,
    COUNT(*) AS total_num,  -- 该班该科总人数
    SUM(CASE WHEN sale_level='优秀' THEN 1 ELSE 0 END) AS excellent_num, --优秀人数
    SUM(CASE WHEN sale_level IN ('优秀','及格') THEN 1 ELSE 0 END) AS pass_num, --合格人数
    ROUND(SUM(CASE WHEN sale_level='优秀' THEN 1 ELSE 0 END)*100.0 / COUNT(*),2) || '%'AS excellent_rate, --优秀率(%)
    ROUND(SUM(CASE WHEN sale_level IN ('优秀','及格') THEN 1 ELSE 0 END)*100.0 / COUNT(*),2) || '%' AS pass_rate --合格率(%)
FROM level
GROUP BY class, subject
ORDER BY class, subject;
