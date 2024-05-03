# Job-market Oriented Course Recommendation System

# Cluster for free to use:
see:
https://scitas-doc.epfl.ch/user-guide/using-clusters/connecting-to-the-clusters/

```bash
ssh -A peyron@izar.epfl.ch # izar or jed
```
- Entrer mdp is-academia

# How to lauch, see, stop jobs:

- to launch a job:
```bash
sbatch run_simu.run
```
- Cancel a job:
```bash
scancel JOBID
```
- Squeue shows information about all your jobs:
```bash
Squeue
```
```bash
```
```bash

```



Repository of experiments for a job market oriented course recommender system. Ongoing project, more work is required.
## Docker use:
1. construire image docker:
```bash
docker build -t nom_de_votre_image:etiquette .
```
2. éxecuter conatiner précédement crée:
```bash
docker run --name nom_de_votre_conteneur nom_de_votre_image:etiquette
```
3. Si vous voilez voir le docker construit:pe
```bash
docker images
```

## Run:ai use on the ml4ed server:

Now let us login to the registry. (try with sudo if does not work)

```bash
docker login ic-registry.epfl.ch
```

1. construire image docker:
```bash
docker build -t nom_de_votre_image:etiquette . # ex: pval-sem-a2c:v1 .
```
2. lié les 2 noms suivant: 
```bash
docker tag  project_sem_a2c_k1:v1 ic-registry.epfl.ch/d-vet/pval-sem-a2c #name_kube a changer ex: ic-registry.epfl.ch/d-vet/pval-sem-a2c
```
3. Now we can push our image:

```bash
docker push ic-registry.epfl.ch/d-vet/pval-sem-a2c
```
4. Checking the existing RunAI projects

```bash
runai list project
```
How to check the job:

```bash
runai describe job hello1 -p ml4ed-peyron
```

Checking the logs:

```bash
 kubectl logs hello1-0-0 -n runai-ml4ed-peyron
```

How to get all jobs

```bash
runai list jobs -p ml4ed-peyron
```

How to delete the job:

```bash
runai delete job -p ml4ed-peyron pval-sem-a2c project-sem
```

5. Check the name of the Persistent Volumes you lab has access to:

```bash
kubectl get pvc -n runai-ml4ed-peyron
```
6. New way of launching a job on runai (change the yaml file with your IDs):

```bash
kubectl create -f kube.yaml
```
7. getting acces to the results: 
For ML4ED (ask me for the password):

```bash
ssh root@icvm0018.xaas.epfl.ch
```
mdp ml4ed: !Au2WazEr6!ZF!@6JjjY
and then it should be in: /mnt/ic1files_epfl_ch_u13722_ic_ml4ed_001_files_nfs


## Installation

Requires python 3.10

Install required packages via pip

```bash
pip install -r requirements.txt
```

## Usage

```bash
python src/pipeline.py --config config/run_test.yaml
```
(pour run plusieurs config différents avec python src/pipeline.py --config config/run.yaml créer un name.sh pour le lancer ./name.sh mettre a l'interieur et a la kingne:)
Below you will find a detailed description of the parameters of the config file

```yaml
taxonomy_path: data/taxonomy.csv # Path to the taxonomy file
course_path: data/courses.json # Path to the courses file
cv_path: data/resumes.json # Path to the resumes file
job_path: data/jobs.json # Path to the jobs file
mastery_levels_path: data/mastery_levels.json # Path to the mastery levels file
results_path: results # Path to the results directory where results are saved
level_3: true # Whether to use only the third level of the taxonomy and not the fourth  (if true: less skills)
nb_courses: 100 # Number of courses to use (set to -1 to use all)
nb_cvs: -1 # Number of resumes to use (set to -1 to use all)
max_cv_skills: 15 # Maximum number of skills per resume
nb_jobs: 100 # Number of jobs to use (set to -1 to use all)
threshold: 0.8 # Threshold for the similarities
k: 2 # Number of courses to recommend
model: greedy # Model to use (greedy, optimal, dqn, ppo, a2c)
total_steps: 500 # Total number of steps for the training of the agent
eval_freq: 5000 # Frequency of the evaluation of the agent
nb_runs: 1 # Number of runs (set to 1 for greedy and optimal since they are deterministic)
seed: 42 # Seed for the random number generator
```

## Renforcement learning framework for Job-Market Oriented Course Recommender

### Skill-based Modeling

- User $u$: vector of skills where each dimension corresponds to a skill and the value is the user's proficiency level.
- Job $j$: vector of skills where each dimension corresponds to a skill and the value is the job's required proficiency level.
- Course $c = (c_r, c_p)$: two vectors of skills where each dimension corresponds to a skill and the value is the course's required (resp. provided) proficiency level.

### MDP

- State user $u$
- Action space $\mathcal{C}$: the set of courses. One action being to recommend a course.
- Reward $r$: number of jobs the learner can apply to.
- Transition probabilities: binary, for now our MDP is deterministic. For a given action $c$ and state $u$, the outcome will always be the same: we update the state $u$ with the skills provided by the course: $c_p$.

### Relavance and similarity functions

TBD

## Description of src files

- [pipeline.py](src/pipeline.py): Trains and evaluate the agents, or heurisitc apporoaches.
- [Greedy.py](src/Greedy.py): Classe that implements the greedy recommendation strategy.
- [Optimal.py](src/Optimal.py): Classe that implements the optimal recommendation.
- [Reinforce.py](src/Reinforce.py): Classe that implements the training and evaluation of the Reinfrocement-based recommendation using agents from [stable_baselines3](https://stable-baselines3.readthedocs.io/en/master/).
- [CourseRecEnv.py](src/CourseRecEnv.py): Classe that implements the evironment for training the agents using the [gymnasium](https://gymnasium.farama.org/index.html) library.
- [Dataset.py](src/Dataset.py): Class that implments the dataset using resumes, courses and jobs.
- [matchings.py](src/matchings.py): Contains various matching, similarity, and relevance functions.

## Done 
- Changement Greedy_reward:
        - changer nb_applicable_jobs par learner_job_matching()
        - addapter la méthode get_course_recommendation() 
        - corriger les problèmes de compilation

- Pipeline:
    - Ajouts des considération du config pour le choix des classe reward ou non (greedy. optimal, dataset)
- Reinforce:
    - 
- Course Rec env_reward:
    -  Changer       self.nb_skills = len(dataset.skills) -> self.nb_skills = 2*len(dataset.skills) ¨
    - step()
            - changer le reward pour step()
            - Pour reward mon bur est de maximiser learner_job_matching() de matching donc dans step() on doit considérer       learner_job_matching comme reward.
    - Reset():
            - creer get_random_env() avec get_random_learner() get_random_job() attention nb skills max et min a detrerminer en fonctio des nombres de skills dasnn les jobs de jobs.json 
- Changement Optimal_Reward:
        - addapter la méthode get_course_recommendation() 
        - corriger les problèmes de compilation
- Changement classe dataset_son_reward:
    - Ajouter la considération sur les 2 possibles classe dataset dans pipelines
    - Déterminer quelles méthodes addapter dans la classe fille(considérant le reward)
    - addapter les méthodes nécessaire(load_learners(),)
    - vérifier que le bon dataset est considéré
    - Changement de datset considéré pour leraners de cv_path->cv_path_reward
    - changer dataset pour que self.learners_wanted[learner_id]  soit un dictionnsaire avec les skills du jobs  (chercher le dictionnaire des skills dans jobs) attentiuon a bien faire un dictionnaire.
    - retravailler le dataset, probléme avec lerners_wanted le format semble ne pas être le bon c'est un dictionnaire de dictionaire, et il semblerait que le forat voulu et liste de tuples comme on le voit dans lerners^. on peut imaginer regqrder la liste lerners.index pour changer l'allure de lerners_wanted tout en gardant les lerners_wanted au bonne position. (les changements ont étédans make_learners_index() pour avoir le bon format) 
    - Ajpout fonction get_average_matching_job_learners() permetant de calculer la moyenne des matching entre wanted job et profile.

- matchings:
    
- Autre: 
    - création et ajout  du datafiles resumes_reward ( création par data_reward_changes)
    - Création des classe filles et choix des méthodes a surchargées
    - ajout d'un paramétre a config pour différencier de proba modéle a reward modele
    - considération a travers les classe et pipeline du nouveau paramétres du config pour le choix des classes
    - Add the wanted position in the resume.json (jobs is a number between 15 and 21136) choose the wanted one for a profile at random.
    - scarp job pour creer le set de numero de job, pour le nouveau fdataset reume prendre les bons numeros de job.


## To DO 

- regarder tutoriel pour verifications des accés
- résoudre pb RL
- Change the callback for reward so its shows the matching avg between job and learner.
- 
- attention pb resume avev wanted job vide a considérer: pour ce cas on va supposer aue un wanted job vide est un job qui ne demande pas de skills que l'on peut apprendre avec des cours donc le matchings avec n'import quelle profile est de 1 dans ce cas.

## Question:
- Si pour le modele Reward on a pas de job (un job vide) que considéer on. j'ai opter pour ne pas considérer ces cas. dans optimal_reward  les job_wanmted vide sont passé.
