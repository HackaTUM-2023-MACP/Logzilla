import argparse
import re
from datetime import datetime
from typing import NamedTuple, List

class LogEntry(NamedTuple):
    line_number: int
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
    current_datetime = datetime.now()  # Get the current datetime

    # Split the log data into lines
    for line_number, line in enumerate(log_data.strip().split('\n')):
        match = log_pattern.match(line)
        if match:
            # Parse the timestamp without the year (the logs don't have it)
            timestamp_str = match.group('timestamp')
            timestamp = datetime.strptime(timestamp_str, '%b %d %H:%M:%S')

            # Assign the current year or the previous year based on the current date
            year = current_datetime.year if timestamp.replace(year=current_datetime.year) <= current_datetime else current_datetime.year - 1
            timestamp = timestamp.replace(year=year)

            entry = LogEntry(
                line_number=line_number + 1,
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
