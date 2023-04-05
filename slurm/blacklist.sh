#!/bin/sh
# Script to run individual jobs
filter_cpu_avail_nodes() {
	sinfo --format '%20n %8O %e' | awk 'NR>1{if (($2 > 40.0) || ($3 < 120000)) print $1}' | paste -s -d, -
}
export BLACK_LIST_NODES=""
exclude_list() {
	exclude_str="$BLACK_LIST_NODES"
	filt_nodes=`filter_cpu_avail_nodes`
	if [ -z "$filt_nodes" ]; then
		true
	else
		if [ -z "$exclude_str" ]; then
			exclude_str="$filt_nodes"
		else
			exclude_str="$exclude_str,$filt_nodes"
		fi
	fi
	if [ -z "$exclude_str" ]; then
		printf $exclude_str
	else
		printf $exclude_str | sed 's/,/\n/g' | sort | uniq | paste -s -d, -
	fi
}

exclude=$(exclude_list)
# remove='ephemeral-'
# exclude=${exclude//$remove/}
# IFS=""
echo $exclude > excluded.txt

# sbatch -- export=params=${params}$ \
# 			   --output='logs/slurm/${ID}.logfile \
# 			   run_single_job.sh
