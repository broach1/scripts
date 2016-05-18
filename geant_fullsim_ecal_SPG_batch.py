import os
import numpy as np

#loads array of random seeds from file
seed_array = np.loadtxt('seeds.txt',dtype='int',delimiter=',')

#the space below (lines 8-22) are for job options (ENE, EVTMAX, etc)
ENE=50e3
EVTMAX=100
BFIELD=0
PHIMIN=0
PHIMAX=6.28
VX=0
VY=0
VZ=0
i=1






from Gaudi.Configuration import *

# Data service
from Configurables import FCCDataSvc
podioevent = FCCDataSvc("EventDataSvc")

# Magnetic field
from Configurables import G4ConstantMagneticFieldTool
if BFIELD==1:
    field = G4ConstantMagneticFieldTool("G4ConstantMagneticFieldTool",FieldOn=True)
else: 
    field = G4ConstantMagneticFieldTool("G4ConstantMagneticFieldTool",FieldOn=False)
 

# DD4hep geometry service
# Parses the given xml file
from Configurables import GeoSvc
geoservice = GeoSvc("GeoSvc", detectors=['file:DetectorDescription/Detectors/compact/FCChh_DectMaster.xml',
                                         'file:DetectorDescription/Detectors/compact/FCChh_ECalBarrel_Mockup.xml'
                                        ],
                    OutputLevel = INFO)

# Geant4 service
# Configures the Geant simulation: geometry, physics list and user actions
from Configurables import G4SimSvc, G4SingleParticleGeneratorTool 
# Configures the Geant simulation: geometry, physics list and user actions
geantservice = G4SimSvc("G4SimSvc", detector='G4DD4hepDetector', physicslist="G4FtfpBert",
particleGenerator=G4SingleParticleGeneratorTool("G4SingleParticleGeneratorTool",
                ParticleName="e-",eMin=ENE,eMax=ENE,etaMin=0.25,etaMax=0.25,phiMin=PHIMIN,phiMax=PHIMAX,VertexX=VX,VertexY=VY,VertexZ=VZ),
                actions="G4FullSimActions") 

geantservice.G4commands += ["/random/setSeeds "+str(seed_array[i-1])+" 0"]
#since the loop to generate the subjobs begins with 1, we need (i-1) to index


# Geant4 algorithm
# Translates EDM to G4Event, passes the event to G4, writes out outputs via tools
from Configurables import G4SimAlg, G4SaveCalHits
# and a tool that saves the calorimeter hits with a name "G4SaveCalHits/saveHCalHits"
#savehcaltool = G4SaveCalHits("saveHCalHits", caloType = "HCal")
#savehcaltool.DataOutputs.caloClusters.Path = "HCalClusters"
#savehcaltool.DataOutputs.caloHits.Path = "HCalHits"

saveecaltool = G4SaveCalHits("saveECalHits", caloType = "ECal")
saveecaltool.DataOutputs.caloClusters.Path = "ECalClusters"
saveecaltool.DataOutputs.caloHits.Path = "ECalHits"

# next, create the G4 algorithm, giving the list of names of tools ("XX/YY")
geantsim = G4SimAlg("G4SimAlg",
                        outputs= [#"G4SaveCalHits/saveHCalHits",
"G4SaveCalHits/saveECalHits"])

# PODIO algorithm
from Configurables import PodioOutput
out = PodioOutput("out",
                   OutputLevel=INFO)
out.outputCommands = ["keep *"]

# ApplicationMgr
from Configurables import ApplicationMgr
ApplicationMgr( TopAlg = [geantsim, out],
                EvtSel = 'NONE',
                EvtMax   = EVTMAX,
                # order is important, as GeoSvc is needed by G4SimSvc
                ExtSvc = [podioevent, geoservice, geantservice],
                OutputLevel=INFO
)
