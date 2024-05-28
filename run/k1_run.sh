cd ..
# Exécute les scripts Python avec différents fichiers de configuration
python src/pipeline.py --config config/run_a2c_k1.yaml &
python src/pipeline.py --config config/run_ppo_k1.yaml &
python src/pipeline.py --config config/run_dqn_k1.yaml &

wait