#!/bin/bash

# Navigue dans le dossier results
cd results

# Supprime tout sauf le fichier .gitignore
find . -not -name '.gitignore' -delete

# Retourne au dossier parent
cd ..

# Exécute les scripts Python avec différents fichiers de configuration
python src/pipeline.py --config config/run.yaml
#./python src/pipeline.py --config config/run1.yaml
