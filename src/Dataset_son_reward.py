import json
import os
import random

import yaml
import pandas as pd

import matchings
from Dataset import Dataset


class Dataset_son_reward(Dataset):
    # The Dataset class is used to load and store the data of the recommendation problem
    def __init__(self, config):
        # Load the data from the configuration file
        super().__init__(config)
        self.child_attribute = "Je suis un attribut de l'enfant"
    def methode_child(self):
        return "Ceci est une méthode de l'enfant"
