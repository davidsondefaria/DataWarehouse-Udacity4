import configparser
import psycopg2
from sql_queries import copy_table_queries, insert_table_queries
from time import time


def load_staging_tables(cur, conn):
    """
        Run querys to load staging tables.
        
        Iterate over a list of staging table load queries to execute and commit to.
        
        Parameters:
        Argument1: Cursor to connect to database
        Argument2: Connection to data
    """
    for query in copy_table_queries:
        print("-----------------------------------------\n \
                Query running:\n {}".format(query))
        t0 = time()
        cur.execute(query)
        conn.commit()
        loadTime = time()-t0
        print("\nDone in: {0:.2f} sec\n".format(loadTime))


def insert_tables(cur, conn):
    """
        Run querys to create tables.
        
        Iterate over a list of insert table queries to execute and commit to.
        
        Parameters:
        Argument1: Cursor to connect to database
        Argument2: Connection to data
    """
    for query in insert_table_queries:
        print("-----------------------------------------\n \
                Query running:\n {}".format(query))
        t0 = time()
        cur.execute(query)
        conn.commit()
        loadTime = time()-t0
        print("\nDone in: {0:.2f} sec\n".format(loadTime))


def main():
    """
        Main function that manages the ETL process.
        
        Connect to Redshift cluster database and inserts data from S3 storage.
    """
    config = configparser.ConfigParser()
    config.read('dwh.cfg')

    conn = psycopg2.connect("host={} dbname={} user={} password={} port={}".format(*config['CLUSTER'].values()))
    cur = conn.cursor()
    
    load_staging_tables(cur, conn)
    insert_tables(cur, conn)

    conn.close()


if __name__ == "__main__":
    main()