import json
import os
import logging
from libs.common import parse_characteristic
from libs.warscroll import WarScroll


class Army:
    def __init__(self, army_obj: dict):
        self.army_obj = army_obj
        self.reference_ws = {}
        self.calculations = {}
        self.points = 0

        self._load_references(self.army_obj.get("faction"))

    def get(self, keys: str):
        parts = keys.split('.')
        obj = self.army_obj
        for part in parts:
            obj = obj[part]
        return obj

    def has(self, keys: str):
        parts = keys.split('.')
        obj = self.army_obj
        for part in parts:
            if part in obj:
                obj = obj[part]
            else:
                return False
        return True

    # get with parsing
    def getp(self, keys: str, modifier: float = 0):
        parts = keys.split('.')
        obj = self.army_obj
        for part in parts:
            obj = obj[part]
        return parse_characteristic(obj, modifier)

    def _load_references(self, faction: str):
        # Path to the directory containing the JSON files
        directory_path = f'data/warscrolls/{faction}/reference/'

        for filename in os.listdir(directory_path):
            if filename.endswith('.json'):  # Only process JSON files
                file_path = os.path.join(directory_path, filename)

                # Open and load the JSON content
                with open(file_path, 'r') as json_file:
                    ws = WarScroll(json.load(json_file))
                    self.reference_ws[ws.get('name_en')] = ws

    def do_calculations(self, improved: bool = False):
        for unit in self.army_obj.get("units"):
            ws = self.reference_ws.get(unit.get("name_en"))
            if ws is None:
                logging.warning(f"Could not find reference for {unit.get('name_en')}")
                continue
            if unit.get("reinforced") is not None and unit.get("reinforced"):
                multiplier = 2
            else:
                multiplier = 1
            self.points += ws.get('characteristics.points') * multiplier
            ws.do_calculations(improved)
            for key in ws.calculations.keys():
                if key not in self.calculations:
                    self.calculations[key] = 0
                self.calculations[key] += ws.calculations[key] * multiplier

        self.calculations['mean_delivered_damage_per_points'] = self.calculations['mean_delivered_damage'] / self.points
        self.calculations['mean_received_damage_per_points'] = self.calculations['mean_received_damage'] / self.points
        self.calculations['mean_received_damage_per_total_health'] = (self.calculations['mean_received_damage'] /
                                                                      self.calculations['total_health'])
        self.calculations['total_health_per_points'] = self.calculations['total_health'] / self.points
        self.calculations['total_control_per_points'] = self.calculations['total_control'] / self.points
