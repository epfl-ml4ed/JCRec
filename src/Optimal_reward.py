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


############################# Change the method below #############################

    def get_course_recommendation(
        self,
        learner,
        enrollable_courses,
        candiate_course_recommendation_list,
        course_recommendations_list,
        max_nb_applicable_jobs,
        max_attractiveness,
        k,
    ):
        """Recursively get the optimal sequence of courses for a learner

        Args:
            learner (list): list of skills and mastery level of the learner
            enrollable_courses (dict): dictionary of courses that the learner can enroll in
            candiate_course_recommendation_list (list): list of candiate courses for the recommendation
            course_recommendations_list (list): optimal sequence of courses for the recommendation to be returned
            max_nb_applicable_jobs (int): current maximum number of applicable jobs given the recommendation list
            max_attractiveness (int): current maximum attractiveness given the recommendation list
            k (int): number of courses to recommend

        Returns:
            tuple: optimal sequence of courses for the recommendation, current maximum number of applicable jobs, current maximum attractiveness
        """
        if k == 0:
            # Base case: return the current recommendation list if the number of applicable jobs is greater than the current maximum
            nb_applicable_jobs = self.dataset.get_nb_applicable_jobs(
                learner, self.threshold
            )
            attractiveness = self.dataset.get_learner_attractiveness(learner)
            required_matching = mt.learner_course_required_matching_totale(learner, candiate_course_recommendation_list, self.dataset)# nombre de skills posséder par le profil nécessiare pour le cours donc si le nb est faible alors le cours n epeut pas etre suivi
            nb_applicable_jobs_prob = nb_applicable_jobs*required_matching

            if nb_applicable_jobs_prob > max_nb_applicable_jobs:
                course_recommendations_list = candiate_course_recommendation_list
                max_nb_applicable_jobs = nb_applicable_jobs_prob
                max_attractiveness = attractiveness

            # If there are multiple courses that maximize the number of applicable jobs,
            # select the one that maximizes the attractiveness of the learner
            elif (
                nb_applicable_jobs_prob == max_nb_applicable_jobs
                and attractiveness > max_attractiveness
            ):
                course_recommendations_list = candiate_course_recommendation_list
                max_nb_applicable_jobs = nb_applicable_jobs_prob
                max_attractiveness = attractiveness

            return (
                course_recommendations_list,
                max_nb_applicable_jobs,
                max_attractiveness,
            )
        # Recursive case: for all courses that the learner can enroll in, get the optimal sequence of courses by calling the function recursively
        else:
            enrollable_courses = self.dataset.get_all_enrollable_courses(
                learner, self.threshold
            )

            for id_c, course in enrollable_courses.items():
                tmp_learner = deepcopy(learner)
                self.update_learner_profile(tmp_learner, course)
                new_candidate_list = candiate_course_recommendation_list + [id_c]
                (
                    course_recommendations_list,
                    max_nb_applicable_jobs,
                    max_attractiveness,
                ) = self.get_course_recommendation(
                    tmp_learner,
                    enrollable_courses,
                    new_candidate_list,
                    course_recommendations_list,
                    max_nb_applicable_jobs,
                    max_attractiveness,
                    k - 1,
                )

            return (
                course_recommendations_list,
                max_nb_applicable_jobs,
                max_attractiveness,
            )