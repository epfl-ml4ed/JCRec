import os
import random

import time as time
import numpy as np
import gymnasium as gym
from gymnasium import spaces
from stable_baselines3.common.callbacks import BaseCallback

import matchings
from CourseRecEnv import CourseRecEnv


class CourseRecEnv_reward(CourseRecEnv):
    # The CourseRecEnv class is a gym environment that simulates the recommendation of courses to learners. It is used to train the Reinforce model.
    def __init__(self, dataset, threshold=0.8, k=3):
        # Initialize the environment
        super().__init__(dataset, threshold, k)

#################### Rewritethe following code snippet ####################
    
    def step(self, action):
        """Method required by the gym environment. It performs the action in the environment and returns the new observation, the reward, whether the episode is terminated, and additional information.

        Args:
            action (int): the course to be recommended

        Returns:
            tuple: the new observation, the reward, whether the episode is terminated, additional information
        """

        course = self.dataset.courses[action]
        learner = self.obs_to_learner()

        required_matching = matchings.learner_course_required_matching(learner, course)# nombre de skills posséder par le profil nécessiare pour le cours donc si le nb est faible alors le cours n epeut pas etre suivi
        provided_matching = matchings.learner_course_provided_matching(learner, course)# nombre de skills gained par le cours. donc si le nb est hait alors le cours est inutile
        
        # Determine if the course is successful based on a probability, which depends on the matching between the learner and the course
        course_success_probability = required_matching # for example, 80% success rate
        course_successful = np.random.rand() < course_success_probability

        if  provided_matching >= 1.0 or not course_successful:
            observation = self._get_obs()
            reward = 0 if not course_successful else -1  # penalize for unsuccessful course, adjust as needed
            terminated = True
            info = self._get_info()
            return observation, reward, terminated, False, info


        if course_successful:
            for skill, level in course[1]:
                self._agent_skills[skill] = max(self._agent_skills[skill], level)

        observation = self._get_obs()
        info = self._get_info()
        reward = info["nb_applicable_jobs"] if course_successful else -1  # adjust reward based on course success
        self.nb_recommendations += 1
        terminated = self.nb_recommendations == self.k

        return observation, reward, terminated, False, info


    
    
    
    def reset(self, seed=None, learner=None):
        """Method required by the gym environment. It resets the environment to its initial state.

        Args:
            seed (int, optional): Random seed. Defaults to None.
            learner (list, optional): Learner to initialize the environment with, if None, the environment is initialized with a random learner. Defaults to None.

        Returns:
            _type_: _description_
        """
        # We need the following line to seed self.np_random
        super().reset(seed=seed)

        if learner is not None:
            self._agent_skills = self.learner_to_obs(learner)
        else:
            self._agent_skills = self.get_random_learner()
        self.nb_recommendations = 0
        observation = self._get_obs()
        info = self._get_info()
        return observation, info