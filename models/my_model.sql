select pdf_id, name 

from {{ source('my_new_project', 'metadata_pdf') }}