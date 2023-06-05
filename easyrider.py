"""
Stage 1/6: Checking the data type
Objectives:
The string containing the data in JSON format is passed to standard input.
Check that the data types match.
Check that the required fields are filled in.
Display the information about the number of found errors in total and in each field.
Keep in mind that there might be no errors at all.
The output should have the same formatting as shown in the example.
"""

from json import loads
from re import fullmatch


class EasyRiderDataChecker:
    data_structure = {
        "bus_id": {"type": int, "format": r"\d+"},
        "stop_id": {"type": int, "format": r"\d+"},
        "stop_name": {"type": str, "format": r"[\w\s\.]+"},
        "next_stop": {"type": int, "format": r"\d+"},
        "stop_type": {"type": str, "format": r"[SOF/s]?"},  # S, O, F
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


def main():
    data = input()
    checker = EasyRiderDataChecker(data)
    checker.check_data()
    print(f"Type and required field validation: {sum(checker.errors.values())} errors")
    for key, value in checker.errors.items():
        print(f"{key}: {value}")


if __name__ == '__main__':
    main()
