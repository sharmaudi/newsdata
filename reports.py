import click
import psycopg2

import news.config as config


@click.command()
@click.option('--report', type=click.Choice(["1",
                                             "2",
                                             "3"]), prompt='Report type',
              help='''Report type:
                        1 - Most Popular articles.
                        2 - Most Popular authors.
                        3 - Days on which more than 1% of requests lead to errors.  
                        ''')
def generate_report(report):
    """Program that generates reports on
     the usage patterns for the News database."""
    db = psycopg2.connect(database=config.database,
                          user=config.user,
                          password=config.password,
                          host=config.host)
    c = db.cursor()
    c.execute(config.queries[report])
    ret = c.fetchall()
    c.close()

    if report == '1' or report == '2':
        for row in ret:
            print(f"{row[0]} -- {row[1]} views")
    elif report == '3':
        for row in ret:
            print(f"{row[0]:%b %d, %Y} -- {row[1]:.2f}% errors")
    else:
        print("Report not found!")


if __name__ == '__main__':
    generate_report()
