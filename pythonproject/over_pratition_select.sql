SELECT
    cl.class,
    sc.subject,
    pe.id,
    pe.name,
    sc.score,
    CASE
        WHEN sc.score >= 80 THEN '优秀'
        WHEN sc.score >= 60 THEN '及格'
        ELSE '不及格'
    END as sale_level,
    -- 分区总人数：班级+科目下总人数
    COUNT(*) OVER(PARTITION BY class, subject) AS total_num,
    -- 分区优秀人数
    SUM(CASE WHEN sc.score >= 80 THEN 1 ELSE 0 END) OVER(PARTITION BY class, subject) AS excellent_num,
    -- 分区合格人数（优秀+及格）
    SUM(CASE WHEN sc.score >= 60 THEN 1 ELSE 0 END) OVER(PARTITION BY class, subject) AS pass_num,
    -- 优秀率带百分号
    ROUND(SUM(CASE WHEN sc.score >= 80 THEN 1 ELSE 0 END) OVER(PARTITION BY class, subject)*100.0
        / COUNT(*) OVER(PARTITION BY class, subject),2) || '%' AS excellent_rate,
    -- 合格率带百分号
    ROUND(SUM(CASE WHEN sc.score >= 60 THEN 1 ELSE 0 END) OVER(PARTITION BY class, subject)*100.0
        / COUNT(*) OVER(PARTITION BY class, subject),2) || '%' AS pass_rate
FROM personnel pe
RIGHT JOIN score_subject sc on pe.id = sc.id
LEFT JOIN class_name cl on cl.id = pe.id
ORDER BY class, subject;
