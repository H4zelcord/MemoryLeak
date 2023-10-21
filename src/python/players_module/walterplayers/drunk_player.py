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
            case Action.ATTACK:
                return result_action, choice(self.get_id_ias(find_response))
            case Action.DEFEND:
                return result_action, choice([True, False])
            case Action.MOVE:
                return result_action, choice(self.get_id_neighbours_zones(find_response))
            case _:
                return result_action, None
