import subprocess
import sys
import time

r="""#!/bin/bash
########################################################################
# SUN Grid Engine job wrapper
# parallel job on opteron queue
########################################################################
#$ -N icsdSearch
#$ -pe mpi2_14 1
#$ -q wp04
#$ -j y
#$ -M 3juholee@physics.rutgers.edu
#$ -m e
#$ -v LD_LIBRARY_PATH
########################################################################
# DON'T remove the following line!
source $TMPDIR/sge_init.sh
########################################################################
source ~/.bashrc
export SMPD_OPTION_NO_DYNAMIC_HOSTS=1
export OMP_NUM_THREADS=1
"""

def submit(start,end):
    subfile='jsub.src'
    with open(subfile,'w') as f:
        print >>f, r
        print >>f, 'python api_aflowlib.py --start %d --end %d' %(start,end)

    cmd='qsub '+subfile
    p = subprocess.Popen(cmd,shell=True,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE, close_fds=True)
    stdin, stdout, stderr = (p.stdin,p.stdout,p.stderr)
    print stdout.read(), stderr.read()
    

nlist=30005
ncore=20
nstep=nlist/ncore
start=0
end=nstep
while start<nlist:
    submit(start,min(end,nlist))
    start=end
    end=end+nstep
    print start
    time.sleep(30)

