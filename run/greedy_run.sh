 cd ..
# Exécute les scripts Python avec différents fichiers de configuration
python src/pipeline.py --config config/run_greeddy_k1.yaml &
python src/pipeline.py --config config/run_greeddy_k2.yaml &
python src/pipeline.py --config config/run_greeddy_k3.yaml &
python src/pipeline.py --config config/run_greeddy_k4.yaml &
python src/pipeline.py --config config/run_greeddy_k5.yaml &
#./python src/pipeline.py --config config/run1.yaml
wait