import argparse

import tqdm
import torch
from transformers import AutoTokenizer, AutoModel

from log_parser import parse_log
from db import DatabaseConnection

def embed_message(msg, model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    inputs = tokenizer(msg, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().tolist()

    return embeddings

# TODO (matoototo): Look into different embedding models
def insert_log_entries(db_connection, log_entries, model_name="bert-base-uncased"):
    # TODO (matoototo): Batch embedding calls if necessary
    for log_entry in tqdm.tqdm(log_entries):
        embeddings = embed_message(log_entry.message, model_name)

        db_connection.run_sql(f"""
            INSERT INTO log_entries (line_number, timestamp, machine, layer, message, message_vector)
            VALUES (%s, %s, %s, %s, %s, %s);
        """, (log_entry.line_number, log_entry.timestamp, log_entry.machine, log_entry.layer, log_entry.message, embeddings))

        db_connection.commit()

    print("All log entries inserted successfully.")

def insert_log_data(db_connection, log_data, model_name="bert-base-uncased"):
    parsed_entries = parse_log(log_data)
    insert_log_entries(db_connection, parsed_entries, model_name)

def main():
    parser = argparse.ArgumentParser(description="Parse log data and insert into a PostgreSQL database.")
    parser.add_argument('logfile', type=argparse.FileType('r'), help="Log file to parse")
    parser.add_argument("--user", required=True, help="The username for the database.")
    parser.add_argument("--password", required=True, help="The password for the database.")
    parser.add_argument("--host", default="localhost", help="The host of the database.")
    parser.add_argument("--port", default="5432", help="The port of the database.")

    args = parser.parse_args()

    with DatabaseConnection(args.password, args.user, args.host, args.port) as db:
        insert_log_data(db, args.logfile.read())

if __name__ == '__main__':
    main()
