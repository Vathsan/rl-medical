#!/bin/bash
#SBATCH --time=03:00:00
#SBATCH --account=def-punithak
#SBATCH --mem=32g
#SBATCH --nodes=1
#SBATCH --gres=gpu:1
#SBATCH --cpus-per-task=16
#SBATCH --mail-type=END
#$BATCH --mail-type=BEGIN
echo 'starting job'
START_TIME=$(date +%s)
source ../env/bin/activate
echo $(python --version)
python DQN.py --task train --files data/filenames/image_files.txt data/filenames/landmark_files.txt --model_name CommNet --file_type brain --landmarks 0 --multiscale --viz 0 --train_freq 50 --write --memory_size 32000 --init_memory_size 24000
echo 'finished job'
END_TIME=$(date +%s)
echo "It took $(($END_TIME - $START_TIME)) seconds"
