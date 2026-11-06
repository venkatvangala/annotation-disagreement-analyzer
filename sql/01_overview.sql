SELECT
    COUNT(DISTINCT id)       AS comments,
    COUNT(DISTINCT rater_id) AS raters,
    COUNT(*)                 AS total_annotations
FROM annotations;