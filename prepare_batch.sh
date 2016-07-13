#!/bin/bash

# $1: joboption name (geant_fullsim_ecal_SPG_batch.py)
# $2: number of events to be processed
# $3: energy of generated particles (in GeV)
# $4: bfield on/off (1/0)
export JOB=$1
export NEVT=$2
export ENEGEV=$3
export ENEMEV=$[$ENEGEV * 1000]

#Conversion from GeV to MeV (energy must be in MeV for DD4hep)                                                                                            
#export ENEMEV=$(($ENEGEV * 1000))
export BFIELD=$4
export PHIMIN=$5
export PHIMAX=$6
export NJOBS=$7
export EVTMAX=$8
export LAR=$9
export LEAD=${10}
export VX=${11}
export VY=${12}
export VZ=${13}
export i=${14}
export CLUSTER=${15}

mkdir MyWorkDir
cd MyWorkDir 

# Copy entire run directory in my working place
mkdir FCCSW
cd FCCSW

cp -r /afs/cern.ch/user/b/broach/FCCSW_updated/FCCSW/* .


# List content of the working directory for debugging purposes
echo "ls -rtl "
ls -rtl

rm -rf submit_batch

# Prepare the joboption file (add the parameters on top)
sed -i "8s/.*/ENE=$ENEMEV/g" ${JOB} 
sed -i "9s/.*/EVTMAX=$EVTMAX/g" ${JOB} 
sed -i "10s/.*/BFIELD=$BFIELD/g" ${JOB} 
sed -i "11s/.*/PHIMIN=$PHIMIN/g" ${JOB} 
sed -i "12s/.*/PHIMAX=$PHIMAX/g" ${JOB} 
sed -i "13s/.*/VX=$VX/g" ${JOB} 
sed -i "14s/.*/VY=$VY/g" ${JOB} 
sed -i "15s/.*/VZ=$VZ/g" ${JOB} 
sed -i "16s/.*/i=$i/g" ${JOB}
sed -i "17s/.*/CLUSTER=$CLUSTER/g" ${JOB}
sed -i "18s/.*/LAR=$LAR/g" ${JOB}
sed -i "19s/.*/LEAD=$LEAD/g" ${JOB}


# Joboption file:
#echo "Joboption file content:"
#cat ${JOB}

less ${JOB}

# Setup & compile
#echo "Setting the enviroment"
#source init.sh
#echo "Compiling "
#make clean
#make -j 8

source /afs/cern.ch/user/b/broach/fcc_eos.sh

# Run the job
./run gaudirun.py ${JOB} | tee myjob.log

# Copy out the results if exist
if [ -e output.root ] ; then
xrdcp output.root root://eospublic//eos/fcc/users/b/broach/July11/e${ENEGEV}_n${NEVT}_lar${LAR}_lead${LEAD}_part${i}.root
xrdcp myjob.log root://eospublic//eos/fcc/users/b/broach/July11/myjob_ecal_bfield${BFIELD}_e${ENEGEV}GeV_n${NEVT}_lar${LAR}_lead${LEAD}_part${i}.log
fi
 
# Clean workspace before exit
cd ../..
rm -rf MyWorkDir
