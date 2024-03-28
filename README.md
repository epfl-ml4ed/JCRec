# Job-market Oriented Course Recommendation System

Repository of experiments for a job market oriented course recommender system. Ongoing project, more work is required.

## Installation

Requires python 3.10

Install required packages via pip

```bash
pip install -r requirements.txt
```

## Usage

```bash
python src/pipeline.py --config config/run.yaml
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


## To DO 
1. create a mother class for courserecenv to transfer the step() and reset() method to the different child class. First do a version with the probability








1. **Révisez la récompense dans la fonction `step` pour mieux refléter l'impact de la réussite de l'apprentissage.**

2. **Mettez en place un pipeline pour évaluer l'efficacité de la fonction `step` originale par rapport à celle améliorée.**
    Le code sera dans le fichier run_viz
   - **Question :**
     - Comment ajuster les étapes pour une visualisation des performances ?
     - Quelles données issues des exécutions sont pertinentes pour une visualisation ?

3. **Intégrez dans la récompense une considération pour l'adéquation avec le poste souhaité par le profil.**

4. **Consultez Jibril sur la manière d'évaluer le modèle, comment l'utiliser sur un profil spécifique, et comment télécharger le modèle entraîné.**

---

Pour ajuster les étapes en vue d'une visualisation des performances et identifier les données pertinentes pour une telle visualisation :

- **Ajustement pour Visualisation** : Implémentez des métriques de suivi à chaque étape de l'exécution, comme la récompense accumulée, la précision de la correspondance emploi-profil après chaque cours recommandé, et le nombre de cours nécessaires pour atteindre un certain seuil de réussite. Utilisez ces métriques pour tracer des courbes d'apprentissage ou des histogrammes de distribution des scores.

- **Données Pertinentes pour Visualisation** : Les données d'intérêt pourraient inclure la récompense totale par épisode, le nombre d'étapes nécessaires pour terminer un épisode, la progression des compétences de l'apprenant au fil du temps, et la fréquence de réussite des cours. Comparer ces données avant et après l'amélioration de la fonction `step` peut révéler l'efficacité des ajustements apportés.k with Jibril how to check the model, how to use it on a profile, how to ownload the trained model.

