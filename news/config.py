import os

# Database name for the news database
database = 'news'

# User name for the news database. This will be
# loaded from the environment variable NEWS_DB_USER.
# If the environment variable is not set, a default
# user vagrant will be used.
user = os.getenv("NEWS_DB_USER", "vagrant")


# Password for the news database. This will be
# loaded from the environment variable NEWS_DB_PASSWORD.
# If the environment variable is not set, a default
# value will be used.
password = os.getenv("NEWS_DB_PASSWORD", "Welcome123")


# Host name for the news database. This will be
# loaded from the environment variable NEWS_DB_HOST.
# If the environment variable is not set, a default
# value will be used.
host = os.getenv("NEWS_DB_HOST", "localhost")


# Dictionary containing Queries used in the reports.
# Contains the following queries
#  1 - Most Popular articles.
#  2 - Most Popular authors.
#  3 - Days on which more than 1% of requests lead to errors.

queries = {
    "1": """
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
    """,
    "2": """
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
    """,

    "3": """
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
    """
}
