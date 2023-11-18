import argparse

import tqdm
import torch
from transformers import AutoTokenizer, AutoModel

from .log_parser import parse_log
from .db import DatabaseConnection

def embed_message(msg, model_name):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name).to(device)

    inputs = tokenizer(msg, padding=True, truncation=True, return_tensors="pt").to(device)
    with torch.no_grad():
        outputs = model(**inputs)
    embeddings = outputs.last_hidden_state.mean(dim=1).squeeze().tolist()

    return embeddings

def wipe_log_entries(db_connection):
    db_connection.run_sql("DELETE FROM log_entries;")
    db_connection.commit()

def batch_insert_log_entries(db_connection, log_entries, model_name="bert-base-uncased", batch_size=32):
    device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
    tokenizer = AutoTokenizer.from_pretrained(model_name)
    model = AutoModel.from_pretrained(model_name).to(device)
    
    for i in tqdm.tqdm(range(0, len(log_entries), batch_size)):
        batch_entries = log_entries[i:i+batch_size]
        batch_messages = [entry.message for entry in batch_entries]
        inputs = tokenizer(batch_messages, padding=True, truncation=True, return_tensors="pt").to(device)
        
        with torch.no_grad():
            outputs = model(**inputs)
        batch_embeddings = outputs.last_hidden_state.mean(dim=1)
        
        for entry, embedding in zip(batch_entries, batch_embeddings):
            db_connection.run_sql(f"""
                INSERT INTO log_entries (line_number, timestamp, machine, layer, message, message_vector)
                VALUES (%s, %s, %s, %s, %s, %s);
            """, (entry.line_number, entry.timestamp, entry.machine, entry.layer, entry.message, embedding.tolist()))
        
        db_connection.commit()

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

def insert_log_data(db_connection, log_data, model_name="bert-base-uncased", wipe=True):
    if wipe: wipe_log_entries(db_connection)
    parsed_entries = parse_log(log_data)
    batch_insert_log_entries(db_connection, parsed_entries, model_name)

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
