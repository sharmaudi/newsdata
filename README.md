# Udacity - Log Analysis Project
Reporting tool that prints out text based reports based on the data in the udacity news database.

# Prerequisites
1. This project is implemented using python 3.6 and has been tested with python version 3.6.1. It uses the latest f-strings string literals and is therefore incompatible with earlier versions of python.
2. This project is dependent on postgres database along with the news schema that comes with the Udacity virtual machine.

# Installation

### Clone the repository
```
git clone https://github.com/sharmaudi/newsdata.git
```
### Change to the repository directory
```
cd newsdata
```
### Install the dependencies. The project is dependent on click and psycopg2 modules.
```
pip install -r requirements.txt
```
### Set Environment variables
The following environment variables need to be set in order to connect to the postgres database.
```
export NEWS_DB_USER = 'db_user'
export NEWS_DB_PASSWORD = 'db_password'
export NEWS_DB_HOST= 'db_host'
```
Check news/config.py for more details

# Deployment
Run the reports.py script with the a report id. It will ask for the report id if none is given.

Here are the supported reports:

1. What are the most popular three articles of all time?
   `python reports.py --report 1`
2. Who are the most popular article authors of all time?
   `python reports.py --report 2`
3. On which days did more than 1% of requests lead to errors?
   `python reports.py --report 3`

To get help use `python reports.py --help`

# Database queries used
The following database queries have been used to generate the reports:
### 1. What are the most popular three articles of all time?

```
SELECT
articles.title,
  t.num::INT AS count
FROM
  articles,
  (SELECT
     path,
     count(*) AS num
   FROM log
   WHERE path != '/'
   GROUP BY path) AS t
WHERE articles.slug = substring(t.path FROM 10)
ORDER BY t.num DESC
LIMIT 3;
```

### 2. Who are the most popular article authors of all time?
```
SELECT
  authors.name,
  author_views.total_views::INT AS count
FROM authors,
  (SELECT
     articles.author,
     sum(t.num) AS total_views
   FROM
     authors,
     articles,
     (SELECT
        path,
        count(*) AS num
      FROM log
      WHERE path != '/'
      GROUP BY path) AS t
   WHERE articles.slug = substring(t.path FROM 10)
   GROUP BY articles.author) AS author_views
WHERE author_views.author = authors.id
ORDER BY total_views DESC;
```

### 3. On which days did more than 1% of requests lead to errors?
```
SELECT
  date,
  ((error_count :: FLOAT / total_count :: FLOAT) * 100) AS percentage
FROM
  (SELECT
     time :: DATE         AS date,
     count(CASE WHEN status = '200 OK'
       THEN 1
           ELSE NULL END) AS success_count,
     count(CASE WHEN status != '200 OK'
       THEN 1
           ELSE NULL END) AS error_count,
     count(*)             AS total_count
   FROM log
   GROUP BY time :: DATE) AS error_summary
WHERE ((error_count :: FLOAT / total_count :: FLOAT) * 100) > 1
ORDER BY percentage DESC
```