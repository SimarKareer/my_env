#!/bin/bash
#SBATCH --job-name=lwarpv7_$1
#SBATCH --output=lwarpv7_$1.out
#SBATCH --error=lwarpv7_$1.err
#SBATCH --gres=gpu:$2
#SBATCH --ntasks=$2
#SBATCH --ntasks-per-node=$2
#SBATCH --cpus-per-task=15
#SBATCH --constraint="a40"
#SBATCH --partition=short
#SBATCH --requeue
#SBATCH --open-mode=append
#SBATCH --exclude="ig-88,perseverance,cheetah,claptrap"

export PYTHONUNBUFFERED=TRUE
export MASTER_PORT=$P
source ~/.bashrc
conda activate micExp
cd ~/flash/Projects/VideoDA/experiments/mmsegmentationExps

set -x
srun -u python -u tools/train.py ./configs/mic/viperHR2csHR_mic_hrda.py --launcher="slurm" --l-warp-lambda=1.0 --l-warp-begin=0 --l-mix-lambda=0.0 --consis-filter True --warp-cutmix True --bottom-pl-fill True --work-dir="./work_dirs/lwarpv7/$1$T" --auto-resume True --wandbid $1$T --load-from=/coc/testnvme/skareer6/Projects/VideoDA/mmsegmentation/work_dirs/lwarp/1gbaseline/iter_40000.pth