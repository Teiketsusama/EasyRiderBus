"""
Stage 3/6: Bus line info
Objectives:
The string containing the data in JSON format is passed to standard input.
Find the names of all the bus lines.
Verify the number of stops for each line.
The output should have the same formatting as shown in the example.
"""

from json import loads
from re import fullmatch


class EasyRiderDataChecker:
    data_structure = {
        "bus_id": {"type": int, "format": r"\d+"},
        "stop_id": {"type": int, "format": r"\d+"},
        "stop_name": {"type": str, "format": r"[A-Z][a-zA-Z\s]+\s(?:Road|Avenue|Boulevard|Street)"},
        "next_stop": {"type": int, "format": r"\d+"},
        "stop_type": {"type": str, "format": r"[SOF\s]?"},  # S, O, F
        "a_time": {"type": str, "format": r"\b(?:[01]\d|2[0-3]):[0-5]\d\b"},  # HH:MM
    }

    errors = dict.fromkeys(data_structure.keys(), 0)

    def __init__(self, data: str):
        self.data = loads(data)

    def check_data(self):
        for bus in self.data:
            for key, value in bus.items():
                if not isinstance(value, self.data_structure[key]["type"]) or \
                        not fullmatch(self.data_structure[key]["format"], str(value)):
                    self.errors[key] += 1


def bus_line_info(data: list):
    print("Line names and number of stops:")
    bus_ids = set(bus["bus_id"] for bus in data)
    for bus_id in bus_ids:
        print(f"bus_id: {bus_id}, stops: {sum(bus['bus_id'] == bus_id for bus in data)}")


def main():
    bus_line_info(EasyRiderDataChecker(input()).data)


if __name__ == '__main__':
    main()
