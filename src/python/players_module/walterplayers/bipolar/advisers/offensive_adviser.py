from random import choice, uniform
from walterplayers.client.dtos.responses import Status
from walterplayers.bipolar.advisers.adviser import Adviser
from walterplayers.constants import Action,Role


class OffensiveAdviser(Adviser):
    ''' Offensive Adviser will be used when life is between 80% and 50%.
    This Adviser will priorize going for karin_gift and lucky_unlucky zones'''

    def __init__(self, player):
        super().__init__(player)
        self._last_action = Action.STOP
        self._attacking = False
        self._life_before_attack = 0
        self._attack_retry = 0 

    def get_interesting_zone(self, find_response):
        interesting_zones = []
        for zone in find_response.neighbours_zones:
            if self.is_interesting_zone(zone):
                interesting_zones.append(zone)
        if interesting_zones:
        #Se ha encontrado alguna zona interesante, mover a por ella.
            return interesting_zones[0]
        else:
        # No se encontraron zonas interesantes
            return None

    def is_interesting_zone(self, zone):
        return zone.triggers.go_ryu or zone.triggers.lucky_unlucky or zone.triggers.karin_gift

    def get_weight_for_zone(self, zone):
        # lets include the edge, taking path with lucky_unlucky
        if zone.triggers.lucky_unlucky | zone.triggers.karin_gift:
            weight = 0.5
        else:
            weight = 1
        return weight

    def get_next_action(self, find_response):
        # Llamar al método get_interesting_zone para obtener la zona interesante
        interesting_zone = self.get_interesting_zone(find_response)

        if (find_response.status.buff.lucky_unlucky >=1 
        and find_response.status.buff.go_ryu == 1):
            Ias = find_response
            for zone in find_response.neighbours_zones:
                for elemento in Ias.current_zone.ias:
                    if elemento.role == Role.BERGEN_TOY:
                        Ias.current_zone.ias.remove(elemento)
                    if len(Ias.current_zone.ias) == 0:
                        return Action.MOVE, (zone.zone_id)
                    else:
                        if self._player.is_possible_attack(find_response):
                            return (Action.ATTACK, self.get_weakest_enemy(find_response))
                        else:
                            return (Action.MOVE, zone.zone_id)
            
        if interesting_zone is not None:
        # Configurar la acción de movimiento hacia la zona interesante
            return (Action.MOVE, interesting_zone.zone_id)
        else:
        # Si no encontramos zona interesante, atacamos 3 veces o hasta que nos hagan daño
            if (Action.MOVE == self._last_action and 
                self._player.is_possible_attack(find_response)):
                self._last_action = Action.ATTACK
                self._attacking = True
                self._life_before_attack = find_response.status.life
                self._attack_retry = 1
                return (Action.ATTACK, self.get_weakest_enemy(find_response))
        
        if (self._attacking & 
            self._attack_retry < 3 & 
            self._life_before_attack == find_response.status.life & 
            self._player.is_possible_attack(find_response)):

            self._last_action = Action.ATTACK
            self._attack_retry += 1
            return (Action.ATTACK, self.get_weakest_enemy(find_response))

        self._last_action = Action.MOVE
        self._attacking = False

        if (self._last_action == Action.MOVE or self._last_action == Action.ATTACK or self._last_action == Action.STOP):
                for zone in find_response.neighbours_zones:
                    if (zone.triggers.karin_gift & zone.triggers.lucky_unlucky):
                        return Action.MOVE, zone.zone_id
                    else:
                        return Action.MOVE, zone.zone_id
        
        if not self._player.is_possible_move(find_response):
            return Action.STOP, None

        # There is alredy a plan, let execute next step or
        # If a go ryu zone is known, player must go there
        if self._actions_to_execute or self.check_and_update_interested_zone_path(find_response):
            return self._actions_to_execute.popleft()

        if self._player.is_possible_attack(find_response) and uniform(0,1) <= 0.6:
            return Action.STOP, None

        unkown_zones = self.get_unknown_zones(find_response)

        if unkown_zones:
            return (Action.MOVE, self._get_zone_with_more_enemies(unkown_zones))

        #lets include current zone to the neighbours to be able
        # to stay in the same zone
        possible_zones = find_response.neighbours_zones.copy()
        possible_zones.append(find_response.current_zone)

        zone_with_more_enemies = self._get_zone_with_more_enemies(possible_zones)

        if zone_with_more_enemies == find_response.current_zone.zone_id:
            return (Action.STOP, None)

        return (Action.MOVE, zone_with_more_enemies)

    def atacar_enemigo(self, find_response):
        self._player._life_points
        vida_actual = find_response.status.life
        while (vida_actual == find_response.status.life & numero_ataques<3):
            numero_ataques = numero_ataques+1
            return Action.ATTACK, find_response.get_enemies(self, find_response)
        
    def _get_zone_with_more_enemies(self, find_response):
        max_enemies = -1
        zones_to_move = []

        for zone in find_response:
            num_enemies = self._player.get_num_enemies_in_zone(zone)
            if num_enemies == max_enemies:
                zones_to_move.append(zone.zone_id)
            elif num_enemies > max_enemies:
                zones_to_move.clear()
                zones_to_move.append(zone.zone_id)
                max_enemies = num_enemies

        return choice(zones_to_move)
