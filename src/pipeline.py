import os
import argparse

import yaml

from Dataset import Dataset
from Dataset_son_reward import Dataset_son_reward
from Greedy import Greedy
from Greedy_reward import Greedy_reward
from Optimal import Optimal
from Optimal_reward import Optimal_reward
from Reinforce import Reinforce
from Reinforce_reward import Reinforce_reward



def create_and_print_dataset(config):
    """Create and print the dataset."""
    if config["type"]=="proba":
        dataset = Dataset(config)
    elif config["type"]=="reward":
        dataset = Dataset_son_reward(config)
    print(dataset)
    return dataset


def main():
    """Run the recommender system based on the provided model and parameters."""
    parser = argparse.ArgumentParser(description="Run recommender models.")

    parser.add_argument("--config", help="Path to the configuration file", default = "config/run.yaml")

    args = parser.parse_args()


    with open(args.config, "r") as f:
        config = yaml.load(f, Loader=yaml.FullLoader)

    # If the class is reward, we use the reward models, otherwise we use the regular models
    if config["type"]=="reward":
        model_classes = {
        "greedy": Greedy_reward,
        "optimal": Optimal_reward,
        "ppo": Reinforce_reward,
        "dqn": Reinforce_reward,
        "a2c": Reinforce_reward,
    }

    else:
        model_classes = {
            "greedy": Greedy,
            "optimal": Optimal,
            "a2c": Reinforce,
            "ppo": Reinforce,
            "dqn": Reinforce,
        }

    for run in range(config["nb_runs"]):
        dataset = create_and_print_dataset(config)
        # If the model is greedy or optimal, we use the corresponding class defined in Greedy.py and Optimal.py
        if config["model"] in ["greedy", "optimal"]:
            recommender = model_classes[config["model"]](dataset, config["threshold"])
            recommendation_method = getattr(
                recommender, f'{config["model"]}_recommendation'
            )
            recommendation_method(config["k"], run)
        # Otherwise, we use the Reinforce class, described in Reinforce.py
        else:
            recommender = model_classes[config["model"]](
                dataset,
                config["model"], 
                config["k"], 
                config["threshold"],
                run,
                config["total_steps"],
                config["eval_freq"],
            )
            recommender.reinforce_recommendation()


if __name__ == "__main__":
    main()
