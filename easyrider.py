"""
Stage 2/6: Correct syntax
Objectives:
The string containing the data in JSON format is passed to standard input.
Check that the data format complies with the documentation.
Only the fields that have such a requirement are relevant, i.e. stop_name, stop_type, a_time,
so, please, count errors only for them.
Like in the previous stage, print the information about the number of found errors in total and in each field.
Remember that there might be no errors at all.
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


def main():
    data = input()
    checker = EasyRiderDataChecker(data)
    checker.check_data()
    print(f"Format validation: {sum(checker.errors.values())} errors")
    for key, value in checker.errors.items():
        if key in ("stop_name", "stop_type", "a_time"):
            print(f"{key}: {value}")


if __name__ == '__main__':
    main()
