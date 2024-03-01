with stg_learning_outcomes as(

select YEAR , LEVEL , PARENTTOPIC as "TOPIC", MIN(LEN(LEARNINGOUTCOME)) AS "MIN_LEARNING_OUTCOME", 
MAX(LEN(LEARNINGOUTCOME)) AS "MAX_LEARNING_OUTCOME"
FROM {{ source('my_new_project', 'urldata') }}
where NOT (LEARNINGOUTCOME = 'Learning Outcomes section is missing.')
GROUP BY YEAR, LEVEL, PARENTTOPIC

)

select * from stg_learning_outcomes