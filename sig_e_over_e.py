import ROOT as rt
import numpy as np
import math


energies = [20, 50, 100, 250, 500, 1000]
stoch_term = []    


i=1
flag = 1
while flag == 1:

    en_calc = []
    sig_calc = []
    err_en = []
    err_sig = []

    
    lar = input("Enter LAr (mm): ")
    lead = input("Enter lead (mm): ")
    
    for energy in energies:
        c1 = rt.TCanvas("c1","c1",1200,800)

        if (energy < 500):
            nevt = 2500
        elif (energy == 500):
            nevt = 1500
        else:
            nevt = 1000

        try:
            c2 = rt.TCanvas("c2","c2",800,600)
            #c3 = rt.TCanvas("c3","c3",800,600)
            
            #fname = "~/FCC_calo_analysis_cpp/output-calo-histo.root"
            fname = "~/grid_runs/martin/LAR"+str(lar)+"mm/e"+str(energy)+"_n"+str(nevt)+"_lar"+str(lar)+"_lead"+str(lead)+"_processed.root"
            #print(fname)
            #fname = "calibration_July1/e"+str(energy)+"_lar"+str(lar)+"_lead"+str(lead)+"_dphi01_dz50_n500_processed.root"

            f1 = rt.TFile.Open(fname)
            hist = f1.Get('h_res_sf')

            c2.cd()

            

            mean = hist.GetMean()
            sigma = hist.GetRMS()
            #initial values, used for calculating
            #IQR and plot ranges
            
            iqr = 1.349*sigma #interquartile range
            emin = mean-5*sigma
            emax = mean+5*sigma
            #range for plotting

            #print(iqr,emin,emax)
            #print("still good")

            #Freedman-Diaconis rule
            #note - rebinning factor must be integer
            #the int(math.ceil( ... ) ) construction
            #rounds the binning factor up to the next
            #integer

            hist.GetXaxis().SetRangeUser(emin,emax)
            binsize = 2*iqr/(hist.GetEntries()**0.33333) #MeV
            print(binsize)
            nbinsnew = (emax-emin)/binsize
            nbinsoriginal = (emax-emin)/100
            #the original bin size was 100 MeV

            #print("rebinning factor", nbinsoriginal/nbins)
            if (int(math.ceil(nbinsoriginal/nbinsnew)) <= 1):
                hist.Rebin(1)
            
            else:
                hist.Rebin(int(math.ceil(nbinsoriginal/nbinsnew)))
                print("rebin successful")

            mean = hist.GetMean()
            sigma = hist.GetRMS()
            

            #print("getting ready to fit")
            #now, we fit in +/- 2sigma region
            func = rt.TF1("func","gaus")
            hist.Fit(func)
            mean = func.GetParameter(1)
            sigma = func.GetParameter(2)
            hist.Fit(func,"","r",mean-2*sigma,mean+2*sigma)
            hist.GetXaxis().SetRangeUser(mean-5*sigma,mean+5*sigma)
            #purely for plotting/aesthetic reasons

            mean = func.GetParameter(1)
            sigma = func.GetParameter(2)
            en_calc.append(mean)
            sig_calc.append(sigma)
            err_en.append(func.GetParError(1))
            err_sig.append(func.GetParError(2))
            rt.gStyle.SetOptFit(1)
            rt.gStyle.SetOptStat(1111)
            rt.gPad.Update()
            i+= 1

            print("Saving histogram")
            c2.SaveAs("e"+str(energy)+"_gaussian_lar"+str(lar)+"_lead"+str(lead)+"_freedmandiaconis.pdf")

        except:
            pass


    c1.cd()
    sig_over_e = np.array(sig_calc)/np.array(en_calc)   
    en_calc = np.array(np.array(en_calc)/1000)
    sig_over_e = np.array(sig_over_e)
    #print(en_calc)
    #print(sig_calc)
    #print(sig_over_e)
    err_en = np.array(err_en)
    err_sig = np.array(err_sig)
    g = rt.TGraphErrors(len(en_calc),en_calc,sig_over_e,err_en/1000,err_sig/(1000*np.asarray(en_calc)))
    g.Draw("AP")

    f2 = rt.TF1("f2","TMath::Sqrt([0]**2/x + [1]**2)",10,1000)
    #f2.SetParameter(0,0.08)
    #f2.SetParameter(1,0.005)
    f2.SetParName(0,"Stoch. term")
    f2.SetParName(1,"Const. term")
    g.Fit(f2)
    rt.gStyle.SetOptFit(1)
    stoch_term.append(f2.GetParameter(0))


    g.SetMarkerStyle(3)
    g.GetXaxis().SetTitle("Electron energy (GeV)")
    g.GetXaxis().SetTitleOffset(1.4)
    g.GetYaxis().SetTitle("#sigma/E")
    g.GetYaxis().SetTitleOffset(1.4)
    #g.SetTitle("Title goes here")
    g.SetTitle(str(lar)+"mm LAr, "+str(lead)+"mm lead")
    rt.gPad.SetLogx()
    rt.gStyle.SetTitleX(0.5)
    rt.gStyle.SetTitleAlign(23)
    print(f2.GetParameter(0))


    c1.SaveAs("plots/sig_over_e_LAR"+str(lar)+"_LEAD"+str(lead)+"_VARBINNING.pdf")

    flag = input("Continue? 1 yes, 0 no: ")

#print(en_calc)
#print(sig_calc)
#print(err_en)    
#print(err_sig)
#print(err_sig/(1000*en_calc))
