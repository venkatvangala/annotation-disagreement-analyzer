SELECT
    id,
    text,
    COUNT(*) AS raters,
    (
        CASE WHEN SUM(admiration)    BETWEEN 1 AND COUNT(*)-1 THEN 1 ELSE 0 END +
        CASE WHEN SUM(amusement)     BETWEEN 1 AND COUNT(*)-1 THEN 1 ELSE 0 END +
        CASE WHEN SUM(anger)         BETWEEN 1 AND COUNT(*)-1 THEN 1 ELSE 0 END +
        CASE WHEN SUM(annoyance)     BETWEEN 1 AND COUNT(*)-1 THEN 1 ELSE 0 END +
        CASE WHEN SUM(approval)      BETWEEN 1 AND COUNT(*)-1 THEN 1 ELSE 0 END +
        CASE WHEN SUM(caring)        BETWEEN 1 AND COUNT(*)-1 THEN 1 ELSE 0 END +
        CASE WHEN SUM(confusion)     BETWEEN 1 AND COUNT(*)-1 THEN 1 ELSE 0 END +
        CASE WHEN SUM(curiosity)     BETWEEN 1 AND COUNT(*)-1 THEN 1 ELSE 0 END +
        CASE WHEN SUM(desire)        BETWEEN 1 AND COUNT(*)-1 THEN 1 ELSE 0 END +
        CASE WHEN SUM(disappointment) BETWEEN 1 AND COUNT(*)-1 THEN 1 ELSE 0 END +
        CASE WHEN SUM(disapproval)   BETWEEN 1 AND COUNT(*)-1 THEN 1 ELSE 0 END +
        CASE WHEN SUM(disgust)       BETWEEN 1 AND COUNT(*)-1 THEN 1 ELSE 0 END +
        CASE WHEN SUM(embarrassment) BETWEEN 1 AND COUNT(*)-1 THEN 1 ELSE 0 END +
        CASE WHEN SUM(excitement)    BETWEEN 1 AND COUNT(*)-1 THEN 1 ELSE 0 END +
        CASE WHEN SUM(fear)          BETWEEN 1 AND COUNT(*)-1 THEN 1 ELSE 0 END +
        CASE WHEN SUM(gratitude)     BETWEEN 1 AND COUNT(*)-1 THEN 1 ELSE 0 END +
        CASE WHEN SUM(grief)         BETWEEN 1 AND COUNT(*)-1 THEN 1 ELSE 0 END +
        CASE WHEN SUM(joy)           BETWEEN 1 AND COUNT(*)-1 THEN 1 ELSE 0 END +
        CASE WHEN SUM(love)          BETWEEN 1 AND COUNT(*)-1 THEN 1 ELSE 0 END +
        CASE WHEN SUM(nervousness)   BETWEEN 1 AND COUNT(*)-1 THEN 1 ELSE 0 END +
        CASE WHEN SUM(optimism)      BETWEEN 1 AND COUNT(*)-1 THEN 1 ELSE 0 END +
        CASE WHEN SUM(pride)         BETWEEN 1 AND COUNT(*)-1 THEN 1 ELSE 0 END +
        CASE WHEN SUM(realization)   BETWEEN 1 AND COUNT(*)-1 THEN 1 ELSE 0 END +
        CASE WHEN SUM(relief)        BETWEEN 1 AND COUNT(*)-1 THEN 1 ELSE 0 END +
        CASE WHEN SUM(remorse)       BETWEEN 1 AND COUNT(*)-1 THEN 1 ELSE 0 END +
        CASE WHEN SUM(sadness)       BETWEEN 1 AND COUNT(*)-1 THEN 1 ELSE 0 END +
        CASE WHEN SUM(surprise)      BETWEEN 1 AND COUNT(*)-1 THEN 1 ELSE 0 END +
        CASE WHEN SUM(neutral)       BETWEEN 1 AND COUNT(*)-1 THEN 1 ELSE 0 END
    ) AS split_emotions
FROM annotations
GROUP BY id, text
HAVING COUNT(*) >= 3
ORDER BY split_emotions DESC
LIMIT 15;