with stg_summary as(

SELECT YEAR , LEVEL , PARENTTOPIC as "TOPIC", MIN(LEN(SUMMARY))  AS "MIN_SUMMARY", MAX(LEN(SUMMARY)) AS "MAX_SUMMARY"
FROM {{ source('my_new_project', 'urldata') }}
WHERE NOT (SUMMARY = 'Summary section is missing.')
GROUP BY YEAR, LEVEL, PARENTTOPIC
)

select * from stg_summary