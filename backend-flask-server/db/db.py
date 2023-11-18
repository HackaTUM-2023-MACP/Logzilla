import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

class DatabaseConnection:
    """Schema:
        line_number SERIAL PRIMARY KEY,
        timestamp TIMESTAMP,
        machine VARCHAR(255),
        layer VARCHAR(255),
        message TEXT,
        message_vector vector(768)
    """
    def __init__(self, password, user="postgres", host='localhost', port='5432', dbname='postgres'):
        self.user = user
        self.password = password
        self.host = host
        self.port = port
        self.dbname = dbname
        self.conn = None
        self.connect()

    def connect(self):
        self.conn = psycopg2.connect(
            dbname=self.dbname,
            user=self.user,
            password=self.password,
            host=self.host,
            port=self.port
        )
        self.conn.set_isolation_level(ISOLATION_LEVEL_AUTOCOMMIT)

    # TODO (matoototo): maybe constrain to filtering by timestamp, machine, layer, etc and ordering by message similarity
    def run_sql(self, sql):
        with self.conn.cursor() as cur:
            cur.execute(sql)
            # Attempt to fetchall only if the cursor has results to fetch
            if cur.description:
                return cur.fetchall()
            return None
        
    # TODO: Currently returns everything, but we probably don't need the embedding vector on the frontend, so maybe remove?
    def get_context(self, target_line_number, num_rows=10):
        """Returns the surrounding window of rows from the database"""
        with self.conn.cursor() as cur:
            cur.execute(
                f"""
                SELECT * FROM log_entries
                WHERE line_number >= {target_line_number - num_rows // 2}
                AND line_number <= {target_line_number + num_rows // 2}
                ORDER BY line_number ASC;
                """
            )
            return cur.fetchall()

    def __enter__(self):
        return self

    def __exit__(self, exc_type, exc_val, exc_tb):
        if self.conn:
            self.conn.close()

import argparse

def main():
    # Set up argparse
    parser = argparse.ArgumentParser(description="Run SQL commands on a PostgreSQL database.")
    parser.add_argument("--user", default="postgres", help="The username for the database.")
    parser.add_argument("--password", required=True, help="The password for the database.")
    parser.add_argument("--host", default="localhost", help="The host of the database.")
    parser.add_argument("--port", default="5432", help="The port of the database.")
    parser.add_argument("--dbname", default="postgres", help="The name of the database.")
    parser.add_argument("--sql", default="SELECT * FROM log_entries LIMIT 10;", help="The SQL command to run.")
    args = parser.parse_args()

    with DatabaseConnection(args.password, args.user, args.host, args.port, args.dbname) as db:
        result = db.run_sql(args.sql)
        if result:
            for row in result:
                print(row)
        else:
            print("SQL command executed successfully, no output to display.")

if __name__ == "__main__":
    main()
