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
        self.learners_wanted = None
        super().__init__(config)

    def load_learners(self, replace_unk=1):
        """Load the learners from the file specified in the config and store it in the class attribute for the new dataset format,
        including handling the 'wanted' attribute for each learner.

        Args:
            replace_unk (int, optional): The value to replace the unknown mastery levels. Defaults to 1.
        """
        learners_data = json.load(open(self.config["cv_path_reward"]))

        self.max_learner_skills = self.config["max_cv_skills"]
        self.learners_index = dict()
        self.learners = dict()
        self.learners_wanted = dict()  # New dictionary to store the 'wanted' value for each learner
        index = 0
        ll=0
        for learner_id, data in learners_data.items():
            
            skills = data["skills"]
            wanted_value = data["wanted"]  # Extract the 'wanted' value from the dataset
            self.learners[learner_id] = dict()
           
            self.learners_wanted[learner_id] = self.jobs[wanted_value] # Store the 'wanted' value
            self.learners_index[learner_id] = index
            self.learners_index[index] = learner_id
            index += 1

            for skill, mastery_level in skills:

                if (
                    isinstance(mastery_level, str)
                    and mastery_level in self.mastery_levels
                ):
                    mastery_level = self.mastery_levels[mastery_level]
                    if mastery_level == -1:
                        mastery_level = replace_unk
                    skill = self.skills2int[skill]
                    if skill not in self.learners[learner_id]:
                        self.learners[learner_id][skill] = []
                    self.learners[learner_id][skill].append(mastery_level)
            # Average the mastery levels for each skill
            for skill, level_list in self.learners[learner_id].items():
                self.learners[learner_id][skill] =round(sum(level_list) / len(level_list))

        # Remove learners with more skills than max_learner_skills
        self.learners = {
            key: value
            for key, value in self.learners.items()
            if len(value) <= self.max_learner_skills
        }
        self.learners_wanted = {
            key: value
            for key, value in self.learners_wanted.items()
            if key in self.learners
        }


    def _replace_mastery_level(self, mastery_level, replace_unk):
        """Helper function to replace the mastery level based on defined mappings."""
        if (
            isinstance(mastery_level, str)
            and mastery_level in self.mastery_levels
        ):
            mastery_level = self.mastery_levels[mastery_level]
            if mastery_level == -1:
                mastery_level = replace_unk
        return mastery_level

    
    def get_learner_job_wanted(self, learner):
        """Return the job wanted by the learner

        Args:
            learner (list): list of skills and mastery level of the learner

        Returns:
            dict: the job wanted by the learner
        """
        return self.learners_wanted[learner]

    def make_learners_index(self):
        """Make the index for the learners. The index is a dictionary that maps the learner id to its index and vice versa"""
        self.learners_index = dict()
        #index_ = 0
        index = 0
        tmp_learners = []
        tmp_learners_wanted = []
        #learners_index_test = dict()
        for learner_id, learner_wanted in self.learners_wanted.items():
            #learners_index_test[learner_id] = index_
            #learners_index_test[index_] = learner_id
            tmp_learners_wanted.append([(skill, level) for skill, level in learner_wanted.items()])
            #index_ += 1
        for learner_id, learner in self.learners.items():
            self.learners_index[learner_id] = index
            self.learners_index[index] = learner_id
            tmp_learners.append([(skill, level) for skill, level in learner.items()])
            index += 1
        self.learners = tmp_learners
        self.learners_wanted = tmp_learners_wanted

    def get_average_matching_job_learners(self):
        """Compute the average matching between all the learners and their wanted jobs wanted

        Returns:
            float: the average matching
        """
        matching = 0
        for elem1, elem2 in zip(self.learners, self.learners_wanted):
            matching += matchings.learner_job_matching(elem1, elem2)
        return matching / len(self.learners)