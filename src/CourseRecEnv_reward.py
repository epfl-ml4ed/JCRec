import os
import random

import time as time
import numpy as np
import gymnasium as gym
from gymnasium import spaces
from stable_baselines3.common.callbacks import BaseCallback

import matchings
from CourseRecEnv import CourseRecEnv, EvaluateCallback
from Dataset_son_reward import Dataset_son_reward
from Optimal_reward import Optimal_reward


class CourseRecEnv_reward(CourseRecEnv):
    # The CourseRecEnv class is a gym environment that simulates the recommendation of courses to learners. It is used to train the Reinforce model.
    def __init__(self, dataset, threshold=0.8, k=3):
        super().__init__(dataset, threshold, k)
        # Modification ici pour doubler le nombre de compétences
        self.nb_skills = len(dataset.skills) * 2
        # Mettre à jour l'espace d'observation pour refléter le nouveau nombre de compétences
        self.observation_space = gym.spaces.Box(low=0, high=self.max_level, shape=(self.nb_skills,), dtype=np.int32)
        self.min_skills_job = min([len(job) for job in dataset.jobs])
        self.max_skills_job = max([len(job) for job in dataset.jobs])

        print(self.observation_space)

    
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

        #attention
        if course_successful:
            for skill, level in course[1]:
                self._agent_skills[skill] = max(self._agent_skills[skill], level)

        observation = self._get_obs()
        job_wanted = self.Dataset_son_reward.get_learner_job_wanted(tmp_learner)
        reward = learner_job_matching(learner, job_wanted) if course_successful else -1  # adjust reward based on course success
        self.nb_recommendations += 1
        terminated = self.nb_recommendations == self.k

        return observation, reward, terminated, False, info


    
    def _get_obs(self):
        """Method required by the gym environment. It returns the current observation of the environment.

        Returns:
            np.array: the current observation of the environment, that is the learner's skills
        """
        return self._agent_skills
    
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
            self._agent_skills = self.get_random_env()
        self.nb_recommendations = 0
        observation = self._get_obs()
        info = self._get_info()
        return observation, info

    def get_random_env(self):
        learner = self.get_random_learner()
        job_wanted = self.get_random_job()
        initial_skills = np.zeros(self.nb_skills, dtype=np.int32)
        initial_skills[:len(learner)] = learner
        initial_skills[len(learner):] = job_wanted
        print(ici)
        return initial_skills

    def get_random_learner(self):
        """Creates a random learner with a random number of skills and levels. This method is used to initialize the environment.

        Returns:
            np.array: the initial observation of the environment, that is the learner's initial skills
        """
        # Choose the number of skills the agent has randomly
        n_skills = random.randint(self.min_skills, self.max_skills)
        initial_skills = np.zeros(int(self.nb_skills/2), dtype=np.int32)
        skills = np.random.choice(int(self.nb_skills/2), size=n_skills, replace=False)
        
        levels = np.random.choice(
            self.mastery_levels,
            n_skills,
            replace=True,
        )
        for skill, level in zip(skills, levels):
            initial_skills[skill] = level
        return initial_skills

    def get_random_job(self):
        """Creates a random job with a random number of required skills and levels. This method is used to initialize the environment.

        Returns:
            np.array: the job's required skills
        """
        # Choose the number of required skills for the job randomly
        n_skills = random.randint(self.min_skills_job, self.max_skills_job)
        required_skills = np.zeros(int(self.nb_skills/2), dtype=np.int32)
        skills = np.random.choice(int(self.nb_skills/2), size=n_skills, replace=False)

        levels = np.random.choice(
            self.mastery_levels,
            n_skills,
            replace=True,
        )
        for skill, level in zip(skills, levels):
            required_skills[skill] = level
        return required_skills

class EvaluateCallback_reward(EvaluateCallback):
    # The EvaluateCallback class is a callback that evaluates the model at regular intervals during the training.
        def __init__(self, eval_env, eval_freq, all_results_filename, verbose=1):
            super().__init__(eval_env, eval_freq, all_results_filename,verbose)
            self.eval_env = eval_env
            self.eval_freq = eval_freq
            self.all_results_filename = all_results_filename
            self.mode = "w"

        def _on_step(self):
            """Method required by the callback. It is called at each step of the training. It evaluates the model every eval_freq steps.

            Returns:
                bool: Always returns True to continue training
            """
            if self.n_calls % self.eval_freq == 0:
                time_start = time.time()
                avg_jobs = 0
                for learner in self.eval_env.dataset.learners:
    
                    tmp_avg_jobs = self.eval_env.dataset.get_average_matching_job_learners()
                    avg_jobs += tmp_avg_jobs
                time_end = time.time()
                print(
                    f"Iteration {self.n_calls}. Average matching job and learners: {avg_jobs / len(self.eval_env.dataset.learners)} Time: {time_end - time_start}"
                )
                with open(
                    os.path.join(
                        self.eval_env.dataset.config["results_path"],
                        self.all_results_filename,
                    ),
                    self.mode,
                ) as f:
                    f.write(
                        str(self.n_calls)
                        + " "
                        + str(avg_jobs / len(self.eval_env.dataset.learners))
                        + " "
                        + str(time_end - time_start)
                        + "\n"
                    )
                if self.mode == "w":
                    self.mode = "a"
            return True  # Return True to continue training
