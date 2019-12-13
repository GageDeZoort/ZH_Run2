# output ntuple for H->tautau analysis for CMSSW_10_2_X

from ROOT import TLorentzVector, TH1
from math import sqrt, sin, cos, pi
import tauFun 
import ROOT
import os
import sys
sys.path.append('SFs')
import ScaleFactor as SF
import generalFunctions as GF

class outTuple() :
    
    def __init__(self,fileName, era):
        from array import array
        from ROOT import TFile, TTree

        # Tau Decay types
        self.kUndefinedDecayType, self.kTauToHadDecay,  self.kTauToElecDecay, self.kTauToMuDecay = 0, 1, 2, 3    
        ROOT.gInterpreter.ProcessLine(".include .")
        for baseName in ['MeasuredTauLepton','svFitAuxFunctions','FastMTT'] : 
            if os.path.isfile("{0:s}_cc.so".format(baseName)) :
                ROOT.gInterpreter.ProcessLine(".L {0:s}_cc.so".format(baseName))
            else :
                ROOT.gInterpreter.ProcessLine(".L {0:s}.cc++".format(baseName))   
                # .L is not just for .so files, also .cc
        
        self.sf_MuonTrigIso27 = SF.SFs()
        self.sf_MuonTrigIso27.ScaleFactor("SFs/LeptonEfficiencies/Muon/Run2017/Muon_IsoMu27.root")
        self.sf_EleTrig35 = SF.SFs()
        self.sf_EleTrig35.ScaleFactor("SFs/LeptonEfficiencies/Electron/Run2017/Electron_Ele35.root")
        #self.SF_muonIdIso = SF.SFs()
        #self.sf_SF_muonIdIso.ScaleFactor("SFs/LeptonEfficiencies/Muon/Run2017/Muon_IsoMu27.root")

        self.f = TFile( fileName, 'recreate' )
        self.t = TTree( 'Events', 'Output tree' )

        self.entries          = 0 
        self.run              = array('l',[0])
        self.lumi             = array('l',[0])
        self.is_trig          = array('l',[0])
        self.is_trigH         = array('l',[0])
        self.is_trigZ         = array('l',[0])
        self.is_trigZH        = array('l',[0])
        self.evt              = array('l',[0])
        self.cat              = array('l',[0])
        self.weight           = array('f',[0])
        self.LHEweight        = array('f',[0])
        self.Generator_weight = array('f',[0])
        self.LHE_Njets        = array('l',[0])
        
        self.pt_3        = array('f',[0])
        self.pt_3_tr     = array('f',[0])
        self.phi_3       = array('f',[0])
        self.phi_3_tr    = array('f',[0])
        self.eta_3       = array('f',[0])
        self.eta_3_tr    = array('f',[0])
        self.m_3         = array('f',[0])
        self.q_3         = array('f',[0])
        self.d0_3        = array('f',[0])
        self.dZ_3        = array('f',[0])
        self.mt_3        = array('f',[0])
        self.pfmt_3      = array('f',[0])
        self.puppimt_3   = array('f',[0])
        self.iso_3       = array('f',[0])
        self.iso_3_ID    = array('l',[0])
        self.gen_match_3 = array('l',[0])
        self.againstElectronLooseMVA6_3   = array('f',[0])
        self.againstElectronMediumMVA6_3  = array('f',[0])
        self.againstElectronTightMVA6_3   = array('f',[0])
        self.againstElectronVLooseMVA6_3  = array('f',[0])
        self.againstElectronVTightMVA6_3  = array('f',[0])
        self.againstMuonLoose3_3          = array('f',[0])
        self.againstMuonTight3_3          = array('f',[0])
        self.byIsolationMVA3oldDMwLTraw_3 = array('f',[0])
        self.trigweight_3  = array('f',[0])
        self.idisoweight_3 = array('f',[0])
        self.decayMode_3   = array('l',[0])

        self.pt_4        = array('f',[0])
        self.pt_4_tr     = array('f',[0])
        self.phi_4       = array('f',[0])
        self.phi_4_tr    = array('f',[0])
        self.eta_4       = array('f',[0])
        self.eta_4_tr    = array('f',[0])
        self.m_4         = array('f',[0])
        self.q_4         = array('f',[0])
        self.d0_4        = array('f',[0])
        self.dZ_4        = array('f',[0])
        self.mt_4        = array('f',[0])
        self.pfmt_4      = array('f',[0])
        self.puppimt_4   = array('f',[0])
        self.iso_4       = array('f',[0])
        self.iso_4_ID    = array('l',[0])
        self.gen_match_4 = array('l',[0])
        self.againstElectronLooseMVA6_4   = array('f',[0])
        self.againstElectronMediumMVA6_4  = array('f',[0])
        self.againstElectronTightMVA6_4   = array('f',[0])
        self.againstElectronVLooseMVA6_4  = array('f',[0])
        self.againstElectronVTightMVA6_4  = array('f',[0])
        self.againstMuonLoose3_4          = array('f',[0])
        self.againstMuonTight3_4          = array('f',[0])
        self.byIsolationMVA3oldDMwLTraw_4 = array('f',[0])
        self.trigweight_4  = array('f',[0])
        self.idisoweight_4 = array('f',[0])
        self.decayMode_4   = array('l',[0])

        # di-tau variables
        self.pt_tt  = array('f',[0])
        self.mt_tot = array('f',[0])
        self.m_vis  = array('f',[0])
        self.m_sv   = array('f',[0])
        self.mt_sv  = array('f',[0])

        # di-lepton variables.   _p and _m refer to plus and minus charge
        # ll_lmass is mass of decay lepton 
        self.ll_lmass  = array('f',[0])     
        self.mll       = array('f',[0])
        self.pt_1      = array('f',[0])
        self.pt_1_tr   = array('f',[0])
        self.phi_1     = array('f',[0])
        self.phi_1_tr  = array('f',[0])
        self.eta_1     = array('f',[0])
        self.eta_1_tr  = array('f',[0])
        self.pt_2      = array('f',[0])
        self.pt_2_tr   = array('f',[0])
        self.phi_2     = array('f',[0])
        self.phi_2_tr  = array('f',[0])
        self.eta_2     = array('f',[0])
        self.eta_2_tr  = array('f',[0])
        
        # MET variables
        self.met         = array('f',[0])
        self.metphi      = array('f',[0])
        self.puppimet    = array('f',[0])
        self.puppimetphi = array('f',[0])
        self.metcov00    = array('f',[0])
        self.metcov01    = array('f',[0])
        self.metcov10    = array('f',[0])
        self.metcov11    = array('f',[0])

        # trigger sf
        self.trig_Lm_MC   = array('f',[0])
        self.trig_Lm_Data = array('f',[0])
        self.trig_Lp_MC   = array('f',[0])
        self.trig_Lp_Data = array('f',[0])
        self.trig_T1_MC   = array('f',[0])
        self.trig_T1_Data = array('f',[0])
        self.trig_T2_MC   = array('f',[0])
        self.trig_T2_Data = array('f',[0])


        # jet variables
        self.njetspt20 = array('f',[0])
        self.njets     = array('f',[0])
        self.nbtag     = array('f',[0])

        self.jpt_1     = array('f',[0])
        self.jpt_1_tr  = array('f',[0])
        self.jeta_1    = array('f',[0])
        self.jeta_1_tr = array('f',[0])
        self.jphi_1    = array('f',[0])
        self.jphi_1_tr = array('f',[0])
        self.jcsv_1    = array('f',[0])
        self.jpt_2     = array('f',[0])
        self.jpt_2_tr  = array('f',[0])
        self.jeta_2    = array('f',[0])
        self.jeta_2_tr = array('f',[0])
        self.jphi_2    = array('f',[0])
        self.jphi_2_tr = array('f',[0])
        self.jcsv_2    = array('f',[0])

        self.bpt_1     = array('f',[0])
        self.bpt_1_tr  = array('f',[0])
        self.beta_1    = array('f',[0])
        self.beta_1_tr = array('f',[0])
        self.bphi_1    = array('f',[0])
        self.bphi_1_tr = array('f',[0])
        self.bcsv_1    = array('f',[0])
        self.bpt_2     = array('f',[0])
        self.bpt_2_tr  = array('f',[0])
        self.beta_2    = array('f',[0])
        self.beta_2_tr = array('f',[0])
        self.bphi_2    = array('f',[0])
        self.bphi_2_tr = array('f',[0])
        self.bcsv_2    = array('f',[0])
      
        self.t.Branch('run',              self.run,               'run/l' )
        self.t.Branch('lumi',             self.lumi,              'lumi/I' )
        self.t.Branch('is_trig',          self.is_trig,           'is_trig/I' )
        self.t.Branch('is_trigH',         self.is_trigH,          'is_trigH/I' )
        self.t.Branch('is_trigZ',         self.is_trigZ,          'is_trigZ/I' )
        self.t.Branch('is_trigZH',        self.is_trigZH,         'is_trigZH/I' )
        self.t.Branch('evt',              self.evt,               'evt/I' )
        self.t.Branch('cat',              self.cat,               'cat/I' )
        self.t.Branch('weight',           self.weight,            'weight/F' )
        self.t.Branch('LHEweight',        self.LHEweight,         'LHEweight/F' )
        self.t.Branch('LHE_Njets',        self.LHE_Njets,         'LHE_Njets/I' )
        self.t.Branch('Generator_weight', self.Generator_weight,  'Generator_weight/F' )

        self.t.Branch('pt_3',        self.pt_3,        'pt_3/F')
        self.t.Branch('pt_3_tr',     self.pt_3_tr,     'pt_3_tr/F')
        self.t.Branch('phi_3',       self.phi_3,       'phi_3/F')
        self.t.Branch('phi_3_tr',    self.phi_3_tr,    'phi_3_tr/F')
        self.t.Branch('eta_3',       self.eta_3,       'eta_3/F')
        self.t.Branch('eta_3_tr',    self.eta_3_tr,    'eta_3_tr/F')
        self.t.Branch('m_3',         self.m_3,         'm_3/F')
        self.t.Branch('q_3',         self.q_3,         'q_3/F')
        self.t.Branch('d0_3',        self.d0_3,        'd0_3/F')
        self.t.Branch('dZ_3',        self.dZ_3,        'dZ_3/F')
        self.t.Branch('mt_3',        self.mt_3,        'mt_3/F')
        self.t.Branch('pfmt_3',      self.pfmt_3,      'pfmt_3/F')
        self.t.Branch('puppimt_3',   self.puppimt_3,   'puppimt_3/F')
        self.t.Branch('iso_3',       self.iso_3,       'iso_3/F')
        self.t.Branch('iso_3_ID',    self.iso_3_ID,    'iso_3_ID/l')
        self.t.Branch('gen_match_3', self.gen_match_3, 'gen_match_3/l')
        self.t.Branch('againstElectronLooseMVA6_3',   self.againstElectronLooseMVA6_3,   'againstElectronLooseMVA6_3/F')
        self.t.Branch('againstElectronMediumMVA6_3',  self.againstElectronMediumMVA6_3,  'againstElectronMediumMVA6_3/F')
        self.t.Branch('againstElectronTightMVA6_3',   self.againstElectronTightMVA6_3,   'againstElectronTightMVA6_3/F')
        self.t.Branch('againstElectronVLooseMVA6_3',  self.againstElectronVLooseMVA6_3,  'againstElectronVLooseMVA6_3/F')
        self.t.Branch('againstElectronVTightMVA6_3',  self.againstElectronVTightMVA6_3,  'againstElectronVTightMVA6_3/F')
        self.t.Branch('againstMuonLoose3_3',          self.againstMuonLoose3_3,          'againstMuonLoose3_3/F')
        self.t.Branch('againstMuonTight3_3',          self.againstMuonTight3_3,          'againstMuonTight3_3/F')
        self.t.Branch('byIsolationMVA3oldDMwLTraw_3', self.byIsolationMVA3oldDMwLTraw_3, 'byIsolationMVA3oldDMwLTraw_3/F')
        self.t.Branch('trigweight_3',  self.trigweight_3,  'trigweight_3/F')
        self.t.Branch('idisoweight_3', self.idisoweight_3, 'idisoweight_3/F')
        self.t.Branch('decayMode_3',   self.decayMode_3,   'decayMode_3/I')

        self.t.Branch('pt_4',        self.pt_4,        'pt_4/F')
        self.t.Branch('pt_4_tr',     self.pt_4,        'pt_4_tr/F')
        self.t.Branch('phi_4',       self.phi_4,       'phi_4/F')
        self.t.Branch('phi_4_tr',    self.phi_4_tr,    'phi_4_tr/F')
        self.t.Branch('eta_4',       self.eta_4,       'eta_4/F')
        self.t.Branch('eta_4_tr',    self.eta_4_tr,    'eta_4_tr/F')
        self.t.Branch('m_4',         self.m_4,         'm_4/F')
        self.t.Branch('q_4',         self.q_4,         'q_4/F')
        self.t.Branch('d0_4',        self.d0_4,        'd0_4/F')
        self.t.Branch('dZ_4',        self.dZ_4,        'dZ_4/F')
        self.t.Branch('mt_4',        self.mt_4,        'mt_4/F')
        self.t.Branch('pfmt_4',      self.pfmt_4,      'pfmt_4/F')
        self.t.Branch('puppimt_4',   self.puppimt_4,   'puppimt_4/F')
        self.t.Branch('iso_4',       self.iso_4,       'iso_4/F')
        self.t.Branch('iso_4_ID',    self.iso_4_ID,    'iso_4_ID/l')
        self.t.Branch('gen_match_4', self.gen_match_4, 'gen_match_4/l')
        self.t.Branch('againstElectronLooseMVA6_4',   self.againstElectronLooseMVA6_4,   'againstElectronLooseMVA6_4/F')
        self.t.Branch('againstElectronMediumMVA6_4',  self.againstElectronMediumMVA6_4,  'againstElectronMediumMVA6_4/F')
        self.t.Branch('againstElectronTightMVA6_4',   self.againstElectronTightMVA6_4,   'againstElectronTightMVA6_4/F')
        self.t.Branch('againstElectronVLooseMVA6_4',  self.againstElectronVLooseMVA6_4,  'againstElectronVLooseMVA6_4/F')
        self.t.Branch('againstElectronVTightMVA6_4',  self.againstElectronVTightMVA6_4,  'againstElectronVTightMVA6_4/F')
        self.t.Branch('againstMuonLoose3_4',          self.againstMuonLoose3_4,          'againstMuonLoose3_4/F')
        self.t.Branch('againstMuonTight3_4',          self.againstMuonTight3_4,          'againstMuonTight3_4/F')
        self.t.Branch('byIsolationMVA3oldDMwLTraw_4', self.byIsolationMVA3oldDMwLTraw_4, 'byIsolationMVA3oldDMwLTraw_4/F')
        self.t.Branch('trigweight_4',  self.trigweight_4,  'trigweight_4/F')
        self.t.Branch('idisoweight_4', self.idisoweight_4, 'idisoweight_4/F')
        self.t.Branch('decayMode_4',   self.decayMode_4,   'decayMode_4/I')

        # di-tau variables
        self.t.Branch('pt_tt', self.pt_tt, 'pt_tt/F')
        self.t.Branch('mt_tot', self.mt_tot, 'mt_tot/F')
        self.t.Branch('m_vis', self.m_vis, 'm_vis/F')
        self.t.Branch('m_sv', self.m_sv, 'm_sv/F')
        self.t.Branch('mt_sv', self.mt_sv, 'mt_sv/F') 

        # di-lepton variables. 
        self.t.Branch('ll_lmass',    self.ll_lmass,    'll_lmass/F')
        self.t.Branch('mll',         self.mll,         'mll/F')   
        self.t.Branch('pt_1',        self.pt_1,        'pt_1/F')
        self.t.Branch('pt_1_tr',     self.pt_1_tr,     'pt_1_tr/F')
        self.t.Branch('phi_1',       self.phi_1,       'phi_1/F')  
        self.t.Branch('phi_1_tr',    self.phi_1_tr,    'phi_1_tr/F')
        self.t.Branch('eta_1',       self.eta_1,       'eta_1/F')    
        self.t.Branch('eta_1_tr',    self.eta_1_tr,    'eta_1_tr/F')
        self.t.Branch('pt_2',        self.pt_2,        'pt_2/F')      
        self.t.Branch('pt_2_tr',     self.pt_2_tr,     'pt_2_tr/F')
        self.t.Branch('phi_2',       self.phi_2,       'phi_2/F')    
        self.t.Branch('phi_2_tr',    self.phi_2_tr,    'phi_2_tr/F')
        self.t.Branch('eta_2',       self.eta_2,       'eta_2/F')      
        self.t.Branch('eta_2_tr',    self.eta_2_tr,    'eta_2_tr/F')
        
        # MET variables
        self.t.Branch('met', self.met, 'met/F')
        self.t.Branch('metphi', self.metphi, 'metphi/F')
        self.t.Branch('puppimet', self.puppimet, 'puppimet/F')
        self.t.Branch('puppimetphi', self.puppimetphi, 'puppimetphi/F')
        self.t.Branch('metcov00', self.metcov00, 'metcov00/F')
        self.t.Branch('metcov01', self.metcov01, 'metcov01/F')
        self.t.Branch('metcov10', self.metcov10, 'metcov10/F')
        self.t.Branch('metcov11', self.metcov11, 'metcov11/F')

        # trigger sf
        self.t.Branch('trig_Lm_MC',  self.trig_Lm_MC, 'trig_Lm_MC/F' )
        self.t.Branch('trig_Lm_Data',  self.trig_Lm_Data, 'trig_Lm_Data/F' )
        self.t.Branch('trig_Lp_MC',  self.trig_Lp_MC, 'trig_Lp_MC/F' )
        self.t.Branch('trig_Lp_Data',  self.trig_Lp_Data, 'trig_Lp_Data/F' )
        self.t.Branch('trig_T1_MC',  self.trig_T1_MC, 'trig_T1_MC/F' )
        self.t.Branch('trig_T1_Data',  self.trig_T1_Data, 'trig_T1_Data/F' )
        self.t.Branch('trig_T2_MC',  self.trig_T2_MC, 'trig_T2_MC/F' )
        self.t.Branch('trig_T2_Data',  self.trig_T2_Data, 'trig_T2_Data/F' )


        # jet variables
        self.t.Branch('njetspt20', self.njetspt20, 'njetspt20/F') 
        self.t.Branch('njets', self.njets, 'njets/F')
        self.t.Branch('nbtag', self.nbtag, 'nbtag/F')

        self.t.Branch('jpt_1',     self.jpt_1,     'jpt_1/F' )
        self.t.Branch('jpt_1_tr',  self.jpt_1_tr,  'jpt_1_tr/F' )
        self.t.Branch('jeta_1',    self.jeta_1,    'jeta_1/F' ) 
        self.t.Branch('jeta_1_tr', self.jeta_1_tr, 'jeta_1_tr/F' )
        self.t.Branch('jphi_1',    self.jphi_1,    'jphi_1/F' )
        self.t.Branch('jphi_1_tr', self.jphi_1_tr, 'jphi_1_tr/F' )
        self.t.Branch('jcsv_1',    self.jcsv_1,    'jcsv_1/F' )
        self.t.Branch('jpt_2',     self.jpt_2,     'jpt_2/F' )
        self.t.Branch('jpt_2_tr',  self.jpt_2_tr,  'jpt_2_tr/F' )
        self.t.Branch('jeta_2',    self.jeta_2,    'jeta_2/F' ) 
        self.t.Branch('jeta_2_tr', self.jeta_2_tr, 'jeta_2_tr/F' )
        self.t.Branch('jphi_2',    self.jphi_2,    'jphi_2/F' )
        self.t.Branch('jphi_2_tr', self.jphi_2_tr, 'jphi_2_tr/F' )
        self.t.Branch('jcsv_2',    self.jcsv_2,    'jcsv_2/F' )

        self.t.Branch('bpt_1',     self.bpt_1,     'bpt_1/F' )
        self.t.Branch('bpt_1_tr',  self.bpt_1_tr,  'bpt_1_tr/F' )
        self.t.Branch('beta_1',    self.beta_1,    'beta_1/F' ) 
        self.t.Branch('beta_1_tr', self.beta_1_tr, 'beta_1_tr/F' )
        self.t.Branch('bphi_1',    self.bphi_1,    'bphi_1/F' )
        self.t.Branch('bphi_1_tr', self.bphi_1_tr, 'bphi_1_tr/F' )
        self.t.Branch('bcsv_1',    self.bcsv_1,    'bcsv_1/F' )
        self.t.Branch('bpt_2',     self.bpt_2,     'bpt_2/F' )
        self.t.Branch('bpt_2_tr',  self.bpt_2_tr,  'bpt_2_tr/F' )
        self.t.Branch('beta_2',    self.beta_2,    'beta_2/F' )
        self.t.Branch('beta_2_tr', self.beta_2_tr, 'beta_2_tr/F' )
        self.t.Branch('bphi_2',    self.bphi_2,    'bphi_2/F' )
        self.t.Branch('bphi_2_tr', self.bphi_2_tr, 'bphi_2_tr/F' )
        self.t.Branch('bcsv_2',    self.bcsv_2,    'bcsv_2/F' )

    def getAntiEle(self,entry,j,bitPos) :
        if ord(entry.Tau_idAntiEle[j]) & bitPos > 0 : return 1.
        else : return 0.

    def getAntiMu(self,entry,j,bitPos) :
        if ord(entry.Tau_idAntiMu[j]) & bitPos > 0 : return 1.
        else : return 0.

    def get_mt(self,METtype,entry,tau) :
        if METtype == 'MVAMet' :
            # temporary choice 
            dphi = tau.Phi() - entry.MET_phi
            return sqrt(2.*tau.Pt()*entry.MET_pt*(1. - cos(dphi)))
        elif METtype == 'PFMet' :
            dphi = tau.Phi() - entry.MET_phi
            return sqrt(2.*tau.Pt()*entry.MET_pt*(1. - cos(dphi)))
        elif METtype == 'PUPPIMet' :
            dphi = tau.Phi() - entry.PuppiMET_phi
            return sqrt(2.*tau.Pt()*entry.PuppiMET_pt*(1. - cos(dphi)))
        else :
            print("Invalid METtype={0:s} in outTuple.get_mt().   Exiting".format(METtype))

    def getPt_tt(self,entry,tau1,tau2) :
        ptMiss = TLorentzVector() 
        ptMiss.SetPtEtaPhiM(entry.MET_pt,0.,entry.MET_phi,0.)
        return (tau1+tau2+ptMiss).Pt()

    def getMt_tot(self,entry,tau1,tau2) :
        pt1, pt2, met = tau1.Pt(), tau2.Pt(), entry.MET_pt
        phi1, phi2, metphi = tau1.Phi(), tau2.Phi(), entry.MET_phi
        arg = 2.*(pt1*met*(1. - cos(phi1-metphi)) + pt2*met*(1. - cos(phi2-metphi)) + pt1*pt2*(1. - cos(phi2-phi1)))
        return sqrt(arg)

    def getM_vis(self,entry,tau1,tau2) :
        return (tau1+tau2).M()

    def getJets(self,entry,tau1,tau2,era) :
        nJet30, jetList, bJetList = 0, [], []
        phi2_1, eta2_1 = tau1.Phi(), tau1.Eta() 
        phi2_2, eta2_2 = tau2.Phi(), tau2.Eta() 
        for j in range(entry.nJet) :
            if entry.Jet_pt[j] < 20. : break
            if abs(entry.Jet_eta[j]) > 4.7 : continue
            phi1, eta1 = entry.Jet_phi[j], entry.Jet_eta[j]
            dPhi = min(abs(phi2_1-phi1),2.*pi-abs(phi2_1-phi1))
            DR = sqrt(dPhi**2 + (eta2_1-eta1)**2)
            dPhi = min(abs(phi2_2-phi1),2.*pi-abs(phi2_2-phi1))
            DR = min(DR,sqrt(dPhi**2 + (eta2_2-eta1)**2))
            if DR < 0.5 : continue
            bjet_discr = 0.6321
            if str(era) == 2017 : bjet_discr = 0.4941
            if str(era) == 2018 : bjet_discr = 0.4184
            if True  and abs(entry.Jet_eta[j]) < 2.5 and entry.Jet_btagDeepB[j] > bjet_discr : bJetList.append(j)
            #if True and abs(entry.Jet_eta[j]) < 2.4 and entry.Jet_btagCSVV2[j] > 0.800 and entry.Jet_pt[j] > 30. : bJetList.append(j)
            if entry.Jet_jetId[j] & 2 == 0 : continue
            if entry.Jet_pt[j] < 30. : continue
            nJet30 += 1
            jetList.append(j) 

        return nJet30, jetList, bJetList 

    def runSVFit(self, entry, channel, jt1, jt2, tau1, tau2 ) :
                      
        measuredMETx = entry.MET_pt*cos(entry.MET_phi)
        measuredMETy = entry.MET_pt*sin(entry.MET_phi)

        #define MET covariance
        covMET = ROOT.TMatrixD(2,2)
        #covMET[0][0] = entry.MET_covXX
        #covMET[1][0] = entry.MET_covXY
        #covMET[0][1] = entry.MET_covXY
        #covMET[1][1] = entry.MET_covYY
        covMET[0][0] = 787.352
        covMET[1][0] = -178.63
        covMET[0][1] = -178.63
        covMET[1][1] = 179.545

        #self.kUndefinedDecayType, self.kTauToHadDecay,  self.kTauToElecDecay, self.kTauToMuDecay = 0, 1, 2, 3

        if channel == 'et' :
            measTau1 = ROOT.MeasuredTauLepton(self.kTauToElecDecay, tau1.Pt(), tau1.Eta(), tau1.Phi(), 0.000511) 
        elif channel == 'mt' :
            measTau1 = ROOT.MeasuredTauLepton(self.kTauToMuDecay, tau1.Pt(), tau1.Eta(), tau1.Phi(), 0.106) 
        elif channel == 'tt' :
            measTau1 = ROOT.MeasuredTauLepton(self.kTauToHadDecay, tau1.Pt(), tau1.Eta(), tau1.Phi(), entry.Tau_mass[jt1])
                        
	if channel != 'em' :
            measTau2 = ROOT.MeasuredTauLepton(self.kTauToHadDecay, tau2.Pt(), tau2.Eta(), tau2.Phi(), entry.Tau_mass[jt2])

	if channel == 'em' :
            measTau1 = ROOT.MeasuredTauLepton(self.kTauToElecDecay, tau1.Pt(), tau1.Eta(), tau1.Phi(), 0.000511)
            measTau2 = ROOT.MeasuredTauLepton(self.kTauToMuDecay, tau2.Pt(), tau2.Eta(), tau2.Phi(), 0.106)

        VectorOfTaus = ROOT.std.vector('MeasuredTauLepton')
        instance = VectorOfTaus()
        instance.push_back(measTau1)
        instance.push_back(measTau2)

        FMTT = ROOT.FastMTT()
        FMTT.run(instance, measuredMETx, measuredMETy, covMET)
        ttP4 = FMTT.getBestP4()
        return ttP4.M(), ttP4.Mt() 
    
    def Fill(self, entry, SVFit, cat, jt1, jt2, LepP, LepM, lepList, isMC, era) :
        ''' - jt1 and jt2 point to the selected tau candidates according to the table below.
            - if e.g., channel = 'et', the jt1 points to the electron list and jt2 points to the tau list.
            - LepP and LepM are TLorentz vectors for the positive and negative members of the dilepton pair
        '''

        sf_Lp_MC, sf_Lp_Data = 0., 0.
        sf_Lm_MC, sf_Lm_Data = 0., 0.
        sf_T1_MC, sf_T1_Data = 0., 0.
        sf_T2_MC, sf_T2_Data = 0., 0.
        TrigListLep = []
        TrigListTau = []
        hltListLep  = []

        #channel_ll = 'mm' or 'ee'
        channel_ll = cat[:-2]

	#if chanl == 'mm' : TrigListLep, hltListLep = GF.findMuTrigger(lepList, entry, era)
	TrigListLep, hltListLep  = GF.findLeptTrigger(lepList, entry, channel_ll, era)

	TrigListLep = list(dict.fromkeys(TrigListLep))
        #print 'TrigerList ===========>', TrigListLep, hltListLep, channel_ll
        
        leadLPt = 0.
        subleadLPt = 0.
        leadEta = -100.
        subleadEta = -100.
        isPLead = True

	if LepP.Pt() > LepM.Pt() : 
            leadLPt = LepP.Pt()
            leadEta = LepP.Eta()
            subleadLPt = LepM.Pt()
            subleadEta = LepM.Eta()
        else : 
            leadLPt = LepM.Pt()
            leadEta = LepM.Eta()
            subleadLPt = LepP.Pt()
            subleadEta = LepP.Eta()
            isPLead = False
        
        '''
        #we have to implement the different .root files depending on the different triggers
        if isMC :

		if len(TrigListLep) == 1 :

		    if lepList[0] == TrigListLep[0] :
			if channel_ll == 'ee' : 
			    sf_Lp_MC = self.sf_EleTrig35.get_EfficiencyMC(LepP.Pt(),LepP.Eta())
			    sf_Lp_Data = self.sf_EleTrig35.get_EfficiencyData(LepP.Pt(),LepP.Eta())
			if channel_ll == 'mm' : 
			    sf_Lp_MC = self.sf_MuonTrigIso27.get_EfficiencyMC(LepP.Pt(),LepP.Eta())
			    sf_Lp_Data = self.sf_MuonTrigIso27.get_EfficiencyData(LepP.Pt(),LepP.Eta())

		    if lepList[1] == TrigListLep[0] :
			if channel_ll == 'ee' : 
			    sf_Lm_MC = self.sf_EleTrig35.get_EfficiencyMC(LepM.Pt(),LepM.Eta())
			    sf_Lm_Data = self.sf_EleTrig35.get_EfficiencyData(LepM.Pt(),LepM.Eta())
			if channel_ll == 'mm' : 
			    sf_Lm_MC = self.sf_MuonTrigIso27.get_EfficiencyMC(LepM.Pt(),LepM.Eta())
			    sf_Lm_Data = self.sf_MuonTrigIso27.get_EfficiencyData(LepM.Pt(),LepM.Eta())


		if len(TrigListLep) == 2 :

                    
		    if 'ee' in channel_ll : 
                        if leadPt > 28. and subleadPt > 28. :
                            if 'DoubleLep' in hltListLep :
                                sf_Lp_MC = self.sf_EleTrig35.get_EfficiencyMC(LepP.Pt(),LepP.Eta())
			        sf_Lp_Data = self.sf_EleTrig35.get_EfficiencyData(LepP.Pt(),LepP.Eta())
			        sf_Lm_MC = self.sf_EleTrig35.get_EfficiencyMC(LepM.Pt(),LepM.Eta())
			        sf_Lm_Data = self.sf_EleTrig35.get_EfficiencyData(LepM.Pt(),LepM.Eta())


		    if 'mm' in channel_ll : 
			sf_Lp_MC = self.sf_MuonTrigIso27.get_EfficiencyMC(LepP.Pt(),LepP.Eta())
			sf_Lp_Data = self.sf_MuonTrigIso27.get_EfficiencyData(LepP.Pt(),LepP.Eta())
			sf_Lm_MC = self.sf_MuonTrigIso27.get_EfficiencyMC(LepM.Pt(),LepM.Eta())
			sf_Lm_Data = self.sf_MuonTrigIso27.get_EfficiencyData(LepM.Pt(),LepM.Eta())

                        print '==========!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!!! TrigList',TrigListLep,'lepList',lepList,channel_ll,sf_Lp_MC, 'and Pt ?',LepP.Pt(), 'sf',sf_Lp_MC,'Pt m',LepM.Pt(),'sf',sf_Lm_MC
         '''

        # channel = 'mt', 'et', 'tt', or 'em'
        channel = cat[-2:]
        
        self.entries += 1

        self.run[0]  = entry.run
        self.lumi[0] = entry.luminosityBlock 
        self.evt[0]  = entry.event
        self.cat[0]  = tauFun.catToNumber(cat)
        
        try :
            self.weight[0]           = entry.genWeight
            self.LHEweight[0]        = entry.LHEWeight_originalXWGTUP
            self.Generator_weight[0] = entry.Generator_weight
            self.LHE_Njets[0]        = ord(entry.LHE_Njets) 
                        
        except AttributeError :
            self.weight[0]           = 1. 
            self.LHEweight[0]        = 1. 
            self.Generator_weight[0] = 1.
            self.gen_match_1[0]      = -1 
            
        self.againstElectronVLooseMVA6_3[0]  = -1.
        self.againstElectronLooseMVA6_3[0]   = -1.
        self.againstElectronMediumMVA6_3[0]  = -1.
        self.againstElectronTightMVA6_3[0]   = -1.
        self.againstElectronVTightMVA6_3[0]  = -1.
        self.againstMuonLoose3_3[0]          = -1.
        self.againstMuonTight3_3[0]          = -1. 
        self.byIsolationMVA3oldDMwLTraw_3[0] = -1.
        self.decayMode_3[0]                  = -1
        self.againstElectronVLooseMVA6_4[0]  = -1.
        self.againstElectronLooseMVA6_4[0]   = -1.
        self.againstElectronMediumMVA6_4[0]  = -1.
        self.againstElectronTightMVA6_4[0]   = -1.
        self.againstElectronVTightMVA6_4[0]  = -1.
        self.againstMuonLoose3_4[0]          = -1.
        self.againstMuonTight3_4[0]          = -1. 
        self.byIsolationMVA3oldDMwLTraw_4[0] = -1.
        self.decayMode_4[0]                  = -1

        tauMass = 1.7768 
        tau1, tau2 = TLorentzVector(), TLorentzVector()

        # Fill variables for Leg3, where 3->tau(ele) and 4->tau(had)
        if channel == 'et' :
            self.pt_3[0]   = entry.Electron_pt[jt1]
            self.phi_3[0]  = entry.Electron_phi[jt1]
            self.eta_3[0]  = entry.Electron_eta[jt1]
            self.m_3[0]    = entry.Electron_mass[jt1]
            self.q_3[0]    = entry.Electron_charge[jt1]
            self.d0_3[0]   = entry.Electron_dxy[jt1]
            self.dZ_3[0]   = entry.Electron_dz[jt1]
            self.iso_3[0]  = entry.Electron_pfRelIso03_all[jt1]
            self.iso_3[0]  = 0. 
            if entry.Electron_mvaFall17V2noIso_WP90[jt1] : self.iso_3[0] = 1.
            
            # Fill genMatch variables for tau(ele)
            if isMC:
                idx_genEle = entry.Electron_genPartIdx[jt1]

                # if idx_genMu = -1, no match was found
                if idx_genEle >= 0:
                    idx_genEle_mom      = entry.GenPart_genPartIdxMother[idx_genEle]
                    self.pt_3_tr[0]     = entry.GenPart_pt[idx_genEle]
                    self.phi_3_tr[0]    = entry.GenPart_phi[idx_genEle]
                    self.eta_3_tr[0]    = entry.GenPart_eta[idx_genEle]

            try: self.gen_match_3[0] = ord(entry.Electron_genPartFlav[jt1])
            except AttributeError: self.gen_match_3[0] = -1
            
            tau1.SetPtEtaPhiM(entry.Electron_pt[jt1],entry.Electron_eta[jt1], entry.Electron_phi[jt1], tauMass)
            tau2.SetPtEtaPhiM(entry.Tau_pt[jt2],entry.Tau_eta[jt2],entry.Tau_phi[jt2],tauMass)
            
            tauListE=[jt1]
	   
            '''TrigListETau=[]
	    TrigListETau = GF.findETrigger(tauListE, entry, era)

            if isMC: 
                if len(TrigListETau) == 1 :
		    sf_T1_MC = self.sf_EleTrig35.get_EfficiencyMC(entry.Electron_pt[jt1],entry.Electron_eta[jt1])
		    sf_T1_Data = self.sf_EleTrig35.get_EfficiencyData(entry.Electron_pt[jt1],entry.Electron_eta[jt1])
  
            '''

        # Fill variables for Leg3 and Leg4, where 3->tau(ele) and 4->tau(mu)
	elif channel == 'em':
            self.pt_3[0]   = entry.Electron_pt[jt1]
            self.phi_3[0]  = entry.Electron_phi[jt1]
            self.eta_3[0]  = entry.Electron_eta[jt1]
            self.m_3[0]    = entry.Electron_mass[jt1]
            self.q_3[0]    = entry.Electron_charge[jt1]
            self.d0_3[0]   = entry.Electron_dxy[jt1]
            self.dZ_3[0]   = entry.Electron_dz[jt1]
            self.iso_3[0]  = entry.Electron_pfRelIso03_all[jt1]
            self.iso_3[0]  = 0. 
            if entry.Electron_mvaFall17V2noIso_WP90[jt1] : self.iso_3[0] = 1.
            
            try : self.gen_match_3[0] = ord(entry.Electron_genPartFlav[jt1])
            except AttributeError : self.gen_match_3[0] = -1
            
            tau1.SetPtEtaPhiM(entry.Electron_pt[jt1], entry.Electron_eta[jt1], entry.Electron_phi[jt1], tauMass)
                                                                                                        #???
            # fill genMatch for tau(ele)
            if isMC:
                idx_genEle = entry.Electron_genPartIdx[jt1]

                # if idx_genEle = -1, no match was found
                if idx_genEle >= 0:
                    idx_genEle_mom      = entry.GenPart_genPartIdxMother[idx_genEle]
                    self.pt_3_tr[0]     = entry.GenPart_pt[idx_genEle]
                    self.phi_3_tr[0]    = entry.GenPart_phi[idx_genEle]
                    self.eta_3_tr[0]    = entry.GenPart_eta[idx_genEle]

            self.pt_4[0]     = entry.Muon_pt[jt2]
            self.phi_4[0]    = entry.Muon_phi[jt2]
            self.eta_4[0]    = entry.Muon_eta[jt2]
            self.m_4[0]      = entry.Muon_mass[jt2]
            self.q_4[0]      = entry.Muon_charge[jt2]
            self.d0_4[0]     = entry.Muon_dxy[jt2]
            self.dZ_4[0]     = entry.Muon_dz[jt2]
            self.iso_4[0]    = entry.Muon_pfRelIso04_all[jt2]
            self.iso_4_ID[0] = 0
            if entry.Muon_mediumId[jt2] : self.iso_4_ID[0] = 1
            
            try : self.gen_match_4[0] = ord(entry.Muon_genPartFlav[jt2]) 
            except AttributeError : self.gen_match_4[0] = -1
            
            tau2.SetPtEtaPhiM(entry.Muon_pt[jt2], entry.Muon_eta[jt2], entry.Muon_phi[jt2], tauMass) 

            # fill genMatch for tau(mu)
            if isMC:
                idx_genMu = entry.Muon_genPartIdx[jt2]
                
                # if idx_genMu = -1, no match was found
                if idx_genMu >= 0:
                    idx_genMu_mom       = entry.GenPart_genPartIdxMother[idx_genMu]
                    self.pt_4_tr[0]     = entry.GenPart_pt[idx_genMu]
                    self.phi_4_tr[0]    = entry.GenPart_phi[idx_genMu]
                    self.eta_4_tr[0]    = entry.GenPart_eta[idx_genMu]

	    '''tauListMu=[]
	    tauListE=[jt1]
	    tauListMu=[jt2]
	    TrigListETau=[]
	    TrigListETau = GF.findETrigger(tauListE, entry, era)
	    TrigListMuTau=[]
	    TrigListMuTau = GF.findETrigger(tauListMu, entry, era)

            if isMC :

	        if len(TrigListETau) == 1 :
		    sf_T1_MC = self.sf_EleTrig35.get_EfficiencyMC(entry.Electron_pt[jt1],entry.Electron_eta[jt1])
		    sf_T1_Data = self.sf_EleTrig35.get_EfficiencyData(entry.Electron_pt[jt1],entry.Electron_eta[jt1])
	        if len(TrigListMuTau) == 1 :
		    sf_T2_MC = self.sf_MuonTrigIso27.get_EfficiencyMC(entry.Muon_pt[jt2],entry.Muon_eta[jt2])
		    sf_T2_Data = self.sf_MuonTrigIso27.get_EfficiencyData(entry.Muon_pt[jt2],entry.Muon_eta[jt2])
            '''

        # Fill variables for Leg3, where 3->tau(mu) and 4->tau(had)
        elif channel == 'mt' :
            self.pt_3[0]     = entry.Muon_pt[jt1]
            self.phi_3[0]    = entry.Muon_phi[jt1]
            self.eta_3[0]    = entry.Muon_eta[jt1]
            self.m_3[0]      = entry.Muon_mass[jt1]
            self.q_3[0]      = entry.Muon_charge[jt1]
            self.d0_3[0]     = entry.Muon_dxy[jt1]
            self.dZ_3[0]     = entry.Muon_dz[jt1]
            self.iso_3[0]    = entry.Muon_pfRelIso04_all[jt1]
            self.iso_3_ID[0] = 0
            if entry.Muon_mediumId[jt1] : self.iso_3_ID[0] = 1
            
            try : self.gen_match_3[0] = ord(entry.Muon_genPartFlav[jt1])
            except AttributeError : self.gen_match_1[0] = -1
            
            tau1.SetPtEtaPhiM(entry.Muon_pt[jt1], entry.Muon_eta[jt1], entry.Muon_phi[jt1], tauMass)
            tau2.SetPtEtaPhiM(entry.Tau_pt[jt2],  entry.Tau_eta[jt2],  entry.Tau_phi[jt2],  tauMass) 
            
            # fill genMatch for tau(mu)
            if isMC:
                idx_genMu = entry.Muon_genPartIdx[jt1]
                
                # if idx_genMu = -1, no match was found
                if idx_genMu >= 0:
                    idx_genMu_mom       = entry.GenPart_genPartIdxMother[idx_genMu]
                    self.pt_3_tr[0]     = entry.GenPart_pt[idx_genMu]
                    self.phi_3_tr[0]    = entry.GenPart_phi[idx_genMu]
                    self.eta_3_tr[0]    = entry.GenPart_eta[idx_genMu]
                    
 	    '''tauListMu=[]
	    tauListMu=[jt1]
	    TrigListMuTau=[]
	    TrigListMuTau = GF.findETrigger(tauListMu, entry, era)

            if isMC :

		    if len(TrigListMuTau) == 1 :
			sf_T1_MC = self.sf_MuonTrigIso27.get_EfficiencyMC(entry.Muon_pt[jt1],entry.Muon_eta[jt1])
			sf_T1_Data = self.sf_MuonTrigIso27.get_EfficiencyData(entry.Muon_pt[jt1],entry.Muon_eta[jt1])


            '''
        
        # Fill variables for Leg3 and Leg4, where 3->tau(had) and 4->tau(had)
        elif channel == 'tt' :
            self.pt_3[0]     = entry.Tau_pt[jt1]
            self.phi_3[0]    = entry.Tau_phi[jt1]
            self.eta_3[0]    = entry.Tau_eta[jt1]
            self.m_3[0]      = entry.Tau_mass[jt1]
            self.q_3[0]      = entry.Tau_charge[jt1]
            self.d0_3[0]     = entry.Tau_dxy[jt1]
            self.dZ_3[0]     = entry.Tau_dz[jt1]
            self.iso_3[0]    = entry.Tau_rawMVAoldDM2017v2[jt1]
            self.iso_3_ID[0] = ord(entry.Tau_idMVAnewDM2017v2[jt1])
 
            self.againstElectronVLooseMVA6_3[0]  = self.getAntiEle(entry,jt1,1)
            self.againstElectronLooseMVA6_3[0]   = self.getAntiEle(entry,jt1,2)
            self.againstElectronMediumMVA6_3[0]  = self.getAntiEle(entry,jt1,4)
            self.againstElectronTightMVA6_3[0]   = self.getAntiEle(entry,jt1,8)
            self.againstElectronVTightMVA6_3[0]  = self.getAntiEle(entry,jt1,16)
            self.againstMuonLoose3_3[0]          = self.getAntiMu(entry,jt1,1)
            self.againstMuonTight3_3[0]          = self.getAntiMu(entry,jt1,2)                            
            self.byIsolationMVA3oldDMwLTraw_3[0] = 0.  
    
            # genMatch the hadronic tau candidate
            idx_t1_gen = GF.genMatchTau(entry, jt1, 'had')
            if idx_t1_gen >= 0:
                self.pt_3_tr[0]  = entry.GenVisTau_pt[idx_t1_gen]
                self.phi_3_tr[0] = entry.GenVisTau_phi[idx_t1_gen]
                self.eta_3_tr[0] = entry.GenVisTau_eta[idx_t1_gen]
            else:
                self.pt_3_tr[0]  = 1.2*entry.Tau_pt[jt1]
                self.phi_3_tr[0] = 1.2*entry.Tau_phi[jt1]
                self.eta_3_tr[0] = 1.2*entry.Tau_eta[jt1]

            try : self.gen_match_3[0] = ord(entry.Tau_genPartFlav[jt1])
            except AttributeError : self.gen_match_3[0] = -1

            try : self.decayMode_3[0] = int(entry.Tau_decayMode[jt1])
            except AttributeError : self.decayMode_3[0] = -1

            tau1.SetPtEtaPhiM(entry.Tau_pt[jt1], entry.Tau_eta[jt1], entry.Tau_phi[jt1], tauMass)
            tau2.SetPtEtaPhiM(entry.Tau_pt[jt2], entry.Tau_eta[jt2], entry.Tau_phi[jt2], tauMass)
            
        else :
            print("Invalid channel={0:s} in outTuple(). Exiting.".format(channel))
            exit()
            
        self.mt_3[0]      = self.get_mt('MVAMet',   entry,tau1)
        self.pfmt_3[0]    = self.get_mt('PFMet',    entry,tau1)
        self.puppimt_3[0] = self.get_mt('PUPPIMet', entry,tau1)

        self.trigweight_3[0]  = -999.   
        self.idisoweight_3[0] = -999.   
	
        # Fill variables for Leg4, where 4->tau(had)
        if channel != 'em':
	    self.pt_4[0]  = entry.Tau_pt[jt2]
            self.phi_4[0] = entry.Tau_phi[jt2]
            self.eta_4[0] = entry.Tau_eta[jt2]
            self.m_4[0]   = entry.Tau_mass[jt2]
            self.q_4[0]   = entry.Tau_charge[jt2]
            self.d0_4[0]  = entry.Tau_dxy[jt2]
            self.dZ_4[0]  = entry.Tau_dz[jt2]
            
            phi, pt = entry.Tau_phi[jt2], entry.Tau_pt[jt2]
            
            self.mt_4[0]      = self.get_mt('MVAMet',   entry, tau2) 
            self.pfmt_4[0]    = self.get_mt('PFMet',    entry, tau2)
            self.puppimt_4[0] = self.get_mt('PUPPIMet', entry, tau2) 
            self.iso_4[0]     = entry.Tau_rawMVAoldDM2017v2[jt2]
            self.iso_4_ID[0]  = ord(entry.Tau_idMVAnewDM2017v2[jt2]) 

            self.againstElectronVLooseMVA6_4[0]  = self.getAntiEle(entry, jt2, 1)
            self.againstElectronLooseMVA6_4[0]   = self.getAntiEle(entry, jt2, 2)
            self.againstElectronMediumMVA6_4[0]  = self.getAntiEle(entry, jt2, 4)
            self.againstElectronTightMVA6_4[0]   = self.getAntiEle(entry, jt2, 8)
            self.againstElectronVTightMVA6_4[0]  = self.getAntiEle(entry, jt2, 16)
            self.againstMuonLoose3_4[0]          = self.getAntiMu( entry, jt2, 1)
            self.againstMuonTight3_4[0]          = self.getAntiMu( entry, jt2, 2)
            self.byIsolationMVA3oldDMwLTraw_4[0] = float(ord(entry.Tau_idMVAoldDMdR032017v2[jt2]))  # check this

            # genMatch the hadronic tau candidate
            idx_t2_gen = GF.genMatchTau(entry, jt2, 'had')
            if idx_t2_gen >= 0:
                self.pt_4_tr[0]  = entry.GenVisTau_pt[idx_t2_gen]
                self.phi_4_tr[0] = entry.GenVisTau_phi[idx_t2_gen]
                self.eta_4_tr[0] = entry.GenVisTau_eta[idx_t2_gen]
            else:
                self.pt_4_tr[0]  = 1.2*entry.Tau_pt[jt2]
                self.phi_4_tr[0] = 1.2*entry.Tau_phi[jt2]
                self.eta_4_tr[0] = 1.2*entry.Tau_eta[jt2]

	    try : self.gen_match_4[0] = ord(entry.Tau_genPartFlav[jt2])
	    except AttributeError: self.gen_match_4[0] = -1

            try : self.decayMode_4[0] = int(entry.Tau_decayMode[jt2])
            except AttributeError: self.decayMode_4[0] = -1

            self.trigweight_4[0]  = -999.   # requires sf need help from Sam on these
            self.idisoweight_4[0] = -999.   # requires sf need help from Sam on these

            # di-tau variables
            self.pt_tt[0]  = self.getPt_tt( entry, tau1, tau2)
            self.mt_tot[0] = self.getMt_tot(entry, tau1, tau2)
            self.m_vis[0]  = self.getM_vis( entry, tau1, tau2)
            
        if SVFit :
            fastMTTmass, fastMTTtransverseMass = self.runSVFit(entry, channel, jt1, jt2, tau1, tau2) 
        else :
            fastMTTmass, fastMTTtransverseMass = -999., -999.
            
        self.m_sv[0] = fastMTTmass 
        self.mt_sv[0] = fastMTTtransverseMass  

        # di-lepton variables.   _p and _m refer to plus and minus charge
        self.ll_lmass[0]  = LepP.M() 
        self.mll[0]       = (LepP + LepM).M()

        # Sort the di-lepton system by Pt
        Lep1, Lep2 = TLorentzVector(), TLorentzVector()
        if (LepP.Pt() > LepM.Pt()): 
            Lep1 = LepP
            Lep2 = LepM
        else:
            Lep1 = LepM
            Lep2 = LepP
            
        self.pt_1[0]   = Lep1.Pt()
        self.phi_1[0]  = Lep1.Phi()
        self.eta_1[0]  = Lep1.Eta()
        self.pt_2[0]   = Lep2.Pt()
        self.phi_2[0]  = Lep2.Phi()
        self.eta_2[0]  = Lep2.Eta()
        
        # genMatch the di-lepton variables
        idx_Lep1, idx_Lep2 = -1, -1
        idx_Lep1_tr, idx_Lep2_tr = -1, -1
        if (Lep1.M() > 0.05 and Lep2.M() > 0.05): # muon mass 
            idx_Lep1 = GF.getLepIdxFrom4Vec(entry, Lep1, 'm')
            idx_Lep2 = GF.getLepIdxFrom4Vec(entry, Lep2, 'm')
            idx_Lep1_tr = entry.Muon_genPartIdx[idx_Lep1]
            idx_Lep2_tr = entry.Muon_genPartIdx[idx_Lep2]
        elif (Lep1.M() < 0.05 and Lep2.M() < 0.05): # electron mass
            idx_Lep1 = GF.getLepIdxFrom4Vec(entry, Lep1, 'e')
            idx_Lep2 = GF.getLepIdxFrom4Vec(entry, Lep2, 'e')
            idx_Lep1_tr = entry.Electron_genPartIdx[idx_Lep1]
            idx_Lep2_tr = entry.Electron_genPartIdx[idx_Lep2]
            
        if idx_Lep1_tr >= 0 and idx_Lep2_tr >= 0:
            self.pt_1_tr[0]  = entry.GenPart_pt[idx_Lep1_tr]
            self.pt_2_tr[0]  = entry.GenPart_pt[idx_Lep2_tr]
            self.eta_1_tr[0] = entry.GenPart_eta[idx_Lep1_tr]
            self.eta_2_tr[0] = entry.GenPart_eta[idx_Lep2_tr]
            self.phi_1_tr[0] = entry.GenPart_phi[idx_Lep1_tr]
            self.phi_2_tr[0] = entry.GenPart_phi[idx_Lep2_tr]
        
        # MET variables
        self.met[0]         = entry.MET_pt    
        self.metphi[0]      = entry.MET_phi
        self.puppimet[0]    = entry.PuppiMET_pt
        self.puppimetphi[0] = entry.PuppiMET_phi
        
        self.metcov00[0] = entry.MET_covXX
        self.metcov01[0] = entry.MET_covXY
        self.metcov10[0] = entry.MET_covXY	
        self.metcov11[0] = entry.MET_covYY

        # trigger sf
        self.trig_Lp_MC[0]   = sf_Lp_MC
        self.trig_Lp_Data[0] = sf_Lp_Data
        self.trig_Lm_MC[0]   = sf_Lm_MC
        self.trig_Lm_Data[0] = sf_Lm_Data
        self.trig_T1_MC[0]   = sf_T1_MC
        self.trig_T1_Data[0] = sf_T1_Data
        self.trig_T2_MC[0]   = sf_T2_MC
        self.trig_T2_Data[0] = sf_T2_Data

        if sf_Lp_MC != 0. or sf_Lm_MC != 0. or sf_T1_MC != 0. or sf_T2_MC != 0. :   self.is_trig[0] = 1 # either Z or H or both
        if sf_Lp_MC == 0. and sf_Lm_MC == 0. and (sf_T1_MC != 0. or sf_T2_MC != 0.) :   self.is_trigH[0] = 1 # H fired the trigger
        if (sf_Lp_MC != 0. or sf_Lm_MC != 0.) and (sf_T1_MC == 0. and sf_T2_MC == 0.) :   self.is_trigZ[0] = 1 # Z fired the trigger
        if (sf_Lp_MC != 0. or sf_Lm_MC != 0.) and (sf_T1_MC != 0. or sf_T2_MC != 0.) :   self.is_trigZH[0] = 1 # either Z or H or both fired it

        # jet variables
        nJet30, jetList, bJetList = self.getJets(entry,tau1,tau2,era) 
        self.njetspt20[0] = len(jetList)
        self.njets[0] = nJet30
        self.nbtag[0] = len(bJetList)
        
        self.jpt_1[0], self.jeta_1[0], self.jphi_1[0], self.jcsv_1[0] = -9.99, -9.99, -9.99, -9.99 
        if len(jetList) > 0 :
            jj1 = jetList[0]
            self.jpt_1[0]  = entry.Jet_pt[jj1]
            self.jeta_1[0] = entry.Jet_eta[jj1]
            self.jphi_1[0] = entry.Jet_phi[jj1]
            self.jcsv_1[0] = entry.Jet_btagDeepB[jj1]

            # genMatch jet1
            idx_genJet = entry.Jet_genJetIdx[jj1]
            if idx_genJet >= 0:
                self.jpt_1_tr[0]  = entry.GenJet_pt[idx_genJet]
                self.jeta_1_tr[0] = entry.GenJet_eta[idx_genJet]
                self.jphi_1_tr[0] = entry.GenJet_phi[idx_genJet]

        self.jpt_2[0], self.jeta_2[0], self.jphi_2[0], self.jcsv_2[0] = -9.99, -9.99, -9.99, -9.99 
        if len(jetList) > 1 :
            jj2 = jetList[1] 
            self.jpt_2[0]  = entry.Jet_pt[jj2]
            self.jeta_2[0] = entry.Jet_eta[jj2]
            self.jphi_2[0] = entry.Jet_phi[jj2]
            self.jcsv_2[0] = entry.Jet_btagDeepB[jj2]
            
            # genMatch jet2
            idx_genJet = entry.Jet_genJetIdx[jj2]
            if idx_genJet >= 0:
                self.jpt_2_tr[0]  = entry.GenJet_pt[idx_genJet]
                self.jeta_2_tr[0] = entry.GenJet_eta[idx_genJet]
                self.jphi_2_tr[0] = entry.GenJet_phi[idx_genJet]

        self.bpt_1[0], self.beta_1[0], self.bphi_1[0], self.bcsv_1[0] = -9.99, -9.99, -9.99, -9.99
        if len(bJetList) > 0 :
            jbj1 = bJetList[0]
            self.bpt_1[0] = entry.Jet_pt[jbj1]
            self.beta_1[0] = entry.Jet_eta[jbj1]
            self.bphi_1[0] = entry.Jet_phi[jbj1]
            self.bcsv_1[0] = entry.Jet_btagDeepB[jbj1] 
            
            # genMatch bjet1
            idx_genJet = entry.Jet_genJetIdx[jbj1]
            if idx_genJet >= 0:
                self.bpt_1_tr[0] = entry.GenJet_pt[idx_genJet]
                self.beta_1_tr[0] =entry.GenJet_eta[idx_genJet]
                self.bphi_1_tr[0] =entry.GenJet_phi[idx_genJet]

        self.bpt_2[0], self.beta_2[0], self.bphi_2[0], self.bcsv_2[0] = -9.99, -9.99, -9.99, -9.99
        if len(bJetList) > 1 :
            jbj2 = bJetList[1] 
            self.bpt_2[0] = entry.Jet_pt[jbj2]
            self.beta_2[0] = entry.Jet_eta[jbj2]
            self.bphi_2[0] = entry.Jet_phi[jbj2]
            self.bcsv_2[0] = entry.Jet_btagDeepB[jbj2]

            # genMatch bjet1
            idx_genJet = entry.Jet_genJetIdx[jbj2]
            if idx_genJet >= 0:
                self.bpt_2_tr[0]  = entry.GenJet_pt[idx_genJet]
                self.beta_2_tr[0] = entry.GenJet_eta[idx_genJet]
                self.bphi_2_tr[0] = entry.GenJet_phi[idx_genJet]

        self.t.Fill()
        #self.weight[0] = 1.
        return

    def setWeight(self,weight) :
        self.weight[0] = weight
        #print("outTuple.setWeight() weight={0:f}".format(weight))
        return

    def writeTree(self) :
        print("In outTuple.writeTree() entries={0:d}".format(self.entries)) 
        self.f.Write()
        self.f.Close()
        return

    
