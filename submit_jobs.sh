#!/bin/bash

export JOB="fullsim.py"
export NEVT=10000
export ENE=1000
export BFIELD=0
export PHIMIN=0
export PHIMAX=6.28
export NJOBS=20
export EVTMAX=250
export LAR=3
export LEAD=2
export VX=0
export VY=0
export VZ=0
export CLUSTER=0

i=${NJOBS}
SM=$[${LAR}+${LEAD}]

#make sure the geometry is correct
#cp ../../new_ecal_dim/${SM}mm/out_LAR${LAR}_LEAD${LEAD}.xml ../Detector/DetFCChhECalSimple/compact/FCChh_ECalDefinition.xml


#option -n 8 -R "span[hosts=1]" for running in parallel


while [ $i -le $NJOBS ]
do
    
    export i
    echo "submitting job $i of $NJOBS"
    bsub -q 1nd prepare_batch.sh ${JOB} ${NEVT} ${ENE} ${BFIELD} ${PHIMIN} ${PHIMAX} ${NJOBS} ${EVTMAX} ${LAR} ${LEAD} ${VX} ${VY} ${VZ} ${i} ${CLUSTER}

i=$[$i+1]
done
