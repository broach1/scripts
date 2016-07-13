Scripts
-------

Contains useful scripts for running code on Grid. Files not included in this README should be viewed with caution, as they may be out of date or not at all useful!

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

martin_notebook.C
-----------
Conversion of Martin Aleksa's Mathematica notebook to ROOT macro. Best run on LXPLUS; remember to source init.sh first. Calculates the sampling term as a function of LAr and lead in layers, among other things.

fullsim.py
-----------
Configuration file for use in the ./run gaudirun.py fullsim.py command. Currently configured for ECAL standalone. Imports seeds.txt with numpy.

seeds.txt
-----------
Contains a list of 500 random seeds, designed to be imported by numpy in the .py configuration file for use in the single particle gun.

submit_jobs.sh
-----------
Submits jobs to run on the LSF batch server.

prepare_batch.sh
-----------
Called by submit_jobs.sh; copies the FCCSW directory to LSF batch (including the build directories - no need to recompile!) and runs the code from the parameters specified in submit_jobs.sh .

sig_e_over_e.py
-----------
Takes processed root files from ECAL standalone and extracts the resolution and fits it as a function of energy (i.e. sigma/E = a/sqrt(E) \quadr C).