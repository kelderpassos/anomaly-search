WITH identify_anomalies AS (
SELECT
	time,
    status,
    count,
    CASE
		WHEN zscore < -3 THEN 'anomaly detected'
        WHEN zscore > 3 THEN 'anomaly detected'
        ELSE 'not an anomaly'
	END as classification
FROM(
	SELECT
		id,
		time,
		status,
		count,
		(count - AVG(count) OVER (PARTITION BY status))
			/ STD(count) OVER(PARTITION BY status) AS zscore
 FROM registry.transaction
    GROUP BY id, time, status, count
) as score ORDER BY id)

SELECT 
	*
FROM identify_anomalies
WHERE classification = 'anomaly detected'
	AND (status = 'denied' OR status = 'failed' OR status = 'reversed')
ORDER BY time;