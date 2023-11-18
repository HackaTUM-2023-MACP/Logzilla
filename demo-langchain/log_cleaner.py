def filter_log_file(input_file_path, output_file_path, relevant_words):
    # Open input and output files
    with open(input_file_path, 'r', encoding='utf-8') as input_file, \
            open(output_file_path, 'w', encoding='utf-8') as output_file:
        # Iterate through each line in the input file
        for line in input_file:
            # Check if any of the relevant words are in the line (case-insensitive)
            if any(word.lower() in line.lower() for word in relevant_words):
                # Write the line to the output file
                output_file.write(line)

    print(f"Successfully edited the file. Output saved to {output_file_path}")

# Example usage:
input_file_path = '/mnt/c/Users/chwen/Desktop/Bewerbungen/Seminare, Challenges/2023-11 HackaTUM23/Logzilla/demo-langchain/logs/test_log1.out'
output_file_path = 'cleaned_test_log1.out'
relevant_words = ['error', 'ssh']  # Add more relevant words as needed. get them from the language model based on the request of the user!!!!

filter_log_file(input_file_path, output_file_path, relevant_words)
