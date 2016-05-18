#!/bin/sh
#manually generate desired combiations of lead and LAr for FCChh ECAL studies

flag=1
TOT=6 #mm, total thickness of layer (LAR + LEAD)

#output files are directed to a directory ../new_ecal/${TOT}mm
#Grid sometimes has issues with new directories, so this directory
#is created a level up from the job submission area
#(also to agree with the structure expected by grid_sub_many.sh )

if [ ! -d "../new_ecal_dim" ]; then
mkdir ../new_ecal_dim
fi

if [ ! -d "../new_ecal_dim/${TOT}mm" ]; then
mkdir ../new_ecal_dim/${TOT}mm
fi


while [ $flag -eq 1 ]
do

echo "input LAR (mm)"
read LAR

echo "input LEAD (mm)"
read LEAD

sed -e "s/4.24/$LAR/" FCChh_ECalDefinition.xml > test_LAR${LAR}_LEAD${LEAD}.xml
sed -e "s/2.44/$LEAD/" test_LAR${LAR}_LEAD${LEAD}.xml > ../new_ecal_dim/${TOT}mm/out_LAR${LAR}_LEAD${LEAD}.xml

echo "Enter 1 to continue; 0 to exit"
read flag

done

#cleanup
rm test_LAR*