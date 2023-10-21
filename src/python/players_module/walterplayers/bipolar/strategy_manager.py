from walterplayers.bipolar.constants import AdviserMode

class StrategyManager:
    ''' Manager of strategy. Given defensive and ofensive limit, a strategy will be choosen. '''

    def __init__(self, defensive_limit, offensive_limit):
        self._previous_adviser_mode = AdviserMode.Offensive
        self._adviser_mode = AdviserMode.Offensive
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
            print('Mode limits initialized with Deffensive Mode Limit : ' +
                str(self._defenvise_mode_limit) + ' and Offensive Mode Limit: ' +
                str(self._offensive_mode_limit))

        if (AdviserMode.Offensive == self._adviser_mode
            and life_points <= self._defenvise_mode_limit):
            self._previous_adviser_mode = self._adviser_mode
            self._adviser_mode = AdviserMode.Defensive
            self._previous_adviser_mode = AdviserMode.Offensive
        elif self._defensive_limit <= life_points and life_points < self._offensive_mode_limit:
            self._adviser_mode = AdviserMode.Offensive
            return

        self._previous_adviser_mode = self._adviser_mode

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
    strategyManager.update_life_points(90)
    print(strategyManager.get_adviser_mode())
    print(strategyManager.is_strategy_changed())
    strategyManager.update_life_points(25)
    print(strategyManager.get_adviser_mode())
    print(strategyManager.is_strategy_changed())