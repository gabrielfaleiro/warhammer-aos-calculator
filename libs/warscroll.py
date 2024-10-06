import json
from libs.common import parse_characteristic
from libs.base import BaseData


class WarScroll:
    def __init__(self, warscroll_obj: dict):
        self.warscroll_obj = warscroll_obj
        self.enemy_save = BaseData.enemy_defense['save']
        self.enemy_ward = BaseData.enemy_defense['ward']
        self.reference_points = BaseData.unit_value['reference_points']
        self.received_wounds = BaseData.received_attacks['wounds']
        self.received_rend = BaseData.received_attacks['rend']
        self.received_damage = BaseData.received_attacks['damage']
        self.calculations = {}

    def get(self, keys: str):
        parts = keys.split('.')
        obj = self.warscroll_obj
        for part in parts:
            obj = obj[part]
        return obj

    def has(self, keys: str):
        parts = keys.split('.')
        obj = self.warscroll_obj
        for part in parts:
            if part in obj:
                obj = obj[part]
            else:
                return False
        return True

    # get with parsing
    def getp(self, keys: str, modifier: float = 0):
        parts = keys.split('.')
        obj = self.warscroll_obj
        for part in parts:
            obj = obj[part]
        return parse_characteristic(obj, modifier)

    def do_calculations(self, improved: bool = False):
        # self.calc_mean_delivered_damage(improved)
        self.calc_mean_delivered_damage_per_points(improved)
        self.calc_mean_received_damage(improved)

    def calc_mean_delivered_damage(self, improved: bool = False) -> float:
        melee_damage = 0
        ranged_damage = 0

        for weapon in self.get('weapons'):
            [weapon_type, delivered_damage, shoot_in_combat] = self._get_weapon_damage(weapon, improved)

            if weapon_type == 'melee':
                melee_damage = melee_damage + delivered_damage
            elif weapon_type == 'ranged':
                ranged_damage = ranged_damage + delivered_damage
                if shoot_in_combat:
                    melee_damage = melee_damage + delivered_damage
            else:
                raise ValueError(f"Invalid weapon type: {weapon_type}")

        main_combat_type = self.get('characteristics.main_combat_type')
        if main_combat_type == 'melee':
            mean_delivered_damage = melee_damage
        elif main_combat_type == 'ranged':
            mean_delivered_damage = ranged_damage
        else:
            raise ValueError(f"Invalid weapon type: {main_combat_type}")

        self.calculations['mean_delivered_damage'] = mean_delivered_damage
        return mean_delivered_damage

    def _get_weapon_damage(self, weapon: dict, improved: bool = False) -> list:
        weapon_ws = WarScroll(weapon)

        # Number of weapons in unit
        if weapon_ws.get('quantity') == 'miniatures_in_unit':
            quantity = self.getp('characteristics.miniatures_in_unit')
        else:
            quantity = weapon_ws.getp('quantity')

        if improved:
            if weapon_ws.has('improved'):
                stats_ws = WarScroll(weapon_ws.get('improved'))
            else:
                stats_ws = WarScroll(weapon_ws.get('base'))
        else:
            stats_ws = WarScroll(weapon_ws.get('base'))

        # Number of wounds inflicted
        if 'crit-mortal' in stats_ws.get('abilities'):
            wounds = (quantity *
                      stats_ws.getp('attacks') *
                      stats_ws.getp('hit', -1) *
                      stats_ws.getp('wound'))
            # Introduce enemy defense characteristics
            delivered_wounds = wounds * (1.0 - parse_characteristic(self.enemy_save,
                                                                    - stats_ws.getp('rend')))
            mortal_wounds = quantity * stats_ws.getp('attacks') * 1 / 6
            delivered_damage = (stats_ws.getp('damage') *
                                ((delivered_wounds + mortal_wounds) *
                                (1.0 - parse_characteristic(self.enemy_ward))))

        else:
            if 'crit-auto-wound' in stats_ws.get('abilities'):
                wounds = (quantity *
                          stats_ws.getp('attacks') *
                          (1/6 + stats_ws.getp('hit', -1) *
                          stats_ws.getp('wound')))
            elif 'crit-2-hits' in stats_ws.get('abilities'):
                wounds = (quantity *
                          stats_ws.getp('attacks') *
                          (1 / 6 + stats_ws.getp('hit')) *
                          stats_ws.getp('wound'))
            else:
                wounds = (quantity *
                          stats_ws.getp('attacks') *
                          stats_ws.getp('hit') *
                          stats_ws.getp('wound'))

            # Introduce enemy defense characteristics
            delivered_wounds = wounds * (1.0 - parse_characteristic(self.enemy_save,
                                                                    - stats_ws.getp('rend')))
            delivered_damage = (stats_ws.getp('damage') *
                                delivered_wounds *
                                (1.0 - parse_characteristic(self.enemy_ward)))

        weapon_type = weapon_ws.get('type')
        if 'shoot-in-combat' in stats_ws.get('abilities'):
            shoot_in_combat = True
        else:
            shoot_in_combat = False

        return [weapon_type, delivered_damage, shoot_in_combat]

    def calc_mean_delivered_damage_per_points(self, improved: bool = False) -> float:
        mean_delivered_damage_per_points = \
            (self.reference_points *
             (self.calc_mean_delivered_damage(improved) /
              self.getp('characteristics.points')))

        self.calculations['mean_delivered_damage_per_points'] = mean_delivered_damage_per_points
        return mean_delivered_damage_per_points


    def calc_mean_received_damage(self, improved: bool = False) -> float:

        if improved:
            if self.has('characteristics.improved'):
                characteristics_ws = WarScroll(self.get('characteristics.improved'))
            else:
                characteristics_ws = WarScroll(self.get('characteristics.base'))
        else:
            characteristics_ws = WarScroll(self.get('characteristics.base'))

        # Calculate saves
        save = characteristics_ws.get('save')
        mean_received_wounds = self.received_wounds * (1.0 - parse_characteristic(save, - self.received_rend))

        # Calculate wards
        ward = characteristics_ws.get('ward')
        if ward is None:
            mean_received_damage = self.received_damage * mean_received_wounds
        else:
            mean_received_damage = self.received_damage * mean_received_wounds * (1.0 - parse_characteristic(ward))

        self.calculations['mean_received_damage'] = mean_received_damage
        return mean_received_damage

