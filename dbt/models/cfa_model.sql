WITH urldata AS (
    SELECT * FROM {{ ref('stg_urldata') }}
),
summary AS (
    SELECT * FROM {{ ref('stg_summary') }}
),
learning_outcome AS (
    SELECT * FROM {{ ref('stg_learning_outcomes') }}
)


SELECT
    urldata.YEAR,
    urldata.LEVEL,
    urldata.TOPIC,
    urldata.NUMBER_OF_ARTICLES,
    summary.MIN_SUMMARY,
    summary.MAX_SUMMARY,
    learning_outcome.MIN_LEARNING_OUTCOME,
    learning_outcome.MAX_LEARNING_OUTCOME
FROM urldata 
JOIN summary ON urldata.YEAR = summary.YEAR AND urldata.LEVEL = summary.LEVEL AND urldata.TOPIC = summary.TOPIC
JOIN learning_outcome ON urldata.YEAR = learning_outcome.YEAR AND urldata.LEVEL = learning_outcome.LEVEL AND urldata.TOPIC = learning_outcome.TOPIC
