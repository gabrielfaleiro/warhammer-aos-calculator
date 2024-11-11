import json
from libs.warscroll import WarScroll
from libs.army import Army


class SpreadsheetWarscroll:
    def __init__(self, filename):
        self.filename = filename
        self.header = ""

    def init_file(self):
        dummy_ws_filepath = './data/base/dummy_warscroll.json'
        with open(dummy_ws_filepath, 'r') as json_file:
            ws = WarScroll(json.load(json_file))
        ws.do_calculations()

        # Get keys from calculations
        keys = list(ws.calculations.keys())
        calculations = ','.join(keys)
        self.header = f"name_en,points,{calculations}"

        try:
            with open(self.filename, 'x') as output_file:
                output_file.write(f"{self.header}\n")
        except FileExistsError:
            with open(self.filename, 'w') as output_file:
                output_file.write(f"{self.header}\n")

    def append_ws(self, json_ws):
        ws = WarScroll(json_ws)
        # Base calculations
        ws.do_calculations()
        base_calcs = ws.calculations

        data = f"{ws.get('name_en')},{ws.get('characteristics.points')}"
        for key in self.header.split(','):
            if key == 'name_en' or key == 'points':
                continue
            else:
                data += f",{base_calcs[key]}"

        with open(self.filename, 'a') as output_file:
            output_file.write(f"{data}\n")


class SpreadsheetArmies:
    def __init__(self, filename):
        self.filename = filename
        self.header = ""

    def init_file(self):
        dummy_ws_filepath = './data/base/dummy_warscroll.json'
        with open(dummy_ws_filepath, 'r') as json_file:
            ws = WarScroll(json.load(json_file))
        ws.do_calculations()

        # Get keys from calculations
        keys = list(ws.calculations.keys())
        calculations = ','.join(keys)
        self.header = f"name,points,{calculations}"

        try:
            with open(self.filename, 'x') as output_file:
                output_file.write(f"{self.header}\n")
        except FileExistsError:
            with open(self.filename, 'w') as output_file:
                output_file.write(f"{self.header}\n")

    def append_army(self, json_army):
        army = Army(json_army)
        # Base calculations
        army.do_calculations()
        base_calcs = army.calculations

        data = f"{army.get('name')},{army.points}"
        for key in self.header.split(','):
            if key == 'name' or key == 'points':
                continue
            else:
                data += f",{base_calcs[key]}"

        with open(self.filename, 'a') as output_file:
            output_file.write(f"{data}\n")