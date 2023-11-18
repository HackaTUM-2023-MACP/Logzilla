from pathlib import Path

dir_path = Path("/home/hackathon14/Logzilla/demo-langchain/logs")

file_name =  "test_log.out"
file_path = Path(dir_path, file_name)
write_path = Path(dir_path, "cleaned_" + file_name)

words_to_keep = [
    "ssh",
    # "fail",
    # "success",
    # "enable",
    # "error",
]

lines = []
prev_line = None

with open(file_path, "r") as f:
    for line in f:
        for word in words_to_keep:
            if word in line:
                # Keep the previous line for extra context
                if prev_line is not None and prev_line not in lines:
                   lines.append(prev_line)

                # Add the current line
                lines.append(line)

                # Append line only once if the word we want is in there
                break
        prev_line = line

with open(write_path, "w") as f:
    for line in lines:
        f.write(line)

print(len(lines))

    

