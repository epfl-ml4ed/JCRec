# Utiliser l'image de base Python 3.10
FROM python:3.10

# Définir le répertoire de travail
WORKDIR /tmp


# Installer les packages requis via pip
COPY requirements.txt .

RUN pip install -r requirements.txt

# Copier les fichiers source et de configuration dans le conteneur
COPY src/ src
COPY config/ config
COPY entrypoint.sh .
COPY data/ data
COPY run/ run

#RUN chmod -R 777 data
RUN chmod -R 777 src
#RUN chmod -R 777 config
RUN chmod -R 777 run

RUN chmod +x run/a2c_run.sh

# Donner les permissions d'exécution au script run.sh
RUN chmod 777 entrypoint.sh

# Créer un dossier pour les résultats des simulations
RUN mkdir results && chmod 777 results

# Commande à exécuter lorsque le conteneur démarre
CMD ["/bin/bash", "entrypoint.sh"]




