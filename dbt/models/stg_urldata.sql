with stg_urldata as(

SELECT YEAR as "YEAR", LEVEL as "LEVEL", PARENTTOPIC as "TOPIC", COUNT(TOPICNAME) AS "NUMBER_OF_ARTICLES"
FROM {{ source('my_new_project', 'urldata') }}
WHERE YEAR IS NOT NULl AND LEVEL IS NOT NULL
GROUP BY YEAR, LEVEL, PARENTTOPIC
)

select * from stg_urldata