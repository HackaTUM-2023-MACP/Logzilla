import argparse

import tqdm
import torch
from transformers import AutoTokenizer, AutoModel
import psycopg2

from log_parser import parse_log

def embed_message(msg, model_name):
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name)

    inputs = tokenizer(msg, padding=True, truncation=True, return_tensors="pt")
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().tolist()

    return embeddings

# TODO (matoototo): Look into different embedding models
def insert_log_entries(user, password, host, port, log_entries, model_name="bert-base-uncased"):
    conn = psycopg2.connect(user=user, password=password, host=host, port=port)
    cur = conn.cursor()

    # TODO (matoototo): Batch embedding calls if necessary
    for log_entry in tqdm.tqdm(log_entries):
        embeddings = embed_message(log_entry.message, model_name)

        cur.execute("""
            INSERT INTO log_entries (timestamp, machine, layer, message, message_vector)
            VALUES (%s, %s, %s, %s, %s);
        """, (log_entry.timestamp, log_entry.machine, log_entry.layer, log_entry.message, embeddings))

        conn.commit()

    conn.commit()
    cur.close()
    conn.close()
    print("All log entries inserted successfully.")

def main():
    parser = argparse.ArgumentParser(description="Parse log data and insert into a PostgreSQL database.")
    parser.add_argument('logfile', type=argparse.FileType('r'), help="Log file to parse")
    parser.add_argument("--user", required=True, help="The username for the database.")
    parser.add_argument("--password", required=True, help="The password for the database.")
    parser.add_argument("--host", default="localhost", help="The host of the database.")
    parser.add_argument("--port", default="5432", help="The port of the database.")

    args = parser.parse_args()

    # Read and parse the log file
    log_data = args.logfile.read()
    parsed_entries = parse_log(log_data)

    # Insert the parsed log entries into the database
    insert_log_entries(args.user, args.password, args.host, args.port, parsed_entries)

if __name__ == '__main__':
    main()
