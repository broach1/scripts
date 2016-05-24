import ROOT as rt
import numpy as np


c1 = rt.TCanvas("c1","c1",1200,800)
leg = rt.TLegend(0.7,0.7,0.9,0.9)

energies = [20, 50, 100, 250, 500]
energies_float = []
sf_list = []



for energy in energies:
    f1 = rt.TFile.Open("~/grid_runs/6mm/LAR3.5_LEAD2.5/no_cryo_fixed/e"+str(energy)+"_n500_b0_processed.root")
    hist = f1.Get("h_hit_energy_ecal")
    sf_list.append((energy*1000)/hist.GetMean())
    energies_float.append(float(energy))

print(len(energies_float))

g1 = rt.TGraph(len(energies_float),np.asarray(energies_float),np.asarray(sf_list))
leg.AddEntry(g1,"3.5mm LAr, 2.5mm lead")
g1.Draw("A*")
leg.Draw()
g1.GetYaxis().SetRangeUser(7.15,7.25)
g1.GetXaxis().SetTitle("Energy (GeV)")
g1.GetYaxis().SetTitle("Sampling fraction")
g1.SetTitle("ECAL sampling fraction")
line = rt.TLine(0,7.21,520,7.21)
line.Draw()
line.SetLineStyle(7)
rt.gPad.Update()

c1.SaveAs("linearity_sf.pdf")
    
    
