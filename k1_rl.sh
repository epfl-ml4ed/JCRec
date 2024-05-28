#!/bin/bash
#SBATCH --job-name=a2c_reward_petit
#SBATCH --nodes=1
#SBATCH --ntasks=3
#SBATCH --cpus-per-task=4
#SBATCH --time=10:00:00
#SBATCH --gres=gpu:3     # je demande 5 GPU au total, un pour chaque tâche

# on navigue vers le répertoire contenant le script bash
#cd "$(dirname "$0")"

# On exécute le script a2c_run.sh 
bash entrypoint.sh k1_run.sh