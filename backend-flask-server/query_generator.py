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

    def _create_reference_message(self, reference_rows):
        reference_message = ""
        for row in reference_rows:
            # reference_message += f"[REF{row['line_number']}] {row['timestamp']} {row['machine']} {row['layer']}: {row['message']}\n"
            reference_message += f"[REF{row[0]}] {row[1]} {row[2]} {row[3]}: {row[4]}\n"
        return reference_message

    def replace_references(self, message, reference_rows):
        """
        Replace the reference format in the message from [REF1234] to <myref rowNo="1234" score="score_value" message="message_value"></myref>,
        utilizing the provided get_score and get_message functions.
        """
        import re
        import html

        # Define the replacement function to be used with re.sub
        def replace(match):
            row_no = match.group(1)
            reference_row = next((row for row in reference_rows if row[0] == int(row_no)), None)
            if reference_row is None:
                raise ValueError([row[0] for row in reference_rows], row_no)
            message_text = reference_row[4]
            score = 0.0
            # Escape HTML special characters in the message text
            message_text = html.escape(message_text)
            return f'<myref rowNo="{row_no}" rowScore="{score}" rowText="{message_text}" rowContext=" #DELIMITER# "></myref>'

        # Pattern to identify the references
        pattern = r'\[REF(\d+)\]'
        # Replace the pattern with the new format using the replace function
        new_message = re.sub(pattern, replace, message)
        return new_message

    def generate_initial_summary(self, reference_rows):
        # This code is for v1 of the openai package: pypi.org/project/openai
        client = openai.OpenAI(api_key=self.api_key)

        response = client.chat.completions.create(
            model="gpt-3.5-turbo-1106",
            messages=[
                {
                "role": "user",
                "content": "Please generate a summary of the following logs. Each log row has an associated reference number (denoted as [REF#] prefix) and a message. If a section of your summary is based on a specific row, you can include it at the end of the sentence but use that sparisngly. However, don't list a large number of references without much text. If multiple messages refer to the same thing, only reference one of them. For example:\n\n[REF530] Nov 10 05:49:37 localhost kernel: pci 0000:08:00.0: BAR 7: no space for [mem size 0x00800000 64bit pref] -> \"... In localhost at the kernel layer, a message indicates that there is a problem with allocating memory for a PCI (Peripheral Component Interconnect) device in the system.[REF530] ...\"\n\nHere are the rows. Please make a summary as requested:\n\n[REF530] Nov 10 05:49:37 localhost kernel: pci 0000:08:00.0: BAR 7: no space for [mem size 0x00800000 64bit pref]\n[REF2164] Nov 10 05:49:44 CMX50070-101776 xu_launcher[1978]: ERROR: Cannot create file \"FrontUnit_1500.log\": Permission denied\n[REF10833]  Nov 10 05:56:40 CMX50070-101776 sshd[50220]: error: kex_exchange_identification: Connection closed by remote host\n[REF14674] Nov 10 09:23:07 CMX50070-101776 start_cmxmarsserver.sh[386]: Got Data: 823400 count: 54 t: 9:23:07 AM\n[REF63692] Nov 13 10:47:31 CMX50070-101776 stop_cmxmarsserver.sh[315768]: Attempting to stop CMXmars Server version  1.120.11-1kirkstone..."
                },
                {
                "role": "assistant",
                "content": "The system kernel reports an issue with allocating memory for a PCI device at [REF530]. A permission denied error is encountered when trying to create a file \"FrontUnit_1500.log\" at [REF2164]. At [REF10833], a connection to an SSH server is closed by the remote host. Data is received and counted at [REF14674]. An attempt to stop CMXmars Server is made at [REF63692]."
                },
                {
                "role": "user",
                "content": f"Great, now do it again. Don't forget the references (VERY important). Do it for the following rows:\n\n{self._create_reference_message(reference_rows)}"
                }
            ],
            temperature=0,
            max_tokens=512,
            top_p=1,
            frequency_penalty=0,
            presence_penalty=0
        )
        
        initial_summary = response.choices[0].message.content
        replaced_summary = self.replace_references(initial_summary, reference_rows)

        return replaced_summary