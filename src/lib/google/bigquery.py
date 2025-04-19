'''
Main bigquery table
CREATE OR REPLACE TABLE `noble-office-299208.portfolio.gn-blog` (
  id STRING,
  title STRING,
  date TIMESTAMP,
  body STRING,
  views INT64,
  likes INT64,
  tags ARRAY<STRING>
)
OPTIONS(
  description = 'Table containing content with id, title, date, body, views, likes, and tags'
);
'''

def query():
    pass

def update():
    pass

def delete():
    pass