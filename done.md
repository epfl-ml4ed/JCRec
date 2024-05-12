# Titre de votre projet

## Introduction

Ce projet vise à développer un système de conseil pour aider les individus à sélectionner les cours les plus pertinents afin de maximiser leur employabilité. Pour atteindre cet objectif, nous avons conçu un environnement Gymnasium spécifique où différents profils peuvent être simulés et testés. En intégrant la considération probabiliste dans des modèles d'apprentissage par renforcement (RL), nous développons des algorithmes capables de prendre des décisions optimales en tenant compte de la probabilité des résultats de leurs actions et de l'impact potentiel de chaque cours sur l'employabilité de l'utilisateur.

En exploitant les techniques avancées de modélisation RL, nous souhaitons fournir des recommandations personnalisées et adaptatives qui prennent en compte non seulement les tendances actuelles du marché de l'emploi mais aussi les préférences et capacités individuelles des utilisateurs. Cela implique l'utilisation d'algorithmes capables d'évaluer l'efficacité des divers parcours éducatifs dans l'amélioration des perspectives d'emploi, rendant ainsi les choix de formation plus stratégiques et fondés sur des données probantes.

## Intégration de la considération probabiliste

- **Intégration au modèle RL :** À ce stade, la considération probabiliste a été intégrée avec succès au modèle RL. Cette intégration permet au modèle de mieux évaluer les conséquences potentielles de ses actions en prenant en compte leur incertitude. Elle a été ajouté a la methode step() comme une coisidération sur lenrequired matchings. Plus clairement le plus haut le matchings skills course le plus haut la probabilités de succés.
- **Intégration au modèle Greedy :**  la considération probabiliste a étl ajouté au modèle Greedy. cette améloiration est possible grasse au changement dans la méthode recommend_and_update de la classe greedy. En outre une considération sur la garde ou non 


### Prochaines étapes

- **Intégration au modèle Optimal :** De même, nous travaillerons à intégrer la considération probabiliste dans le modèle Optimal. pour cette classe il faudra mettre a jour la méthode get_course_recommendation pour ajouter la possibilités d'échouer un cours. 
- **Considération du reward :** Ajot d'un reward prenant en compte les desirs de l'utilisateurs.(on veut que le but de l'utuliateur soit pris en compte.)


## Conclusion

L'intégration de la considération probabiliste dans les modèles RL, Greedy, et Optimal, associée à notre objectif de conseiller les profils sur les meilleurs cours à prendre pour maximiser leur employabilité, représente une avancée significative dans notre projet. Elle ouvre la voie à des recommandations personnalisées plus robustes et efficaces, capables de guider les utilisateurs vers les choix de formation les plus stratégiques et fondés sur des données probantes.

#### Question:
- Est-il possible de comparer le nombre de jobs accessibles pour évaluer les améliorations des modèles et des méthodes greedy ?
- Faut-il conserver les cours échoués pour éviter de répéter les mêmes erreurs, ou les supprimer ?
- Je n'arrive pas à faire un push, je n'ai pas les accès : "Permission denied" sur le dépôt GitHub epfl-ml4ed/SkillMatch4CourseRec pour l'utilisateur valentinpey, erreur 403.
- Des difficultés à charger les modèles entraînés, ce qui pourrait devenir problématique.
- Problème avec la fréquence d'évaluation dans le modèle de RL, pas avec la méthode greedy : erreur si la fréquence d'évaluation est inférieure au nombre de steps, liée à la classe EvaluateCallback.
- Demande de clarifications sur le fonctionnement de la méthode de recommandation de cours optimal, en particulier sur la sélection des cours. Discuter avec Jibril pour mieux comprendre.