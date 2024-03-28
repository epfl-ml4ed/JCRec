import os
import json

from copy import deepcopy
from time import time
import matchings as mt
import numpy as np

# from Dataset import Dataset


class Greedy:
    def __init__(self, dataset, threshold, proba_version):
        self.dataset = dataset
        self.threshold = threshold
        self.proba_version = proba_version

    def update_learner_profile(self, learner, course):
        """Update the learner profile with the skills and levels provided by the course

        Args:
            learner (list): list of skills and mastery level of the learner
            course (list): list of required (resp. provided) skills and mastery level of the course
        """
        # Update the learner profile with the skills and levels provided by the course (course [1] is the list of skills and levels provided by the course)
        for cskill, clevel in course[1]:
            found = False
            i = 0
            while not found and i < len(learner):
                lskill, llevel = learner[i]
                if cskill == lskill:
                    learner[i] = (lskill, max(llevel, clevel))
                    found = True
                i += 1
            if not found:
                learner.append((cskill, clevel))

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

    def recommend_and_update(self, learner):
        """Recommend a course to the learner and update the learner profile

        Args:
            learner (list): list of skills and mastery level of the learner

        Returns:
            int: the id of the course recommended
        """
        enrollable_courses = self.dataset.get_all_enrollable_courses(
            learner, self.threshold
        )
        # print(f"{len(enrollable_courses)} courses are enrollable for this learner")
        # print(f"{enrollable_courses.keys()}")
        course_recommendation = self.get_course_recommendation(
            learner, enrollable_courses
        )

        self.update_learner_profile(
            learner, self.dataset.courses[course_recommendation]
        )
        return course_recommendation

    def greedy_recommendation(self, k, run):
        """Make k greedy recommendations for each learner and save the results in a json file

        Args:
            k (int): number of recommendations to make for each learner
            run (int): run number
        """
        results = dict()
        print(f"-----------------------------------------------------------------")
        avg_l_attrac = self.dataset.get_avg_learner_attractiveness()
        print(f"The average attractiveness of the learners is {avg_l_attrac:.2f}")

        results["original_attractiveness"] = avg_l_attrac

        avg_app_j = self.dataset.get_avg_applicable_jobs(self.threshold)
        print(f"The average nb of applicable jobs per learner is {avg_app_j:.2f}")

        results["original_applicable_jobs"] = avg_app_j

        time_start = time()
        recommendations = dict()

        for i, learner in enumerate(self.dataset.learners):
            index = self.dataset.learners_index[i]
            recommendation_sequence = []
            for _ in range(k):
                recommendation_sequence.append(
                    self.recommend_and_update(self.dataset.learners[i])
                )
            recommendations[index] = [
                self.dataset.courses_index[course_id]
                for course_id in recommendation_sequence
            ]

        time_end = time()
        avg_recommendation_time = (time_end - time_start) / len(self.dataset.learners)
        print(f"-----------------------------------------------------------------")

        print(f"Average Recommendation Time: {avg_recommendation_time:.2f} seconds")

        results["avg_recommendation_time"] = avg_recommendation_time

        avg_l_attrac = self.dataset.get_avg_learner_attractiveness()
        print(f"The new average attractiveness of the learners is {avg_l_attrac:.2f}")

        results["new_attractiveness"] = avg_l_attrac

        avg_app_j = self.dataset.get_avg_applicable_jobs(self.threshold)
        print(f"The new average nb of applicable jobs per learner is {avg_app_j:.2f}")
        print(f"-----------------------------------------------------------------")

        results["new_applicable_jobs"] = avg_app_j

        results["recommendations"] = recommendations

        filename = (
            "greedy_nbskills_"
            + str(len(self.dataset.skills))
            + "_k_"
            + str(k)
            + "_run_"
            + str(run)
            + ".json"
        )
        
        json.dump(
            results,
            open(
                os.path.join(
                    self.dataset.config["results_path"],
                    filename,
                ),
                "w",
            ),
            indent=4,
        )
