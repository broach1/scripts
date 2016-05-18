#!/bin/bash

i=1              #iteration number - begins with 1
NJOBS=1          #total number of jobs to submit
LAR=3.5          #mm
LEAD=2.5         #mm
SM=6             #LAR + LEAD
NTOT=1000        #total number of events across all jobs: NTOT=EVTMAX*NJOBS
BFIELD=0         #0 off, 1 on
ENE=50e3         #MeV
EVTMAX=100       #number of events in each job
PHIMIN=0         #set phi range of generated particles
PHIMAX=6.28      # ...
VX=0             #set vertex X coordinate of generated particle (mm)
VY=0             # Y ...
VZ=0             # Z...

cp ../new_ecal_dim/${SM}mm/out_LAR${LAR}_LEAD${LEAD}.xml DetectorDescription/Detectors/compact/FCChh_ECalDefinition.xml


while [ $i -le $NJOBS ]
do

#add job options to the python script
sed -i "8s/.*/ENE=$ENE/g" geant_fullsim_ecal_SPG_batch.py 
sed -i "9s/.*/EVTMAX=$EVTMAX/g" geant_fullsim_ecal_SPG_batch.py 
sed -i "10s/.*/BFIELD=$BFIELD/g" geant_fullsim_ecal_SPG_batch.py 
sed -i "11s/.*/PHIMIN=$PHIMIN/g" geant_fullsim_ecal_SPG_batch.py 
sed -i "12s/.*/PHIMAX=$PHIMAX/g" geant_fullsim_ecal_SPG_batch.py 
sed -i "13s/.*/VX=$VX/g" geant_fullsim_ecal_SPG_batch.py 
sed -i "14s/.*/VY=$VY/g" geant_fullsim_ecal_SPG_batch.py 
sed -i "15s/.*/VZ=$VZ/g" geant_fullsim_ecal_SPG_batch.py 
sed -i "16s/.*/i=$i/g" geant_fullsim_ecal_SPG_batch.py 

#prun --exec ". ./grid_test.sh" --cmtConfig=x86_64-slc6-gcc49-opt --site=CERN-PROD --outDS user.broach.e${ENE}_LAR${LAR}_LEAD${LEAD}_NTOT${NTOT}_BFIELD${BFIELD}_PART${i}_OF_${NJOBS} --outputs output.root
./run gaudirun.py geant_fullsim_ecal_SPG_batch.py
echo user.broach.e${ENE}_LAR${LAR}_LEAD${LEAD}_NTOT${NTOT}_BFIELD${BFIELD}_PART${i}_OF_${NJOBS}
i=$[$i+1]

done
