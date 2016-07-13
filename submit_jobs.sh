#!/bin/bash

export JOB="fullsim.py"
export NEVT=500
export ENE=1000
export BFIELD=0
export PHIMIN=0
export PHIMAX=6.28
export NJOBS=12
export EVTMAX=834
export LAR=6
export LEAD=2
export VX=0
export VY=0
export VZ=0
export CLUSTER=0

i=1
SM=$[${LAR}+${LEAD}]

#make sure the geometry is correct
cp /afs/cern.ch/user/b/broach/FCCSW_updated/new_ecal_dim/${SM}mm/out_LAR${LAR}_LEAD${LEAD}.xml /afs/cern.ch/user/b/broach/FCCSW_updated/FCCSW/Detector/DetFCChhECalSimple/compact/FCChh_ECalDefinition.xml


#option -n 8 -R "span[hosts=1]" for running in parallel


while [ $i -le $NJOBS ]
do
    
    export i
    echo "submitting job $i of $NJOBS"
    bsub -q 1nd prepare_batch.sh ${JOB} ${NEVT} ${ENE} ${BFIELD} ${PHIMIN} ${PHIMAX} ${NJOBS} ${EVTMAX} ${LAR} ${LEAD} ${VX} ${VY} ${VZ} ${i} ${CLUSTER}

i=$[$i+1]
done
