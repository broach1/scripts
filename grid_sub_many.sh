#!/bin/bash

#copy the correct file to the detector area to prepare for run
#also name the output dataset
LAR=4.24
LEAD=2.44
NTOT=1000
E=20 #GeV
#cp ../new_ecal/${SM}mm/out_LAR${LAR}_LEAD${LEAD}.xml DetectorDescription/Detectors/compact/FCChh_ECalDefinition.xml


i=1
TOT=1
while [ $i -le $TOT ]
do
echo $i >> iteration.txt
prun --exec ". ./grid_test.sh" --cmtConfig=x86_64-slc6-gcc49-opt --site=CERN-PROD --outDS user.broach.e${E}_LAR${LAR}_LEAD${LEAD}_NTOT${NTOT}_BFIELD0_PART${i}_OF_${TOT} --outputs output.root
#./run gaudirun.py geant_fullsim_ecal_SPG_batch.py
echo user.broach.e${E}_LAR${LAR}_LEAD${LEAD}_NTOT${NTOT}_BFIELD0_PART${i}_OF_${TOT}
i=$[$i+1]
rm iteration.txt

done
