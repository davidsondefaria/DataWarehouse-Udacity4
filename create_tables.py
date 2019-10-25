import configparser
import psycopg2
from sql_queries import create_table_queries, drop_table_queries


def drop_tables(cur, conn):
    """
        Run querys to drop tables.
        
        Iterate over a list of table drop queries to execute and commit to.
        
        Parameters:
        Argument1: Cursor to connect to database
        Argument2: Connection to data
    """
    for query in drop_table_queries:
        cur.execute(query)
        conn.commit()


def create_tables(cur, conn):
    """
        Run querys to create tables.
        
        Iterate over a list of table creation queries to execute and commit to.
        
        Parameters:
        Argument1: Cursor to connect to database
        Argument2: Connection to data
    """
    for query in create_table_queries:
        cur.execute(query)
        conn.commit()


def main():
    """
        Main function that manages the tables creation.
        
        Reads database configuration hosted in cluster to connect and create tables schema.
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()

    drop_tables(cur, conn)
    create_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()