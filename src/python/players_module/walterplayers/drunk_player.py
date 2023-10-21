from random import choice

from walterplayers.base_player import BasePlayer
from walterplayers.constants import Action

class DrunkPlayer(BasePlayer):
    ''' Drunk player will choose one random available action  '''

    def choose_action(self, find_response):
        
        available_actions = list(Action)

        #Consultar Vida Actual 
        print("Vida actual: ", self._life_points)
        #struct (list, dict) = mod1, mod2, mod3, mod4 (activan según self._life points)

        #Si estamos en una zona con enemigos, llamaremos a MOVE para que encuentre una zona libre a la que ir.
        #En caso contrario, llamaremos a STOP para permanecer en la zona segura.
        zone = find_response.current_zone
        num_enemies = self.get_num_enemies_in_zone(zone)
        if num_enemies == 0:
            print("No hay enemigos. Nos quedamos quietos...")
            result_action = Action.STOP
        if num_enemies != 0:
            print("Hay enemigos. Deberíamos movernos...")
            result_action = Action.MOVE

        #Diferentes respuestas en función de la acción decidida
        match result_action:
            case Action.STOP:
                return result_action, None
            case Action.ATTACK:
                return result_action, choice(self.get_id_ias(find_response))
            case Action.DEFEND:
                return result_action, choice([True, False])
            case Action.MOVE:
                #Buscamos una zona libre entre las vecinas. Si se encuentra, se mueve.
                for zone in find_response.neighbours_zones:
                    print(zone.zone_id)
                    num_enemies = self.get_num_enemies_in_zone(zone)
                    if num_enemies == 0:
                        print("No hay enemigos...")
                        return Action.MOVE, zone.zone_id
            case _:
                return result_action, None
