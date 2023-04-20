#!/bin/bash
#SBATCH --time=03-00
#SBATCH --account=def-punithak
#SBATCH --mem=100g
#SBATCH --nodes=1
#SBATCH --gpus-per-node=p100:1
#SBATCH --cpus-per-task=20
#SBATCH --mail-type=END
#$BATCH --mail-type=BEGIN
echo 'starting job'
START_TIME=$(date +%s)
source ../env/bin/activate
echo $(python --version)
python DQN.py --task train --files data/echoFusion/filenames/image_files.txt data/echoFusion/filenames/landmark_files.txt --model_name Network3d --file_type fetal --landmarks 0 0 0 0 0 --multiscale --viz 0 --train_freq 50 --write --max_episodes 20000 --memory_size 100000 --init_memory_size 30000
echo 'finished job'
END_TIME=$(date +%s)
echo "It took $(($END_TIME - $START_TIME)) seconds"
