#!/bin/bash

config1='{
    "model":"RecVAE", "mlp_hidden_size":[64], "epochs":1, "eval_batch_size":2048, "train_batch_size":2048, 
    "data_path": "./train_model/dataset",
    "dataset": "wyoming",
    "eval_args": {
        "split": {"RS": [0.8, 0.1, 0.1]},
        "order": "RO",
        "group_by": "user",
        "mode": {"valid": "uni100", "test": "uni100"},
        "valid_neg_sample_args": {"distribution": "uniform", "sample_num": 1},
        "test_neg_sample_args": {"distribution": "uniform", "sample_num": 1}
    },
    "metrics": ["Recall", "MRR", "NDCG", "Hit", "Precision"]}'

for config in "$config1"
do
    python run_vae_experiment.py "$config"
done