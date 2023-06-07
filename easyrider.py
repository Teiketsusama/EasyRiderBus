"""
Stage 4/6: Special stops
Objectives:
The string containing the data in JSON format is passed to standard input.
Make sure each bus line has exactly one starting point (S) and one final stop (F).
If a bus line does not meet this condition, stop checking and print a message about it.
Do not continue checking the other bus lines.
If all bus lines meet the condition, count how many starting points and final stops there are.
Print their unique names in alphabetical order.
Count the transfer stops and print their unique names in alphabetical order.
A transfer stop is a stop shared by at least two bus lines.
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

    def bus_line_info(self):
        print("Line names and number of stops:")
        bus_lines = set(bus["bus_id"] for bus in self.data)
        for bus_line in bus_lines:
            print(f"bus_id: {bus_line}, stops: {sum(bus['bus_id'] == bus_line for bus in self.data)}")

    def special_stop_info(self):
        bus_lines = set(bus["bus_id"] for bus in self.data)
        for bus_line in bus_lines:
            stop_types = [bus["stop_type"] for bus in self.data if bus["bus_id"] == bus_line]
            if stop_types.count("S") != 1 or stop_types.count("F") != 1:
                print(f"There is no start or end stop for the line: {bus_line}.")
                return

        start_stops = set(bus["stop_name"] for bus in self.data if bus["stop_type"] == "S")
        final_stops = set(bus["stop_name"] for bus in self.data if bus["stop_type"] == "F")
        stop_names = [bus["stop_name"] for bus in self.data]
        transfer_stops = set(stop_name for stop_name in stop_names if stop_names.count(stop_name) > 1)
        print(f"Start stops: {len(start_stops)} {sorted(list(start_stops))}")
        print(f"Transfer stops: {len(transfer_stops)} {sorted(list(transfer_stops))}")
        print(f"Finish stops: {len(final_stops)} {sorted(list(final_stops))}")


def main():
    data = input()
    checker = EasyRiderDataChecker(data)
    checker.special_stop_info()


if __name__ == '__main__':
    main()
