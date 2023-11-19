import openai
from itertools import zip_longest
import json


class ChatAssistant:
    def __init__(self, api_key):
        self.api_key = api_key
        openai.api_key = api_key
        

    def user_msg_to_sql_and_reference_and_response(self, usr_msg_list, bot_msg_list):
        """
        Run inference on a list of user messages and bot messages to generate a SQL query, 
        a reference message, and a response message.
        """
        try:
            conversation_prompt = [{
                "role": "system",
                "content": """
                    You are a helpful system administrator and you are chatting with a user that wants to analyze a system log file. For example, the user might want to see all SSH login attempts from the last 24 hours. 
                    
                    Your answer must be exactly in the following format and contain nothing else: {"sql_query": <SQL QUERY FILTER COMMAND>, "reference_entry": <REFERENCE MESSAGE IN THE LOG FILE>, "chat_response": <CHAT RESPONSE TO THE USER>}
                    
                    Use fuzzy matching in the sql_query. Available columns: timestamp TIMESTAMP, machine VARCHAR(255), layer VARCHAR(255), message TEXT, message_vector vector(768)
                    
                    The reference_entry should be an example message from the log file that the user may look for based on his questions.
                    
                    The chat_response should inform the user about what to look for in the log file based on his questions.
                """
            }]
            
            # Alternatingly add user and bot messages to the conversation, starting with the bot.
            for usr_msg, bot_msg in zip_longest(usr_msg_list, bot_msg_list):
                if bot_msg:
                    conversation_prompt.append({"role": "assistant", "content": bot_msg})
                if usr_msg:
                    conversation_prompt.append({"role": "user", "content": usr_msg})

            client = openai.OpenAI(api_key=self.api_key)
            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages=conversation_prompt
            )
            
            result_json = response.choices[0].message.content
            result_dict = json.loads(result_json)

            return (
                result_dict.get("sql_query"),
                result_dict.get("reference_entry"),
                result_dict.get("chat_response")
            )
        except Exception as e:
            print("ERROR in user_msg_to_sql_and_reference_and_response:", e)
            return "", "", ""


    def generate_sql_query(self, user_content_list, assistant_content_list):
        conversation_sql_query = [{"role": "system", "content": "You are only allowed to reply with an SQL query. For filtering, only use fuzzy matching and never include the message in the query. The database table has the following columns: timestamp TIMESTAMP, machine VARCHAR(255), layer VARCHAR(255), message TEXT, message_vector vector(768). "}]
        
        for i in range(max(len(user_content_list), len(assistant_content_list))):
            if i < len(user_content_list):
                
                conversation_sql_query.append({"role": "user", "content": user_content_list[i]})
                
            if i < len(assistant_content_list):
                
                conversation_sql_query.append({"role": "assistant", "content": assistant_content_list[i]})
        
        completion = openai.chat.Completion.create(
            model="gpt-3.5-turbo", 
            messages=conversation_sql_query
        )
        message_string = completion['choices'][0]['message']['content']
    
        return message_string

    def generate_reference_message(self, user_content_list, assistant_content_list):
        conversation_reference_message = [{"role": "system", "content": "Please reply only with a possible message that we should look for in a system logfile to find the answers to the user's prompt."}]

        for i in range(max(len(user_content_list), len(assistant_content_list))):
            if i < len(user_content_list):
                
                conversation_reference_message.append({"role": "user", "content": user_content_list[i]})
            if i < len(assistant_content_list):
                
                conversation_reference_message.append({"role": "assistant", "content": assistant_content_list[i]})
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=conversation_reference_message
        )
        message_string = completion['choices'][0]['message']['content']
    
        return message_string

    def generate_chat_response(self, user_content_list, assistant_content_list):     # also consider summary as an input here (maybe system input?)
        
        
        conversation_chat_response = [{"role": "system", "content": ""}]
        
        for i in range(max(len(user_content_list), len(assistant_content_list))):
            if i < len(user_content_list):
               
                conversation_chat_response.append({"role": "user", "content": user_content_list[i]})
                
            if i < len(assistant_content_list):
                
                conversation_chat_response.append({"role": "assistant", "content": assistant_content_list[i]})
                
        
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=conversation_chat_response
        )
        message_string = completion['choices'][0]['message']['content']
    
        return message_string

    def update_summary(self, user_content_list, assistant_content_list, current_summary, new_query_results):
        
        summary_update_input = current_summary + "Use the following new query results and conversation with the user to update the above mentioned summary and also reference them in the new summary" + new_query_results
        conversation_summary_update = [{"role": "system", "content": summary_update_input}]
        
        for i in range(max(len(user_content_list), len(assistant_content_list))):
            if i < len(user_content_list):
                conversation_summary_update.append({"role": "user", "content": user_content_list[i]})
                
            if i < len(assistant_content_list):
                conversation_summary_update.append({"role": "assistant", "content": assistant_content_list[i]})
                
        
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo", 
            messages=conversation_summary_update
        )
        message_string = completion['choices'][0]['message']['content']
    
        return message_string


if __name__ == "__main__":
    # Example usage:
    api_key = "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"
    chat_assistant = ChatAssistant(api_key)

    # Combine messages to conversation context
    user_messages = ["Are there any ssh errors in the last 24 hours?", "sorry, I meant the last 48 hours"]
    assistant_messages = ["okay will do", "okay will do"]
    current_summary = [""]
    new_query_results = [""]

    # Function 1
    # result_function1 = chat_assistant.generate_chat_response(user_messages, assistant_messages)
    # print(result_function1)
    
    crt_summary = """
An unexpected error occurred while executing a critical process. The system suggests checking input parameters and ensuring the integrity of database connections.
<myref rowNo="22" rowScore="0.32" rowText="Critical: Application crashed unexpectedly" rowContext="Investigate crash logs #DELIMITER#Review recent code changes"></myref>
        """
        
    new_query_results = "Error on the moon. another error on the sun."
        
    summary = chat_assistant.update_summary(user_messages, assistant_messages, crt_summary, new_query_results)
    
    print(summary)

    # # Function 2
    # result_function2 = chat_assistant.generate_reference_message(conversation_reference_message)
    # print(result_function2)
