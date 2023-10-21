from walterplayers.bipolar.constants import AdviserMode

class StrategyManager:
    ''' Manager of strategy. Given defensive and ofensive limit, a strategy will be choosen. '''

    def __init__(self, ultra_offensive_limit, offensive_limit, defensive_limit, ultra_defensive_limit):
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
        print('Strategy Manager created with UltraOffensive Limit: ' + 
            str(self._ultra_offensive_limit) + 'Offensive Limit: ' +
            str(self._offensive_limit) + 'Defensive Limit: ' +
            str(self._defensive_limit) + ' and UltraDefensive Limit: ' +
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
           
            print('Mode limits initialized with UltraOffensive Mode Limit : ' +
                str(self._ultra_offensive_mode_limit) + ' Offensive Mode Limit: ' +
                str(self._offensive_mode_limit) + ' Defensive Mode Limit: ' +
                str(self._defensive_mode_limit) + ' and UltraDefensive Mode Limit: ' +
                str(self._ultra_defensive_mode_limit)
            )
        
        if life_points > 0 and life_points < self._ultra_defensive_mode_limit:
            self._adviser_mode = AdviserMode.UltraDefensive
            self._previous_adviser_mode = AdviserMode.Defensive
        elif self._ultra_defensive_limit <= life_points and life_points < self._defensive_mode_limit:
            self._adviser_mode = AdviserMode.Defensive
            self._previous_adviser_mode = AdviserMode.UltraDefensive
        elif self._defensive_limit <= life_points and life_points < self._offensive_mode_limit:
            self._adviser_mode = AdviserMode.Offensive
            self._previous_adviser_mode = AdviserMode.UltraOffensive
        elif self._offensive_limit <= life_points and life_points < self._ultra_offensive_mode_limit:
            self._adviser_mode = AdviserMode.UltraOffensive
            self._previous_adviser_mode = AdviserMode.Offensive

    def is_strategy_changed(self):
        ''' Return True if life point changes strategy to follow up. '''
        return self._previous_adviser_mode != self._adviser_mode

    def get_adviser_mode(self):
        ''' Return active adviser mode. '''
        return self._adviser_mode


if __name__ == "__main__":
    strategyManager = StrategyManager(1, 0.8, 0.5, 0.3)
    strategyManager.update_life_points(200)
    print(strategyManager.get_adviser_mode())
    print(strategyManager.is_strategy_changed())
    strategyManager.update_life_points(170)
    print(strategyManager.get_adviser_mode())
    print(strategyManager.is_strategy_changed())
    strategyManager.update_life_points(150)
    print(strategyManager.get_adviser_mode())
    print(strategyManager.is_strategy_changed())
    strategyManager.update_life_points(120)
    print(strategyManager.get_adviser_mode())
    print(strategyManager.is_strategy_changed())
    strategyManager.update_life_points(90)
    print(strategyManager.get_adviser_mode())
    print(strategyManager.is_strategy_changed())
    strategyManager.update_life_points(25)
    print(strategyManager.get_adviser_mode())
    print(strategyManager.is_strategy_changed())