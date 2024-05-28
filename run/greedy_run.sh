 cd ..
# Exécute les scripts Python avec différents fichiers de configuration
python src/pipeline.py --config config/run_greedy_k1.yaml &
python src/pipeline.py --config config/run_greedy_k2.yaml &
python src/pipeline.py --config config/run_greedy_k3.yaml &
python src/pipeline.py --config config/run_greedy_k4.yaml &
python src/pipeline.py --config config/run_greedy_k5.yaml &
#./python src/pipeline.py --config config/run1.yaml
wait