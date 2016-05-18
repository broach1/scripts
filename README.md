Scripts
-------

Contains useful scripts for running code on Grid.

grid_sub.sh
----------
Uses prun to submit a single job to Grid.


grid_sub_many.sh
-----------
Submits many jobs to Grid by looping over desired files and automatically naming the outDS. (Currently used to test modifications in the ratio of lead to LAr in the ECAL.)

grid_test.sh
-----------
Actually runs the job on the Grid. It sources the stack, builds the code, and runs the single particle gun to generate events.

change_ecal.sh
-----------
Generates new FCChh_ECalDefinition.xml files in a separate directory with differing values of LAr and lead thickness
