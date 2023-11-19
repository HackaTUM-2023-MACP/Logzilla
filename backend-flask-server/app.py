import os
import time
from dotenv import load_dotenv
from db import DatabaseConnection
from flask import Flask, send_file, request, jsonify, g
from query_generator import ChatAssistant

from db import insert_log_data, parse_log

load_dotenv()

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


# TODO: Maybe refactor this into a pool?
def create_db_connection():
    """ Factory function to create a database connection."""
    return DatabaseConnection(
        password=os.environ['DB_PASSWORD'],
        user=os.environ.get('DB_USER', 'postgres'),
        host=os.environ.get('DB_HOST', 'localhost'),
        port=os.environ.get('DB_PORT', '5432'),
        dbname=os.environ.get('DB_NAME', 'postgres')
    )

@app.before_request
def before_request():
    """Open a database connection before each request."""
    g.db = create_db_connection()
    OPENAI_KEY = os.environ.get('OPENAI_KEY')
    g.chat_assistant = ChatAssistant(OPENAI_KEY)

@app.route('/')
def index():
    return 'Hello, Flask!'


# It is good practice to have the API routes namespaced, so that they do not get mixed
# with any possible routes used by the React side. E.g. "/api/time" instead of "/time".
@app.route('/api/time')
def get_current_time():
    return {'time': time.time()}


@app.route('/api/summary', methods=['POST'])
def update_summary():
    if request.method == 'POST':
        data = request.get_json()
        current_summary = data.get('currentSummary')
        top_k_log_refs = data.get('topKLogRefs') # best k log rows (list of strings)

        chat_assistant = ChatAssistant(os.environ.get('OPENAI_KEY'))

        # TODO: Pass the current_summary and update_message to the model, which re-queries the database and returns an updated summary
        if current_summary.strip() == "":
            reference_rows = g.db.random_n(10)
            updated_summary = chat_assistant.generate_initial_summary(reference_rows)
            # print(updated_summary)
        
            return {'updatedSummary': updated_summary}
        else:
            return {'updatedSummary': current_summary}


@app.route('/api/get_context', methods=['POST'])
def get_context():
    if request.method == 'POST':
        request_data = request.get_json()
        line_number = request_data['line_number']
        context = g.db.get_context(line_number)
        return {'context': context}

@app.route('/api/response', methods=['POST'])
def get_chat_response():
    
    start_time = time.time()
    print("[get_chat_response] Request received.")

    try:
        data = request.json
        user_msgs = data.get('userMessages', [])  
        bot_msgs = data.get('botMessages', [])  
        summary = data.get('summary', '')  
        
        sql_str, reference_str, response_str = g.chat_assistant.user_msg_to_sql_and_reference_and_response(user_msgs, bot_msgs)
        if not all([sql_str, reference_str, response_str]):
            print("[get_chat_response] Error: SQL, reference, or response string is empty.")
            response_str = "Sorry, this was not specific enough. Please ask a question about the system log you uploaded."
            return jsonify({'botResponse': response_str, 'filteredRows': [], 'summary': summary})
        print(f"[get_chat_response] SQL: {sql_str} | Reference: {reference_str} | Response: {response_str}")
        
        # If the SQL filter includes a WHERE clause, remove it and everything before.
        if "WHERE" in sql_str:
            sql_str = sql_str[sql_str.index("WHERE") + 6:]
        
        # List of tuples (row number, datetime.datetime, network, layer, msg, score)
        filtered_rows = g.db.query_with_reference(reference_str, top_k=5)
        print(f"[get_chat_response] DB Query successful (len(filtered_rows)={len(filtered_rows)}).")
            
        filtered_rows = [{
            'rowNo': row[0],
            'datetime': row[1].strftime("%Y-%m-%d %H:%M:%S"),
            'network': row[2],
            'layer': row[3],
            'msg': row[4],
            'score': row[5]
        } for row in filtered_rows]
        
        updated_summary = g.chat_assistant.update_summary(filtered_rows, summary)
        
        print(f"[get_chat_response] Request completed in {time.time() - start_time} seconds.")

        return jsonify({'botResponse': response_str, 'filteredRows': filtered_rows, 'summary': updated_summary})
    except Exception as e:
        return {'error': str(e)}

def write_and_readfile(file):
    time_prefix = str(time.time()).replace('.', '')
    filename = os.path.join(app.config['UPLOAD_FOLDER'], f"{time_prefix}_{file.filename}")
    file.save(filename)

    with open(filename, 'r') as logfile:
        log_data = logfile.read()

    os.remove(filename)
    return log_data


@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files.get('file')
        whitelist = request.form.getlist('whitelist')
        blacklist = request.form.getlist('blacklist')

        if whitelist == []: whitelist = None
        else:
            whitelist = [l for l in whitelist[0].split(',') if l != '']
        if blacklist == []: blacklist = None

        print(f"Whitelist: {whitelist}, Blacklist: {blacklist}")
        
        if file:
            log_data = write_and_readfile(file)
            insert_log_data(g.db, log_data, whitelist=whitelist, blacklist=blacklist)
            return jsonify(message='File uploaded and log entries inserted successfully', success=True, filename=file.filename)
        else:
            return jsonify(message='No file was uploaded', success=False), 400
        
    except Exception as e:
        print("Error:", e)
        return jsonify(error=str(e)), 500

@app.route('/api/layers', methods=['POST'])
def get_log_layers():
    try:
        file = request.files['file']
        if file:
            log_data = write_and_readfile(file)
            parsed_entries = parse_log(log_data)
            layers = list(set(entry.layer for entry in parsed_entries))
            return jsonify(layers=layers), 200
        else:
            return jsonify(error="No file was uploaded"), 400
    except Exception as e:
        print("Error:", e)
        return jsonify(error=str(e)), 500



if __name__ == '__main__':
    app.run(debug=True, port=4000, threaded=False)

