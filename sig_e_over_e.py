import ROOT as rt
import numpy as np

en_calc = []
sig_calc = []
err_en = []
err_sig = []

energies = [20, 50, 100, 250, 500]
c1 = rt.TCanvas("c1","c1",1200,800)



for energy in energies:
    
    
    fname = "~/grid_runs/6mm/LAR3.5_LEAD2.5/no_cryo_fixed/e"+str(energy)+"_n500_b0_processed.root"
    f1 = rt.TFile.Open(fname)
    hist = f1.Get('h_res')
    #hist.Rebin(5)
    #rt.gStyle.SetOptStat(0)
    
    func = rt.TF1("func","gaus")
    hist.Fit(func)
    mean = func.GetParameter(1)
    sigma = func.GetParameter(2)
    hist.Fit(func,"","r",mean-2*sigma,mean+2*sigma)
    
    mean = func.GetParameter(1)
    sigma = func.GetParameter(2)
    en_calc.append(mean)
    sig_calc.append(sigma)
    err_en.append(func.GetParError(1))
    err_sig.append(func.GetParError(2))
        
c1.cd()
sig_over_e = np.array(sig_calc)/np.array(en_calc)   
en_calc = np.array(np.array(en_calc)/1000)
sig_over_e = np.array(sig_over_e)
err_en = np.array(err_en)
err_sig = np.array(err_sig)
g = rt.TGraph(len(en_calc),en_calc,sig_over_e)
g.Draw("AP")

f2 = rt.TF1("f2","TMath::Sqrt([0]**2/x + [1]**2)",10,1000)
f2.SetParName(0,"Stoch. term")
f2.SetParName(1,"Const. term")
g.Fit(f2)
rt.gStyle.SetOptFit(1)


g.SetMarkerStyle(3)
g.GetXaxis().SetTitle("Electron energy (GeV)")
g.GetYaxis().SetTitle("#sigma/E")
g.SetTitle("3.5mm LAr, 2.5mm lead")
#rt.gPad.SetLogx()


c1.SaveAs("c1.pdf")
    
