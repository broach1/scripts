#!/bin/bash

i=1             
#iteration number - begins with 1

NJOBS=4  
#total number of jobs to submit

LAR=4.5          
LEAD=1.5         
SM=6             
#mm
#SM=LAR+LEAD

NTOT=500         
#total number of events across all jobs: NTOT=EVTMAX*NJOBS

BFIELD=0         
#0 off, 1 on

ENE=20e3    
#MeV

EVTMAX=1      
#number of events in each job

PHIMIN=0    
PHIMAX=6.28           
#set phi range of generated particles

VX=0          
VY=0           
VZ=0
#set vertex coordinate of generated particle (mm)             

CLUSTER=1
#running on the FCC Cluster? 1 yes, 0 no

cp ../new_ecal_dim/${SM}mm/out_LAR${LAR}_LEAD${LEAD}.xml DetectorDescription/Detectors/compact/FCChh_ECalDefinition.xml

source init_fcc_stack.sh


while [ $i -le $NJOBS ]
do

cp geant_fullsim_ecal_SPG_batch.py geant_fullsim_ecal_SPG_batch$i.py

#add job options to the python script
sed -i "8s/.*/ENE=$ENE/g" geant_fullsim_ecal_SPG_batch$i.py 
sed -i "9s/.*/EVTMAX=$EVTMAX/g" geant_fullsim_ecal_SPG_batch$i.py 
sed -i "10s/.*/BFIELD=$BFIELD/g" geant_fullsim_ecal_SPG_batch$i.py 
sed -i "11s/.*/PHIMIN=$PHIMIN/g" geant_fullsim_ecal_SPG_batch$i.py 
sed -i "12s/.*/PHIMAX=$PHIMAX/g" geant_fullsim_ecal_SPG_batch$i.py 
sed -i "13s/.*/VX=$VX/g" geant_fullsim_ecal_SPG_batch$i.py 
sed -i "14s/.*/VY=$VY/g" geant_fullsim_ecal_SPG_batch$i.py 
sed -i "15s/.*/VZ=$VZ/g" geant_fullsim_ecal_SPG_batch$i.py 
sed -i "16s/.*/i=$i/g" geant_fullsim_ecal_SPG_batch$i.py
sed -i "17s/.*/CLUSTER=1/g" geant_fullsim_ecal_SPG_batch$i.py

./run gaudirun.py geant_fullsim_ecal_SPG_batch$i.py > output_$i.log 2>&1 &
i=$[$i+1]

done
