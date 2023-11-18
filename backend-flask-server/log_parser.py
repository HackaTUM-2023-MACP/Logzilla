import argparse
import re
from datetime import datetime
from typing import NamedTuple, List

class LogEntry(NamedTuple):
    timestamp: datetime
    machine: str
    layer: str
    message: str

def parse_log(log_data: str) -> List[LogEntry]:
    # Regex pattern for matching the log entry format
    log_pattern = re.compile(
        r'(?P<timestamp>\w+ \d+ \d+:\d+:\d+) '  # Date and time
        r'(?P<machine>\S+) '                    # Machine name
        r'(?P<layer>\S+): '                     # Layer
        r'(?P<message>.*)'                      # Message
    )

    entries = []

    # Split the log data into lines
    for line in log_data.strip().split('\n'):
        match = log_pattern.match(line)
        if match:
            # Convert the timestamp to a datetime object
            timestamp_str = match.group('timestamp')
            timestamp = datetime.strptime(timestamp_str, '%b %d %H:%M:%S')

            # Create a LogEntry namedtuple from the regex groups
            entry = LogEntry(
                timestamp=timestamp,
                machine=match.group('machine'),
                layer=match.group('layer'),
                message=match.group('message')
            )
            entries.append(entry)

    return entries

def main():
    parser = argparse.ArgumentParser(description="Parse log data and print to stdout.")
    parser.add_argument('logfile', type=argparse.FileType('r'), help="Log file to parse")
    args = parser.parse_args()

    log_data = args.logfile.read()

    parsed_entries = parse_log(log_data)

    for entry in parsed_entries:
        print(entry)

if __name__ == '__main__':
    main()
