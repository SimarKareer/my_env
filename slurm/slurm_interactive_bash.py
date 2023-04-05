import os
import argparse

parser = argparse.ArgumentParser()
parser.add_argument(
    '-n','--job_name', type=str, default='bash', help='name to give job'
)
parser.add_argument(
    '-c','--num_cpus', type=int, default=15, help='number of cpus to allocate to the job'
)
parser.add_argument(
    '-e','--exclude', type=str, default="", help='list of nodes to avoid, separated by commas'
)
parser.add_argument(
    '-w','--want', type=str, default='', help='name of node that you want to run the job on'
)
parser.add_argument(
    '-p','--partition', type=str, default='short', help='partition to run the job on'
)
parser.add_argument(
    '-o','--overcap', action='store_true', help='indicates submission to overcap partition'
)
# parser.add_argument(
#     '-q','--quadro', action='store_true', help='indicates desire to use a node with Quadro cards'
# )
parser.add_argument(
    '-g', '--gpu', type=str, default="", help="constaints"
)

parser.add_argument(
    '-ng', '--numgpu', type=int, default=1, help="num gpu"
)

args = parser.parse_args()

#--nodes 1 --ntasks {args.numgpu}
cmd = (
    f"srun --gres gpu:{args.numgpu}"
    f" --cpus-per-task {args.num_cpus}"
)

if args.exclude:
    cmd += " --exclude {args.exclude}"

if args.overcap:
    cmd += " --account overcap --partition overcap"
else:
    cmd += f" --partition {args.partition}"

if args.job_name != '':
    cmd += f' --job-name {args.job_name}'

if args.want != '':
    cmd += f' -w {args.want}'

# if args.quadro:
#     cmd += f' --constraint claptrap,glados,olivaw,oppy,sophon,zima'

if args.gpu != "":
    cmd += f' --constraint={args.gpu}'

cmd += " --pty bash"

print("Executing: ", cmd)

os.system(cmd)
