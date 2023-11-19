import psycopg2
from psycopg2.extensions import ISOLATION_LEVEL_AUTOCOMMIT

import torch
from transformers import AutoTokenizer, AutoModel


# Same thing as in backend-flask-server/db/populate_db.py but we gotta go fast... (cba to refactor)
def embed_message(msg, model_name="bert-base-uncased"):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name).to(device)

    inputs = tokenizer(msg, padding=True, truncation=True, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().tolist()

    return embeddings

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
    def run_sql(self, sql, params=None):
        with self.conn.cursor() as cur:
            cur.execute(sql, params)
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

    def commit(self):
        self.conn.commit()

    def query_with_reference(self, message, model_name="bert-base-uncased", top_k=10):
        # Embed the input message
        message_embedding = embed_message(message, model_name)
        message_embedding_str = ','.join([str(e) for e in message_embedding])

        # Perform a dot product similarity search
        sql = f"""
        SELECT line_number, timestamp, machine, layer, message, 1 - (message_vector <=> '[{message_embedding_str}]') AS similarity
        FROM log_entries
        ORDER BY 1 - (message_vector <=> '[{message_embedding_str}]') DESC
        LIMIT {top_k};
        """
        return self.run_sql(sql)
    
    def query_with_reference_and_sql(self, message, sql_str, model_name="bert-base-uncased", top_k=10):
        # Embed the input message
        message_embedding = embed_message(message, model_name)
        message_embedding_str = ','.join([str(e) for e in message_embedding])

        # Perform a dot product similarity search
        sql = f"""
        SELECT line_number, timestamp, machine, layer, message, 1 - (message_vector <=> '[{message_embedding_str}]') AS similarity
        FROM log_entries
        WHERE {sql_str}  -- Add the filtering condition here
        ORDER BY 1 - (message_vector <=> '[{message_embedding_str}]') DESC
        LIMIT {top_k};
        """
        return self.run_sql(sql)


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
        # print(db.query_with_reference("error: kex_exchange_identification: Connection closed by remote host"))
        print(db.query_with_reference_and_sql("BIOS-provided physical RAM map", "layer = 'kernel'"))
        # result = db.run_sql(args.sql)
        # if result:
        #     for row in result:
        #         print(row)
        # else:
        #     print("SQL command executed successfully, no output to display.")

if __name__ == "__main__":
    main()
