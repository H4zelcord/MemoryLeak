from walterplayers.bipolar.constants import AdviserMode

class StrategyManager:
    ''' Manager of strategy. Given defensive and ofensive limit, a strategy will be choosen. '''

    def __init__(self, ultra_offensive_limit, offensive_limit, defensive_limit, ultra_defensive_limit):
        #Inicio en Ultraofensiva
        self._adviser_mode = AdviserMode.UltraOffensive
        self._previous_adviser_mode = AdviserMode.UltraOffensive
        self._ultra_offensive_limit = ultra_offensive_limit
        self._offensive_limit = offensive_limit
        self._defensive_limit = defensive_limit
        self._ultra_defensive_limit = ultra_defensive_limit
        self._ultra_offensive_mode_limit = None
        self._offensive_mode_limit = None
        self._defensive_mode_limit = None
        self._ultra_defensive_mode_limit = None
        #Print de los porcentajes de los limites a fijar
        print('Strategy Manager created with UltraOffensive Limit: ' + 
            str(self._ultra_offensive_limit) + '\nOffensive Limit: ' +
            str(self._offensive_limit) + '\nDefensive Limit: ' +
            str(self._defensive_limit) + '\nand UltraDefensive Limit: ' +
            str(self._ultra_defensive_limit)
        )

    def update_life_points(self, life_points):
        ''' Update life points to strategy manager. Life point is used to change strategy. '''
        if (not self._ultra_offensive_mode_limit or not self._offensive_mode_limit
        or not self._defensive_mode_limit or not self._ultra_defensive_mode_limit):
            #First time that the life points is updated, limits should be compute
            self._ultra_offensive_mode_limit = self._ultra_offensive_limit * life_points
            self._offensive_mode_limit = self._offensive_limit * life_points
            self._defensive_mode_limit = self._defensive_limit * life_points
            self._ultra_defensive_mode_limit = self._ultra_defensive_limit * life_points
            #Print de los limites fijados
            print('Mode limits initialized with UltraOffensive Mode Limit : ' +
                str(self._ultra_offensive_mode_limit) + '\nOffensive Mode Limit: ' +
                str(self._offensive_mode_limit) + '\nDefensive Mode Limit: ' +
                str(self._defensive_mode_limit) + '\nand UltraDefensive Mode Limit: ' +
                str(self._ultra_defensive_mode_limit)
            )
        #Paso a Ultradefensiva
        if life_points > 0 and life_points < self._ultra_defensive_mode_limit:
            self._previous_adviser_mode = self._adviser_mode
            self._adviser_mode = AdviserMode.UltraDefensive
        #Paso a Defensiva
        elif self._ultra_defensive_limit <= life_points and life_points < self._defensive_mode_limit:
            self._previous_adviser_mode = self._adviser_mode
            self._adviser_mode = AdviserMode.Defensive
        #Paso a Ofensiva
        elif self._defensive_limit <= life_points and life_points < self._offensive_mode_limit:
            self._previous_adviser_mode = self._adviser_mode
            self._adviser_mode = AdviserMode.Offensive
        #Pase a Ultraofensiva
        elif self._offensive_limit <= life_points and life_points < self._ultra_offensive_mode_limit:
            self._previous_adviser_mode = self._adviser_mode
            self._adviser_mode = AdviserMode.UltraOffensive
    #Se comprueba si se ha cambiado de estrategia para cambiar acciones a realizar si fuera necesario
    def is_strategy_changed(self):
        ''' Return True if life point changes strategy to follow up. '''
        return self._previous_adviser_mode != self._adviser_mode

    def get_adviser_mode(self):
        ''' Return active adviser mode. '''
        return self._adviser_mode