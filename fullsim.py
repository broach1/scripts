import os
import numpy as np

#loads array of random seeds from file
seed_array = np.loadtxt('seeds.txt',dtype='int',delimiter=',')

#the space below (lines 8-22) are for job options (ENE, EVTMAX, etc)
ENE=20e3
EVTMAX=1000
BFIELD=0
PHIMIN=0
PHIMAX=6.28
VX=0
VY=0
VZ=0
i=33
CLUSTER=0







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
from Configurables import GeoSvc, G4SingleParticleGeneratorTool
geoservice = GeoSvc("GeoSvc", detectors=['file:Detector/DetFCChhBaseline1/compact/FCChh_DectEmptyMaster.xml',
                                         'file:Detector/DetFCChhECalSimple/compact/FCChh_ECalBarrel_Mockup.xml'],
                    OutputLevel = ERROR)


# Geant4 service
# Configures the Geant simulation: geometry, physics list and user actions
from Configurables import G4SimSvc
# giving the names of tools will initialize the tools of that type
geantservice = G4SimSvc("G4SimSvc", detector='G4DD4hepDetector', physicslist="G4FtfpBert", actions="G4FullSimActions")

# Geant4 algorithm
# Translates EDM to G4Event, passes the event to G4, writes out outputs via tools
from Configurables import G4SimAlg, G4SaveCalHits
# first, create a tool that saves the tracker hits
# Name of that tool in GAUDI is "XX/YY" where XX is the tool class name ("G4SaveTrackerHits")
# and YY is the given name ("saveTrackerHits")
saveecaltool = G4SaveCalHits("saveCalHits")
saveecaltool.DataOutputs.caloClusters.Path = "ECalClusters"
saveecaltool.DataOutputs.caloHits.Path = "ECalHits"
#saveecaltool.DataOutputs.trackHitsClusters.Path = "hitClusterAssociation"
# next, create the G4 algorithm, giving the list of names of tools ("XX/YY")
pgun = G4SingleParticleGeneratorTool("gun", saveEdm=True, etaMin=-0.01, etaMax=0.01, phiMin=PHIMIN, phiMax=PHIMAX, energyMin=ENE, energyMax=ENE, particleName="e-")
#pgun.DataOutputs.genParticles.Path = "genParticles"
geantsim = G4SimAlg("G4SimAlg",
                    outputs= ["G4SaveCalHits/saveCalHits" ],
                    eventGenerator=pgun)



geantservice.G4commands += ["/random/setSeeds "+str(seed_array[i-1])+" 0"]
#since the loop to generate the subjobs begins with 1, we need (i-1) to index

#set range cuts
geantservice.G4commands += ["/run/setCut 0.1 mm"] 

# PODIO algorithm
from Configurables import PodioOutput
out = PodioOutput("out",
                   OutputLevel=INFO)

if CLUSTER==1: #otherwise use the generic name output.root for Grid runs
    out.filename = "/mnt/broach/e"+str(int(ENE/1e3))+"_part"+str(i)+"_lar"+str(LAR)+"_lead"+str(LEAD)+".root"

out.outputCommands = ["keep *"]

#CPU information
from Configurables import AuditorSvc, ChronoAuditor
chra = ChronoAuditor()
audsvc = AuditorSvc()
audsvc.Auditors = [chra]
geantsim.AuditExecute = True

# ApplicationMgr
from Configurables import ApplicationMgr
ApplicationMgr( TopAlg = [geantsim 
                          ,out
                          ],
                EvtSel = 'NONE',
                EvtMax   = EVTMAX,
                # order is important, as GeoSvc is needed by G4SimSvc
                ExtSvc = [podioevent, geoservice, geantservice, audsvc],
                OutputLevel=INFO
 )
