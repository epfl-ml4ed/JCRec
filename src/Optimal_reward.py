import os
import json

from copy import deepcopy
from time import time
import matchings as mt
from Optimal import Optimal
# from Dataset import Dataset


class Optimal_reward(Optimal):
    def __init__(self, dataset, threshold):
        super().__init__(dataset, threshold)
        self.child_attribute = "Je suis un attribut de l'enfant"
    def methode_child(self):
        return "Ceci est une méthode de l'enfant"