#JANA: variables ENE (energy in !!MeV), BFIELD (0,1), EVTMAX (number of events) to be defined before running

import os
import numpy as np
i = int(np.loadtxt('iteration.txt'))


#500 8-digit integers generated from random.org
#more random seeds than one could ever need
#next step - put this in a text file, which is then read with numpy
seed = [82774323, 75578453, 54717921, 44200772, 62432467, 28757934, 88786510, 69633919, 93057004, 50728325, 61627352, 96178638, 40069348, 34894385, 52750372, 42777201, 64164579, 45261592, 75336159, 31945576, 63455456, 43736865, 28750251, 88625930, 73039769, 71766593, 65608696, 57242644, 70814024, 66485693, 66731754, 82726880, 34005506, 73370890, 53823480, 70170964, 54785659, 32040841, 88864645, 60259552, 78503098, 67060793, 84081528, 72212120, 65671973, 74838095, 42147727, 67327148, 69318444, 18969293, 79259072, 15505283, 80231707, 13767997, 67771692, 16589983, 29718410, 39687328, 95189531, 81271134, 48682202, 87833159, 62898241, 33955802, 38219542, 88319217, 10941338, 66211493, 78064191, 15616417, 77216008, 62015704, 29900733, 58114431, 11987086, 84878515, 65998676, 76060371, 15327300, 87329158, 46807737, 20903973, 86769933, 31275526, 52659874, 19727448, 62312236, 47025909, 11089559, 17455036, 67021419, 42763771, 28040759, 66067913, 40187808, 73679689, 80334862, 74867369, 20284044, 47745438, 34572359, 88951364, 95872201, 93978096, 63373290, 82150108, 91669981, 89801731, 25806795, 70683769, 87990104, 57381815, 92477899, 87983384, 12128748, 31971238, 90552791, 61053112, 64849780, 36767155, 77078298, 82971916, 99512395, 50694317, 12754986, 35128843, 98132310, 45231216, 51931681, 34062376, 47119534, 65356258, 80930748, 24702528, 72431355, 22440720, 34079094, 34465659, 43683501, 48033184, 65371996, 46295817, 37389285, 90363929, 32657362, 77158758, 28315672, 15879989, 13182258, 14707258, 91855713, 91283843, 67330149, 78608593, 25483396, 38077454, 30164375, 16012918, 32483320, 81590448, 29589138, 20395370, 66566294, 19723171, 66467212, 47915108, 92505008, 69024017, 58754894, 28229974, 67670315, 40408795, 27798070, 11229252, 65133124, 10824290, 59548005, 82742869, 53798125, 68760012, 61218137, 63115326, 23908012, 45140589, 63444938, 42545564, 18811377, 95238910, 59690851, 47886243, 28260068, 31784125, 14887162, 17823304, 54333035, 27351728, 71989066, 43768216, 15461791, 95083975, 10180606, 96150026, 36490456, 56772006, 15435005, 27547107, 97952651, 45310660, 46314575, 44162245, 12208584, 90375466, 49870028, 28829948, 28937561, 93741741, 67439530, 59899603, 95871753, 63353170, 33138916, 41868070, 74596816, 50521565, 27732903, 70595589, 64568487, 77125393, 21063431, 61788856, 66389228, 66899088, 74881855, 97803454, 91601692, 39546034, 86866974, 80418508, 83255019, 34358276, 23246067, 85841194, 83043102, 54618129, 35732138, 29763533, 12135426, 63401370, 54135317, 36259792, 39349475, 93876134, 66087785, 71950967, 39505418, 40314320, 99738357, 61847645, 86782815, 28289152, 53233964, 72408071, 41939450, 28349009, 51724618, 15703655, 43085262, 68961776, 38532495, 66694412, 99727873, 96719413, 79589087, 81277210, 45833992, 85128816, 51107085, 87860675, 73063670, 99026550, 72813301, 81787786, 25882659, 80500261, 19267504, 76853816, 12122889, 80777847, 65503086, 76184372, 48032456, 30725191, 71978249, 39235989, 69990177, 66241347, 78471085, 23454494, 79850014, 63656948, 70220456, 54271865, 43844632, 44784214, 20480787, 50842760, 99824615, 29122350, 56547944, 77563318, 80844608, 34411323, 81076853, 43971004, 38899806, 70415367, 58576780, 66392551, 16693932, 70371457, 81775154, 27598476, 70216631, 12405533, 68522173, 46309192, 72275175, 74003472, 98716813, 56633320, 14865843, 19280741, 25118719, 36481733, 12183681, 33563428, 78644001, 47243985, 40566446, 47341423, 87329074, 95117316, 42103265, 14139943, 58284900, 99920496, 39239624, 18412340, 86868781, 60018933, 50830064, 34361330, 80016702, 94531091, 65158282, 58411966, 61360442, 68315114, 52806020, 27399277, 85449697, 53216043, 36793303, 35767954, 69889300, 31549080, 68273489, 88174634, 52573107, 63667322, 77343302, 76348401, 68696515, 40760456, 22561345, 15635401, 26161192, 72286616, 80061180, 69084105, 84801091, 63259570, 84304140, 48159222, 60924186, 55132219, 20126699, 73520779, 46816123, 93692457, 38233713, 76513331, 98256871, 17480291, 94568794, 71878855, 91486238, 75581480, 86601298, 91632616, 22834735, 32119236, 93037586, 62837769, 64200251, 16061521, 51467328, 18152711, 11323730, 61607409, 73234094, 85325274, 15150173, 81247922, 53295795, 83540866, 40272028, 14783656, 51968965, 98374844, 50609936, 24576668, 45593741, 65582225, 65120124, 62910113, 63564644, 70241816, 44528394, 71510769, 56768557, 15553901, 10717437, 60283454, 47468370, 88336367, 23467252, 48851751, 23532087, 32663345, 42686687, 18894787, 66000065, 80873429, 61139991, 50477232, 49970542, 37280494, 23282944, 59174404, 54071147, 58790429, 27830751, 90139037, 88223119, 75532452, 67694184, 10950519, 99919933, 53174974, 52402024, 28652460, 49557963, 84602228, 36283293, 17313136, 68723921, 29705141, 35295479, 69696645, 99343330, 36856758, 47763352, 97650374, 54691924, 70701102, 85375505, 14182882, 33036581, 15277413, 12033284, 55252057, 59586065, 86419566, 20846059, 44144860, 47724227, 74287830, 55344249, 40261498, 47489681, 66625170, 61469123, 95257997, 59258183, 45431427, 90246002, 54242145, 62185368, 79299761]

ENE = 20e3
EVTMAX = 1
BFIELD = 0
PHIMIN = 0
PHIMAX = 6.28
VX=0
VY=0
VZ=0




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

geantservice.G4commands += ["/random/setSeeds "+str(seed[i-1])+" 0"]
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
