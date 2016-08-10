import ROOT as rt
import numpy as np
import math


energies = [20, 50, 100, 250, 500, 1000]
x0_list = [25,27,30,35,40,45,50,55,60]
big_array = np.zeros((70,len(energies)))
stoch_term=[]
flag = 1
lar = input("Enter LAr (mm): ")
lead = input("Enter lead (mm): ")
while flag == 1:

    for x0 in x0_list:
        sig_calc=[]
        err_sig=[]
        err_en=[]
        en_calc=[]
        i=1
    

        c3 = rt.TCanvas("c3","c3",1200,800)
        c3.Divide(3,2)
        rt.gStyle.SetOptStat(01)
        rt.gStyle.SetOptFit(1)

        for energy in energies:

            c1 = rt.TCanvas("c1","c1",1200,800)


            try:


                fname = "e"+str(energy)+"_n10000"+"_lar"+str(lar)+"_lead"+str(lead)+"_processed_x0.root"
                print(fname)

                f1 = rt.TFile.Open(fname)
                hist = f1.Get('h_res_sf_'+str(x0)+'X0')


                mean = hist.GetMean()
                sigma = hist.GetRMS()


                iqr = 1.349*sigma
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

                binsizeoriginal=1 #MeV
                hist.GetXaxis().SetRangeUser(emin,emax)
                binsizenew = 2*iqr/(hist.GetEntries()**0.33333) #MeV
                #print(binsizenew)
                nbinsnew = (emax-emin)/binsizenew
                nbinsoriginal = (emax-emin)/binsizeoriginal
                #the original bin size was 100 MeV

                #print("rebinning factor", nbinsoriginal/nbins)
                if (int(math.ceil(nbinsoriginal/nbinsnew)) <= 1):
                    hist.R1ebin(1)

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
                hist.GetXaxis().SetTitle("Energy (MeV)")

                #hist.GetYaxis().SetTitle("Events/bin")
                #hist.GetYaxis(0).SetTitleOffset(1.2)
                hist.SetTitle(str(energy)+" GeV, LAr "+str(lar)+",Pb "+str(lead))
                rt.gStyle.SetTitleAlign(13)

                c3.cd(i)
                hist.DrawCopy()
                #purely for plotting/aesthetic reasons

                mean = func.GetParameter(1)
                sigma = func.GetParameter(2)
                print(sigma)
                en_calc.append(mean)
                sig_calc.append(sigma)
                print(sig_calc)
                err_en.append(func.GetParError(1))
                err_sig.append(func.GetParError(2))


                i+=1

            except:
                pass

        c3.SaveAs("lar"+str(lar)+"_lead"+str(lead)+"_"+str(x0)+"x0_"+"_multiplot.pdf")
        c1.cd()
        sig_over_e = np.array(sig_calc)/np.array(en_calc)   
        en_calc = np.array(np.array(en_calc)/1000)
        sig_over_e = np.array(sig_over_e)
    #print(en_calc)
    #print(sig_calc)
    #print(sig_over_e)
        err_en = np.array(err_en)
        err_sig = np.array(err_sig)
        err_sigovere = err_sig/(1000*np.asarray(energies))
        big_array[x0,:] = sig_over_e
        big_array[x0+1,:]=err_sigovere
        g = rt.TGraphErrors(len(en_calc),en_calc,sig_over_e,err_en/1000,err_sig/(1000*np.asarray(en_calc)))
        g.Draw("AP")
        g.SetMarkerSize(2)
        g.SetMarkerStyle(20)

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
    #rt.gStyle.SetTitleX(0.5)
    #rt.gStyle.SetTitleAlign(23)
        print(f2.GetParameter(0))


        c1.SaveAs("plots/sig_over_e_LAR"+str(lar)+"_LEAD"+str(lead)+"_"+str(x0)+"x0_FD.pdf")
    print(big_array)
    print(big_array[25,:])
    en=np.array(energies,"float")
    
    c7 = rt.TCanvas("c7","c7",800,600)
    c7.cd()
    g_25 = rt.TGraphErrors(6,en,big_array[25,:],big_array[1,:],big_array[26,:])
    g_30 = rt.TGraphErrors(6,en,big_array[30,:],big_array[1,:],big_array[31,:])
    g_35 = rt.TGraphErrors(6,en,big_array[35,:],big_array[1,:],big_array[36,:])
    g_40 = rt.TGraphErrors(6,en,big_array[40,:],big_array[1,:],big_array[41,:])
    g_45 = rt.TGraphErrors(6,en,big_array[45,:],big_array[1,:],big_array[46,:])
    g_50 = rt.TGraphErrors(6,en,big_array[50,:],big_array[1,:],big_array[51,:])
    g_55 = rt.TGraphErrors(6,en,big_array[55,:],big_array[1,:],big_array[56,:])
    g_60 = rt.TGraphErrors(6,en,big_array[60,:],big_array[1,:],big_array[61,:])




    g_25.Draw("ACP")
    g_30.Draw("ACP SAME")
    g_35.Draw("ACP SAME")
    #g_40.Draw("AP SAME")
    #g_45.Draw("AP SAME")
    #g_50.Draw("AP SAME")
    #g_55.Draw("AP SAME")
    #g_60.Draw("AP SAME")
    rt.gPad.SetLogx()
    f = input("enter something")

    flag=0
    #flag = input("Continue? 1 yes, 0 no: ")
#print(en_calc)
#print(sig_calc)
#print(err_en)    
#print(err_sig)
#print(err_sig/(1000*en_calc))
