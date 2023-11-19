import os
import time
from dotenv import load_dotenv
from db import DatabaseConnection
from flask import Flask, send_file, request, jsonify, g
from query_generator import ChatAssistant

import torch
import transformers
from transformers import AutoTokenizer, BitsAndBytesConfig, AutoModelForCausalLM
from langchain.llms import HuggingFacePipeline

from db import insert_log_data, parse_log, generate_summary

load_dotenv()

app = Flask(__name__)

UPLOAD_FOLDER = './uploads'
USE_MISTRAL = True # flag to whether use the 7b instruction tuned mistral model
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create hugging face model
if USE_MISTRAL == True:
    # Load model config to cache
    model_name='mistralai/Mistral-7B-Instruct-v0.1'

    model_config = transformers.AutoConfig.from_pretrained(
        model_name
    ) 

    # Initialize tokenizer
    tokenizer = AutoTokenizer.from_pretrained(model_name, trust_remote_code=True)
    tokenizer.pad_token = tokenizer.eos_token
    tokenizer.padding_side = "right"

    # Specify quantization config
    use_4bit = True

    # Compute dtype for 4-bit base models
    bnb_4bit_compute_dtype = "float16"

    # Quantization type (fp4 or nf4)
    bnb_4bit_quant_type = "nf4"

    # Activate nested quantization for 4-bit base models (double quantization)
    use_nested_quant = False

    compute_dtype = getattr(torch, bnb_4bit_compute_dtype)

    bnb_config = BitsAndBytesConfig(
        load_in_4bit=use_4bit,
        bnb_4bit_quant_type=bnb_4bit_quant_type,
        bnb_4bit_compute_dtype=compute_dtype,
        bnb_4bit_use_double_quant=use_nested_quant,
    )

    # Check GPU compatibility with bfloat16
    if compute_dtype == torch.float16 and use_4bit:
        major, _ = torch.cuda.get_device_capability()
        if major >= 8:
            print("=" * 80)
            print("Your GPU supports bfloat16: accelerate training with bf16=True")
            print("=" * 80) 

    # Load model
    model = AutoModelForCausalLM.from_pretrained(
        model_name,
        quantization_config=bnb_config,
    )

    # Initialize langchain LLM from hugging face pipeline 
    text_generation_pipeline = transformers.pipeline(
        model=model,
        tokenizer=tokenizer,
        task="text-generation",
        #temperature=0.2,
        repetition_penalty=1.1,
        return_full_text=True,
        max_new_tokens=300,
        #do_sample=True
    )

    # This is the object to pass to generate summaries (first you need MapReduceDocumentChain's)
    llm = HuggingFacePipeline(pipeline=text_generation_pipeline)



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
        data = request.get_json()
        current_summary = data.get('currentSummary')
        top_k_log_refs = data.get('topKLogRefs') # best k log rows (list of strings)

        api_key = "PUT API KEY KERE"
        chat_assistant = ChatAssistant(api_key)

        # TODO: Pass the current_summary and update_message to the model, which re-queries the database and returns an updated summary
        updated_summary = chat_assistant  # Replace with actual update logic
        
        # <myref rowNo="12" rowScore="0.24" rowText="This is a log row" rowContext=""/>
#         updated_summary = """
# An unexpected error occurred while executing a critical process. The system suggests checking input parameters and ensuring the integrity of database connections.
# <mycaption>My<mycaption/>
# A warning has been logged indicating that resource usage has surpassed the defined threshold. It is advised to inspect resource allocation and optimize code for improved efficiency.
# Positive feedback in the log reveals successful establishment of a database connection. The process involved initializing the connection pool and executing a query for data retrieval.
# A critical entry notifies that the application crashed unexpectedly. It is imperative to investigate crash logs and thoroughly review recent code changes for potential issues.
# The log records the completion of a system update. To ensure success, verify updated features and address any user-reported issues that may have surfaced.
#         """.strip()
        updated_summary = """
An unexpected error occurred while executing a critical process. The system suggests checking input parameters and ensuring the integrity of database connections.
<myref rowNo="22" rowScore="0.32" rowText="Critical: Application crashed unexpectedly" rowContext="Investigate crash logs #DELIMITER#Review recent code changes"></myref>
A warning has been logged indicating that resource usage has surpassed the defined threshold. It is advised to inspect resource allocation and optimize code for improved efficiency.
<myref rowNo="22" rowScore="0.32" rowText="Critical: Application crashed unexpectedly" rowContext="Investigate crash logs #DELIMITER#Review recent code changes"></myref>
Positive feedback in the log reveals successful establishment of a database connection. The process involved initializing the connection pool and executing a query for data retrieval.
<myref rowNo="31" rowScore="0.58" rowText="Critical: Application crashed unexpectedly" rowContext="Investigate crash logs #DELIMITER#Review recent code changes"></myref>
A critical entry notifies that the application crashed unexpectedly. It is imperative to investigate crash logs and thoroughly review recent code changes for potential issues.
<myref rowNo="42" rowScore="0.21" rowText="Information: System update completed" rowContext="Verify updated features #DELIMITER#Check for user-reported issues"></myref>
The log records the completion of a system update. To ensure success, verify updated features and address any user-reported issues that may have surfaced.
        """

        return {'updatedSummary': updated_summary}

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

        api_key = "PUT API KEY KERE"
        chat_assistant = ChatAssistant(api_key)
        conversation = chat_assistant.combine_messages(user_msgs, bot_msgs, [""], [""])
        
        sql_query = chat_assistant.generate_sql_query(conversation)
        reference_message = chat_assistant.generate_reference_message(conversation)

        bot_msgs.append('This is a test message from the backend server.')

        return {'botMessages': bot_msgs, 'userMessages': user_msgs}
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
        if blacklist == []: blacklist = None

        print(f"Whitelist: {whitelist}, Blacklist: {blacklist}")
        
        if file:
            log_data = write_and_readfile(file)
            insert_log_data(g.db, log_data, whitelist=whitelist, blacklist=blacklist)
            # TODO - @altay generate summary
            summary = generate_summary(log_data, llm, use_mistral=USE_MISTRAL)
            return jsonify(message='File uploaded and log entries inserted successfully', success=True, filename=file.filename, summary=summary)
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
        return jsonify(error=str(e)), 500



if __name__ == '__main__':
    app.run(debug=True)

