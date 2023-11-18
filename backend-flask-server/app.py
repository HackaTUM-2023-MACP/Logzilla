import os
import time
from dotenv import load_dotenv
from db import DatabaseConnection
from flask import Flask, send_file, request, jsonify, g

from db import insert_log_data

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
        request_data = request.get_json()
        current_summary = request_data['current_summary']
        update_message = request_data['update_message']

        # TODO: Pass the current_summary and update_message to the model, which re-queries the database and returns an updated summary
        updated_summary = current_summary  # Replace with actual update logic

        return {'updated_summary': updated_summary}

@app.route('/api/get_context', methods=['POST'])
def get_context():
    if request.method == 'POST':
        request_data = request.get_json()
        line_number = request_data['line_number']
        context = g.db.get_context(line_number)
        return {'context': context}
        


@app.route('/api/response', methods=['POST'])
def get_chat_response():
    try:
        data = request.json
        user_msgs = data.get('userMessages', [])  
        bot_msgs = data.get('botMessages', [])  

        bot_msgs.append('This is a test message from the backend server.')

        return {'botMessages': bot_msgs, 'userMessages': user_msgs}
    except Exception as e:
        return {'error': str(e)}


@app.route('/api/upload', methods=['POST'])
def upload_file():
    try:
        file = request.files['file']
        if file:
            time_prefix = str(time.time()).replace('.', '')
            filename = os.path.join(app.config['UPLOAD_FOLDER'], f"{time_prefix}_{file.filename}")
            file.save(filename)

            with open(filename, 'r') as logfile:
                log_data = logfile.read()
            
            insert_log_data(g.db, log_data)
            os.remove(filename)
            return {'message': 'File uploaded and log entries inserted successfully', 'success': True, 'filename': file.filename}
        else:
            print('No file was uploaded')
            return {'message': 'No file was uploaded', 'success': False}
        
    except Exception as e:
        print(f'Error uploading file: {e}')
        return {'error': str(e)}


if __name__ == '__main__':
    app.run(debug=True)

