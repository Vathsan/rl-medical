#!/bin/bash
#SBATCH --time=05-00
#SBATCH --account=def-punithak
#SBATCH --mem=100g
#SBATCH --nodes=1
#SBATCH --gpus-per-node=a100:1
#SBATCH --cpus-per-task=16
#SBATCH --mail-type=END
#$BATCH --mail-type=BEGIN
echo 'starting job'
START_TIME=$(date +%s)
source ../env/bin/activate
echo $(python --version)
python DQN.py --task train --files data/echoFusion/filenames/image_files.txt data/echoFusion/filenames/landmark_files.txt --model_name CommNet --file_type fetal --landmarks 0 0 0 1 1 1 2 2 2 --multiscale --viz 0 --train_freq 50 --write --max_episodes 40000 --memory_size 64000 --init_memory_size 20000
echo 'finished job'
END_TIME=$(date +%s)
echo "It took $(($END_TIME - $START_TIME)) seconds"
