import numpy as np
import pandas as pd

# player: str
# action: str
# strategy: (player, action)
# strategies: pd.Series
# opponent_strategies: pd.Series -- length == self.players.size - 1
# strategy_profile: pd.Series -- length == self.players.size

class c:
    def __init__ (self, players, payoff_tensor):
        self.players = pd.Series (players, name = "players")
        self.player_shape = tuple (map (len, self.players.values))
        self.payoff_tensor_shape = tuple ([
            *self.player_shape,
            len (players),
        ])

        assert payoff_tensor.shape == self.payoff_tensor_shape
        self.payoff_tensor = payoff_tensor

    def Strategies (self, strategies, name = "Strategies"):
        return pd.Series (
            strategies,
            name = name,
            index = self.players.index)

    def strategy_to_index (self, strategy):
        player, action = strategy
        if pd.isna (action):
            return slice (None)
        else:
            return self.players [player] .index (action)

    def strategies_to_index_list (self, strategies):
        return list (map (
            lambda strategy: self.strategy_to_index (strategy),
            strategies.items ()))

    def payoff_array (self, strategy_profile):
        strategy_profile = self.Strategies (strategy_profile)
        assert strategy_profile.size == self.players.size
        index_list = self.strategies_to_index_list (strategy_profile)
        return self.payoff_tensor [tuple (index_list)]

    def payoff_series (self, strategy_profile):
        return pd.Series (
            self.payoff_array (strategy_profile),
            name = "playoffs",
            index = self.players.index)

    def responses (self, opponent_strategies):
        opponent_strategies = self.Strategies (opponent_strategies)
        miss = opponent_strategies [ opponent_strategies.isna () ]
        player_list = miss.keys ()
        assert len (player_list) == 1
        player = player_list [0]
        action_list = self.players [player]
        index_list = self.strategies_to_index_list (opponent_strategies)
        multi_index = pd.MultiIndex.from_arrays (
            [action_list],
            names = [player])
        return pd.DataFrame (
            self.payoff_tensor [tuple (index_list)],
            index = multi_index,
            columns = self.players.keys ())

    def bast_response (self, opponent_strategies):
        responses = self.responses (opponent_strategies)
        player = responses.index.names [0]
        return responses.sort_values (
            by = player,
            axis = 0,
            ascending = False) .head (1)

    # def opponent_strategies (self, strategy):
    #     return

    # def nash_equilibrium (self):
    #     return

    # def dominant_strategy (self):
    #     return
