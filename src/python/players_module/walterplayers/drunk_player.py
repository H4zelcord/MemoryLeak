from random import choice

from walterplayers.base_player import BasePlayer
from walterplayers.constants import Action

class DrunkPlayer(BasePlayer):
    ''' Drunk player will choose one random available action  '''

    def choose_action(self, find_response):
        
        available_actions = list(Action)

        result_action = Action.MOVE
        print(find_response)

        match result_action:
            case Action.STOP:
                return Action.STOP
            case Action.ATTACK:
                return result_action, choice(self.get_id_ias(find_response))
            case Action.DEFEND:
                return result_action, choice([True, False])
            case Action.MOVE:
                for zone in find_response.neighbours_zones:
                    print(zone.zone_id)
                    num_enemies = self.get_num_enemies_in_zone(zone)
                    if num_enemies == 0:
                        print("No hay enemigos...")
                        return Action.MOVE, zone.zone_id
            case _:
                return result_action, None
