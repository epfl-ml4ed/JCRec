import os
import json

from copy import deepcopy
from time import time
import matchings as mt
import numpy as np

from Greedy import Greedy
# from Dataset import Dataset


class Greedy_reward(Greedy):
    def __init__(self, dataset, threshold):
        super().__init__(dataset, threshold)
        self.child_attribute = "Je suis un attribut de l'enfant"

############################# Change the method below #############################

    def get_course_recommendation(self, learner, enrollable_courses):
        """Return the greedy recommendation for the learner

        Args:
            learner (list): list of skills and mastery level of the learner
            enrollable_courses (dict): dictionary of courses that the learner can enroll in

        Returns:
            int: the id of the course recommended
        """
        course_recommendation = None
        max_nb_applicable_jobs = 0
        max_attractiveness = 0

        for id_c, course in enrollable_courses.items():
            tmp_learner = deepcopy(learner)
            self.update_learner_profile(tmp_learner, course)

            nb_applicable_jobs = self.dataset.get_nb_applicable_jobs(
                tmp_learner, self.threshold
            )
            attractiveness = self.dataset.get_learner_attractiveness(tmp_learner)

            required_matching = mt.learner_course_required_matching(learner, course)# nombre de skills posséder par le profil nécessiare pour le cours donc si le nb est faible alors le cours n epeut pas etre suivi
            nb_applicable_jobs_prob = nb_applicable_jobs*required_matching
            # Select the course that maximizes the number of applicable jobs

            if nb_applicable_jobs_prob > max_nb_applicable_jobs:
                max_nb_applicable_jobs = nb_applicable_jobs_prob
                course_recommendation = id_c
                max_attractiveness = attractiveness

            # If there are multiple courses that maximize the number of applicable jobs,
            # select the one that maximizes the attractiveness of the learner

            elif nb_applicable_jobs_prob == max_nb_applicable_jobs:
                if attractiveness > max_attractiveness:
                    max_attractiveness = attractiveness
                    course_recommendation = id_c

        return course_recommendation

