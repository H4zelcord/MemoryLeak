#IMPORTANTE: ESTO ES UNA COPIA DE LA ESTRATEGIA DEFENSIVA.
#HAY QUE DESARROLLARLA ACORDE A LO QUE HEMOS PENSADO.

import sys
from random import choice, uniform

from walterplayers.bipolar.advisers.adviser import Adviser
from walterplayers.constants import Action

class UltraDefensiveAdviser(Adviser):
    ''' Defensive Adviser will be used when life is less than the limit.
    This Adviser will priorize going for karin_gift zones'''

    def is_interesting_zone(self, zone):
        return zone.triggers.karin_gift and zone.triggers.lucky_unlucky

    def get_weight_for_zone(self, zone):
        # lets include the edge, avoiding taking path with lucky_unlucky
        if zone.triggers.lucky_unlucky:
            weight = 1
        else: 
            weight = 0.5
        return weight

    def get_next_action(self, find_response):
        # It looks like we are one of the finisher players.
        if (not self._player.is_possible_move(find_response) and
            self._player.is_possible_attack(find_response)):
            return Action.ATTACK, self.get_weakest_enemy(find_response) 
    
        # There is alredy a plan, let execute next step OR
        # if a karin gift is known, player must go there
        if (self._actions_to_execute or
            self.check_and_update_interested_zone_path(find_response)):
            return self._actions_to_execute.popleft()

        if self._player.is_possible_attack(find_response) and self.all_neighbours_zones_has_less_than_three_enemies(find_response):
            weakest_enemy = self.get_enemy(find_response)
            if weakest_enemy.life <= find_response.status.life:
                return Action.ATTACK, weakest_enemy.id

        unknown_zones = self.get_unknown_zones(find_response)

        if unknown_zones and uniform(0,1) >= 0.5:
            return (Action.MOVE, self._get_zone_with_less_enemies(unknown_zones))

        #lets include current zone to the neighbours to be able
        # to stay in the same zone
        possible_zones = find_response.neighbours_zones.copy()
        possible_zones.append(find_response.current_zone)

        zone_with_less_enemies = self._get_zone_with_less_enemies(possible_zones)

        if zone_with_less_enemies == find_response.current_zone.zone_id:
            return (Action.STOP, None)

        return (Action.MOVE, zone_with_less_enemies)
    
    def all_neighbours_zones_has_less_than_three_enemies(self, find_response):
        for zone in find_response.neighbours_zones:
            if self._player.get_num_enemies_in_zone(zone) >= 3:
                return False
            
        return True

    
    def get_enemy(self, find_response):
        ''' The weakest enemy in the current zone. '''
        min_life = sys.maxsize
        enemy_to_attack = None

        for enemy in self._player.get_enemies(find_response):
            if enemy.life <= min_life:
                enemy_to_attack = enemy
                min_life = enemy.life

        return enemy_to_attack

    def _get_zone_with_less_enemies(self, possible_zones):
        min_enemies = sys.maxsize
        zones_to_move = []

        for zone in possible_zones:
            num_enemies = self._player.get_num_enemies_in_zone(zone)
            if num_enemies == min_enemies:
                zones_to_move.append(zone.zone_id)
            elif num_enemies < min_enemies:
                zones_to_move.clear()
                zones_to_move.append(zone.zone_id)
                min_enemies = num_enemies

        return choice(zones_to_move)