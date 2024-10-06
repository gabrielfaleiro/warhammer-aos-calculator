import json


class BaseData(object):

    enemy_defense = {}
    received_attacks = {}
    unit_value = {}

    @staticmethod
    def load_base():
        file_path = './data/base/enemy_defense.json'
        with open(file_path, 'r') as json_file:
            try:
                BaseData.enemy_defense = json.load(json_file)
            except json.JSONDecodeError as e:
                print(f"Error parsing {file_path}: {e}")

        file_path = './data/base/received_attacks.json'
        with open(file_path, 'r') as json_file:
            try:
                BaseData.received_attacks = json.load(json_file)
            except json.JSONDecodeError as e:
                print(f"Error parsing {file_path}: {e}")

        file_path = './data/base/unit_value.json'
        with open(file_path, 'r') as json_file:
            try:
                BaseData.unit_value = json.load(json_file)
            except json.JSONDecodeError as e:
                print(f"Error parsing {file_path}: {e}")
