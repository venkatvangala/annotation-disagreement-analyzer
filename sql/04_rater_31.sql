SELECT
    rater_id,
    COUNT(*) AS annotations,
    ROUND(AVG(n_labels), 2) AS avg_labels_per_item
FROM (
    SELECT
        rater_id,
        admiration + amusement + anger + annoyance + approval + caring +
        confusion + curiosity + desire + disappointment + disapproval +
        disgust + embarrassment + excitement + fear + gratitude + grief +
        joy + love + nervousness + optimism + pride + realization +
        relief + remorse + sadness + surprise + neutral AS n_labels
    FROM annotations
)
WHERE rater_id = 31
GROUP BY rater_id;