import numpy as np
import pandas as pd

class c:
    def __init__(self, players):
        self.players = players

        self.shape = tuple(map(
            lambda x: len(x),
            self.players.values()))

        self.tensors = {}
        self.tensor_size = np.array(self.shape).prod()

        for player in players:
            self.tensors[player] = np.ndarray(
                shape=self.shape,
                buffer=np.zeros(self.tensor_size))
