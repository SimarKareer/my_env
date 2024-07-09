import subprocess
import sys
import os
import time
import random



dont_save = False
overcap = False
args = sys.argv[1:]

if '-d' in args:
    args = [a for a in args if a != '-d']
    dont_save = True

if '-b' in args:
    os.system("sh /coc/testnvme/skareer6/home/my_env/slurm/blacklist.sh")
    args = [f for f in args if f != '-b']

if '-o' in args:
    overcap = True
    args = [f for f in args if f != '-o']

sbatch_file = args[0]

args = [f for f in args if f != sbatch_file]


with open(sbatch_file) as f:
    data = f.read()

if overcap:
    data = data.replace('--partition=short', '--partition=overcap')
    data = data.replace('--partition=long', '--partition=overcap')
    overcap_string = "#SBATCH --account=overcap\n"
    last_sbatch_loc = data.rfind("#SBATCH")
    newline = data[last_sbatch_loc:].find("\n")
    data = data[:last_sbatch_loc+newline+1] + overcap_string + data[last_sbatch_loc+newline+1:]

for idx, arg in enumerate(args):
    data = data.replace(f'${idx+1}', arg)

# replace all instances of $T with a string of the current time formatted as %Y%m%d_%H%M%S
data = data.replace('$T', time.strftime('%m-%d-%H-%M-%S'))

data = data.replace("$P", f"{random.randint(26000, 40000)}")

# Create and delete a temporary file
temp_file = sbatch_file.replace('.sh', '_'+'_'.join(args)+'.sh')

with open(temp_file, 'w') as f:
    f.write(data)
try:
    subprocess.check_call(['sbatch', temp_file])
except:
    print('sbatch failed!!')

if dont_save:
    os.remove(temp_file)
