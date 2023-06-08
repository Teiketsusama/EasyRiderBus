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

    def arrival_time_info(self):
        print("Arrival time test:")
        bus_lines = set(bus["bus_id"] for bus in self.data)
        wrong_time_stops = {}
        for bus_line in bus_lines:
            stops = [bus for bus in self.data if bus["bus_id"] == bus_line]
            for i in range(len(stops) - 1):
                current_stop = stops[i]
                next_stop = stops[i + 1]
                if next_stop["a_time"] <= current_stop["a_time"]:
                    wrong_time_stops[bus_line] = next_stop["stop_name"]
                    break

        if wrong_time_stops.values():
            for bus_line, stop_name in wrong_time_stops.items():
                print(f"bus_id line {bus_line}: wrong time on station {stop_name}")
        else:
            print("OK")

    def on_demand_stops(self):
        start_stops = set(bus["stop_name"] for bus in self.data if bus["stop_type"] == "S")
        final_stops = set(bus["stop_name"] for bus in self.data if bus["stop_type"] == "F")
        stop_names = [bus["stop_name"] for bus in self.data]
        transfer_stops = set(stop_name for stop_name in stop_names if stop_names.count(stop_name) > 1)
        print("On demand stops test:")
        on_demand_stops = [bus["stop_name"] for bus in self.data if bus["stop_type"] == "O"]
        if on_demand_stops:
            wrong_stops = [stop for stop in on_demand_stops
                           if stop in start_stops or stop in final_stops or stop in transfer_stops]
            if wrong_stops:
                print(f"Wrong stop type: {sorted(wrong_stops)}")
            else:
                print("OK")


def main():
    data = input()
    checker = EasyRiderDataChecker(data)
    checker.on_demand_stops()


if __name__ == '__main__':
    main()
