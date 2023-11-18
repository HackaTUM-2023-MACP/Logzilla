import argparse
import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

def create_db_and_table(user: str, password: str, host: str = 'localhost', port: str = '5432'):
    # Connect to PostgreSQL server
    conn = psycopg2.connect(dbname='postgres', user=user, password=password, host=host, port=port)
    conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)
    cur = conn.cursor()

    cur.execute("CREATE EXTENSION IF NOT EXISTS vector;")

    # Create table with an additional column for vector embedding
    cur.execute("""
        CREATE TABLE log_entries (
            line_number SERIAL PRIMARY KEY,
            timestamp TIMESTAMP,
            machine VARCHAR(255),
            layer VARCHAR(255),
            message TEXT,
            message_vector vector(768)  -- Assuming 768 dimensions for vector, varies by embedding model
        );
    """)
    print("Table 'log_entries' created successfully")

    # Close cursor and connection
    cur.close()
    conn.close()

if __name__ == "__main__":
    # Set up argparse
    parser = argparse.ArgumentParser(description="Set up the PostgreSQL database and table for log entries.")
    parser.add_argument("--user", required=True, help="The username for the database.")
    parser.add_argument("--password", required=True, help="The password for the database.")
    parser.add_argument("--host", default="localhost", help="The host of the database.")
    parser.add_argument("--port", default="5432", help="The port of the database.")

    args = parser.parse_args()

    # Create the database and table
    create_db_and_table(args.user, args.password, args.host, args.port)
