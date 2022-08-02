import ROOT
import pandas as pd

#the class takes in a dataframe which contains variables including the BDT output variable as the 1st input
class before_after_ML_plots:
    def __init__(self, original_df,generation_variable,xgb_variable,selection_cut,variable_name,bins,range_min,range_max):
        self . original_df                           = original_df
        self . generation_variable                   = generation_variable
        self . variable_name                         = variable_name
        self . xgb_variable                          = xgb_variable
        self . selection_cut                         = selection_cut
        self . bins                                  = bins
        self . range_min                             = range_min
        self . range_max                             = range_max
        self . before_after_ML_dataframe_creator()
        self . common_hist_features(h1d)
        
    #create dataframes for signal and background 
    def before_after_ML_dataframe_creator(self):
        #before ML
        signal_in_original_df = self.original_df[self.original_df[self.generation_variable]>0]
        back_in_original_df = self.original_df[self.original_df[self.generation_variable]==0]
        
        #after ML
        signal_in_after_ml = self.original_df[(self.original_df[self.generation_variable]>0) & ((self.original_df[self.xgb_variable]>self.selection_cut))]
        back_in_after_ml = self.original_df[(self.original_df[self.generation_variable]==0) & ((self.original_df[self.xgb_variable]>self.selection_cut))]
        
        return signal_in_original_df, back_in_original_df, signal_in_after_ml, back_in_after_ml
    
    #create a histogram for variable
    def create_fill_histograms(self):
        signal_df, back_df, signal_in_after_ml, back_in_after_ml=self.before_after_ML_dataframe_creator()
        
        h1d_sig = ROOT.TH1D("","",self.bins,self.range_min,self.range_max)
        for i in range(0,signal_df[self.variable_name].shape[0]):
            h1d_sig.Fill(signal_df[self.variable_name].iloc[i])
            
        h1d_back = ROOT.TH1D("","",self.bins,self.range_min,self.range_max)
        for i in range(0,back_df[self.variable_name].shape[0]):
            h1d_back.Fill(back_df[self.variable_name].iloc[i])
            
        h1d_sig_after_ml = ROOT.TH1D("","",self.bins,self.range_min,self.range_max)
        for i in range(0,signal_in_after_ml[self.variable_name].shape[0]):
            h1d_sig_after_ml.Fill(signal_in_after_ml[self.variable_name].iloc[i])
            
        h1d_back_after_ml = ROOT.TH1D("","",self.bins,self.range_min,self.range_max)
        for i in range(0,back_in_after_ml[self.variable_name].shape[0]):
            h1d_back_after_ml.Fill(back_in_after_ml[self.variable_name].iloc[i])
        
        return h1d_sig, h1d_back, h1d_sig_after_ml, h1d_back_after_ml
    
    #common features used in all the histograms
    def common_hist_features(self,h1d):
        h1d.SetStats(0)
        h1d.SetMarkerSize(0.7)
        h1d.SetYTitle("counts")
        h1d.GetYaxis().CenterTitle()
        h1d.GetYaxis().SetTitleSize(0.05)
        h1d.GetYaxis().SetLabelSize(0.04)
        h1d.GetXaxis().CenterTitle()
        h1d.GetXaxis().SetTitleSize(0.05)
        h1d.GetXaxis().SetLabelSize(0.04)
        h1d.SetXTitle(self.variable_name)
        return h1d
    
    #before ML backround histogram modifier  
    def back_before_ml(self,h1d):
        h1d.SetMarkerColor(ROOT.kRed)
        h1d.SetLineColor(ROOT.kRed)
        h1d.SetMarkerStyle(8)
        h1d = self.common_hist_features(h1d)
        return h1d
    
    #before ML signal histogram modifier
    def sig_before_ml(self, h1d):
        h1d.SetMarkerColor(ROOT.kBlack)
        h1d.SetLineColor(ROOT.kBlack)
        h1d.SetMarkerStyle(8)
        h1d = self.common_hist_features(h1d)
        return h1d
    
    #after ML background histogram modifier
    def back_after_ml(self,h1d):
        h1d.SetMarkerColor(ROOT.kMagenta)
        h1d.SetLineColor(ROOT.kMagenta)
        h1d.SetMarkerStyle(21)
        h1d = self.common_hist_features(h1d)
        return h1d
    
    #after ML background histogram modifier
    def sig_after_ml(self, h1d):
        h1d.SetMarkerColor(ROOT.kBlue)
        h1d.SetLineColor(ROOT.kBlue)
        h1d.SetMarkerStyle(21)
        h1d = self.common_hist_features(h1d)
        return h1d
    
#use case
cl = before_after_ML_plots(df_clean_urqmd,'Candidates_plain_generation','xgb_preds',0.9,"Candidates_plain_chi2_prim_second",1000,0,5000000)
h1d_sig, h1d_back, h1d_sig_after_ml, h1d_back_after_ml = cl.create_fill_histograms()


#plotting
c=ROOT.TCanvas("","",800,800)
c.SetBottomMargin(0.12)
c.SetTopMargin(0.02)
c.SetLeftMargin (0.15);
c.SetRightMargin (0.08)
c.Draw()
c.SetLogy()
ROOT.TGaxis.SetMaxDigits(2)
#c.SetLogx()
h1d_back=cl.back_before_ml(h1d_back)
h1d_sig=cl.sig_before_ml(h1d_sig)
h1d_sig_after_ml=cl.back_after_ml(h1d_sig_after_ml)
h1d_back_after_ml=cl.sig_after_ml(h1d_back_after_ml)
legend = ROOT.TLegend(0.5,0.75,0.8,0.85);
legend.SetTextSize(0.023);
legend.AddEntry(h1d_back,"#Lambda_{backg} before","pe,X0")
legend.AddEntry(h1d_sig,"#Lambda_{sig} before","pe,X0")
legend.AddEntry(h1d_back_after_ml,"#Lambda_{backg} after ML","pe,X0")
legend.AddEntry(h1d_sig_after_ml,"#Lambda_{sig} after ML","pe,X0")
h1d_back.Draw("pe")
h1d_sig.Draw("pe,same")
h1d_sig_after_ml.Draw("pe,same")
h1d_back_after_ml.Draw("pe,same")
legend.Draw()
c.Print("hists.png")
