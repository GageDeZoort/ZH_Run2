#!/usr/bin/env python

""" ZH.py: makes an nTuple for the ZH->tautau analysis """

__author__ = "Dan Marlow, Alexis Kalogeropoulos, Gage DeZoort" 
__version__ = "GageDev_v1.1"

# import external modules 
import sys
import numpy as np
from ROOT import TFile, TTree, TH1, TH1D, TCanvas, TLorentzVector  
from math import sqrt, pi

# import from ZH_Run2/funcs/
sys.path.insert(1,'../funcs/')
import tauFun
import generalFunctions as GF 
import outTuple
import time

def getArgs() :
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-v","--verbose",default=0,type=int,help="Print level.")
    parser.add_argument("-f","--inFileName",default='ZHtoTauTau_test.root',help="File to be analyzed.")
    parser.add_argument("-c","--category",default='none',help="Event category to analyze.")
    parser.add_argument("--nickName",default='',help="MC sample nickname") 
    parser.add_argument("-d","--dataType",default='MC',help="Data or MC") 
    parser.add_argument("-o","--outFileName",default='',help="File to be used for output.")
    parser.add_argument("-n","--nEvents",default=0,type=int,help="Number of events to process.")
    parser.add_argument("-m","--maxPrint",default=0,type=int,help="Maximum number of events to print.")
    parser.add_argument("-t","--testMode",default='',help="tau MVA selection")
    parser.add_argument("-y","--year",default=2017,type=int,help="Data taking period, 2016, 2017 or 2018")
    parser.add_argument("-s","--selection",default='ZH',help="is this for the ZH or the AZH analysis?")
    parser.add_argument("-u","--unique",default='none',help="CSV file containing list of unique events for sync studies.") 
    parser.add_argument("-w","--weights",default=False,type=int,help="to re-estimate Sum of Weights")
    
    return parser.parse_args()

args = getArgs()
print("args={0:s}".format(str(args)))
maxPrint = args.maxPrint 

cutCounter = {}
cutCounterGenWeight = {}

#cats = ['eee','eem','eet', 'mmm', 'mme', 'mmt']
cats = ['ee','mm']

for cat in cats : 
    cutCounter[cat] = GF.cutCounter()
    cutCounterGenWeight[cat] = GF.cutCounter()

inFileName = args.inFileName
print("Opening {0:s} as input.  Event category {1:s}".format(inFileName,cat))

isAZH=False
if str(args.selection) == 'AZH' : isAZH = True
if isAZH : print 'You are running on the AZH mode !!!'

inFile = TFile.Open(inFileName)
inFile.cd()
inTree = inFile.Get("Events")
nentries = inTree.GetEntries()
nMax = nentries
print("nentries={0:d} nMax={1:d}".format(nentries,nMax))
if args.nEvents > 0 : nMax = min(args.nEvents-1,nentries)


MC = len(args.nickName) > 0 
if args.dataType == 'Data' or args.dataType == 'data' : MC = False
if args.dataType == 'MC' or args.dataType == 'mc' : MC = True

if MC :
    print "this is MC, will get PU etc", args.dataType
    PU = GF.pileUpWeight()
    PU.calculateWeights(args.nickName,args.year)
else :
    CJ = ''
    if args.year == 2016 : CJ = GF.checkJSON(filein='Cert_271036-284044_13TeV_ReReco_07Aug2017_Collisions16_JSON.txt')
    if args.year == 2017 : CJ = GF.checkJSON(filein='Cert_294927-306462_13TeV_EOY2017ReReco_Collisions17_JSON.txt')
    if args.year == 2018 : CJ = GF.checkJSON(filein='Cert_314472-325175_13TeV_17SeptEarlyReReco2018ABC_PromptEraD_Collisions18_JSON.txt')


era=str(args.year)

outFileName = GF.getOutFileName(args).replace(".root",".ntup")

if MC : 
    if "WJetsToLNu" in outFileName:
	hWxGenweightsArr = []
	for i in range(5):
	    hWxGenweightsArr.append(TH1D("W"+str(i)+"genWeights",\
		    "W"+str(i)+"genWeights",1,-0.5,0.5))
    elif "DYJetsToLL" in outFileName:
	hDYxGenweightsArr = []
	for i in range(5):
	    hDYxGenweightsArr.append(TH1D("DY"+str(i)+"genWeights",\
		    "DY"+str(i)+"genWeights",1,-0.5,0.5))


if args.weights > 0 :
    hWeight = TH1D("hWeights","hWeights",1,-0.5,0.5)
    hWeight.Sumw2()

    for count, e in enumerate(inTree) :
        hWeight.Fill(0, e.genWeight)
    

        if "WJetsToLNu" in outFileName :

            npartons = ord(e.LHE_Njets)
	    if  npartons <= 4: 	hWxGenweightsArr[npartons].Fill(0, e.genWeight)
        if "DYJetsToLL" in outFileName :
            npartons = ord(e.LHE_Njets)
	    if  npartons <= 4 : hDYxGenweightsArr[npartons].Fill(0, e.genWeight)

    fName = GF.getOutFileName(args).replace(".root",".weights")
    fW = TFile( fName, 'recreate' )
    print 'Will be saving the Weights in', fName
    fW.cd()

    if "WJetsToLNu" in outFileName :
        for i in range(len(hWxGenweightsArr)):
            hWxGenweightsArr[i].Write()
    elif "DYJetsToLL" in outFileName:
        for i in range(len(hDYxGenweightsArr)):
            hDYxGenweightsArr[i].Write()

    hWeight.Write()

#############end weights

# read a CSV file containing a list of unique events to be studied 
unique = False 
if args.unique != 'none' :
    unique = True
    uniqueEvents = set()
    for line in open(args.unique,'r').readlines() : uniqueEvents.add(int(line.strip()))
    print("******* Analyzing only {0:d} events from {1:s} ******.".format(len(uniqueEvents),args.unique))
    
print("Opening {0:s} as output.".format(outFileName))
outTuple = outTuple.outTuple(outFileName, era)


tStart = time.time()
countMod = 1000
isMC = True
for count, e in enumerate(inTree) :
    if count % countMod == 0 :
        print("Count={0:d}".format(count))
        if count >= 10000 : countMod = 10000
    if count == nMax : break    
    
    for cat in cats : 
        cutCounter[cat].count('All')
	if  MC :   cutCounterGenWeight[cat].countGenWeight('All', e.genWeight)

    isInJSON = False
    if not MC : isInJSON = CJ.checkJSON(e.luminosityBlock,e.run)
    if not isInJSON and not MC :
        #print("Event not in JSON: Run:{0:d} LS:{1:d}".format(e.run,e.luminosityBlock))
        continue

    for cat in cats: cutCounter[cat].count('InJSON')
    
    MetFilter = GF.checkMETFlags(e,args.year)
    if MetFilter : continue
    
    for cat in cats: cutCounter[cat].count('METfilter') 

    if unique :
        if e.event in uniqueEvents :
            for cat in cats: cutCounter[cat].count('Unique') 
        else :
            continue

    if not tauFun.goodTrigger(e, args.year) : continue
    
    for cat in cats: 
	cutCounter[cat].count('Trigger')
	if  MC :   cutCounterGenWeight[cat].countGenWeight('Trigger', e.genWeight)
            
    for cat in cats:
        lepMode = cat[:2]
        if args.category != 'none' and not lepMode in args.category : continue

        if lepMode == 'ee' :
            if e.nElectron < 2 : continue
            for cat in cats : 
	        cutCounter[cat].count('LeptonCount')
	        if  MC :   cutCounterGenWeight[cat].countGenWeight('LeptonCount', e.genWeight)
        if lepMode == 'mm' :
            if e.nMuon < 2 : continue 

            for cat in cats : 
	        cutCounter[cat].count('LeptonCount')
	        if  MC :   cutCounterGenWeight[cat].countGenWeight('LeptonCount', e.genWeight)

	lepList=[]

	pairList=[]

        goodElectronList = tauFun.makeGoodElectronList(e)
        goodMuonList = tauFun.makeGoodMuonList(e)
        goodElectronList, goodMuonList = tauFun.eliminateCloseLeptons(e, goodElectronList, goodMuonList)

        # selects a third lepton that is not part of the Z peak already
        goodElectronListExtraLepton = tauFun.makeGoodElectronListExtraLepton(e,goodElectronList)
        goodMuonListExtraLepton = tauFun.makeGoodMuonListExtraLepton(e,goodMuonList)

	tauList = tauFun.getGoodTauList(cat, e)
        goodElectronListExtraLepton, goodMuonListExtraLepton,tauList = tauFun.eliminateCloseTauAndLepton(e, goodElectronListExtraLepton, goodMuonListExtraLepton, tauList)



        if lepMode == 'ee' :

            if len(goodElectronList) < 2 :continue
            cutCounter[cat].count('GoodLeptons')

            pairList, lepList = tauFun.findZ(goodElectronList,[], e)
            if len(lepList) != 2 :
                if unique :
                    print("LepList Fail: : Event ID={0:d} cat={1:s}".format(e.event,cat))
                    GF.printEvent(e)
                    if MC : GF.printMC(e)
                continue
            
        
        if lepMode == 'mm' :

            if len(goodMuonList) < 2 : continue
            cutCounter[cat].count('GoodLeptons')

            pairList, lepList = tauFun.findZ([],goodMuonList, e)
            if len(lepList) != 2 : continue

        if len(pairList) < 1 : continue

        LepP, LepM = pairList[0], pairList[1]
	M = (LepM + LepP).M()

        #if (len( goodMuonList)>1 or len( goodElectronList) >0 ) and len(goodElectronListExtraLepton)> 0 or len(goodMuonListExtraLepton) > 0 or len(tauList): 
        #    print e.event, 'goodEl', goodElectronList, 'goodM', goodMuonList, 'ExtraEl', goodElectronListExtraLepton, 'ExtraM', goodMuonListExtraLepton, 'taus', tauList,lepMode, cat, M

	#just use the highest pT object for mu/el
        if len(goodElectronListExtraLepton) > 0 and len(goodMuonListExtraLepton) > 0 :
	    if e.Electron_pt[goodElectronListExtraLepton[0]] > e.Muon_pt[goodMuonListExtraLepton[0]] : goodMuonListExtraLepton = []
	    else : goodElectronListExtraLepton = []


        if lepMode == 'ee' :
            for cat in cats[:4] : 
	        cutCounter[cat].count('LeptonPair')
	        if  MC :   cutCounterGenWeight[cat].countGenWeight('LeptonPair', e.genWeight)
        if lepMode == 'mm' :
            for cat in cats[4:] : 
	        cutCounter[cat].count('LeptonPair')
	        if  MC :   cutCounterGenWeight[cat].countGenWeight('LeptonPair', e.genWeight)
                
        if not tauFun.mllCut(M) :
            continue 

        if lepMode == 'ee' :
            for cat in cats[:4]: 
	        cutCounter[cat].count('FoundZ')
	        if  MC :   cutCounterGenWeight[cat].countGenWeight('FoundZ', e.genWeight)
        if lepMode == 'mm' :
            for cat in cats[4:]: 
	        cutCounter[cat].count('FoundZ')
	        if  MC :   cutCounterGenWeight[cat].countGenWeight('FoundZ', e.genWeight)
        

	if MC :
	    outTuple.setWeight(PU.getWeight(e.PV_npvs)) 
	    outTuple.setWeightPU(PU.getWeight(e.Pileup_nPU)) 
	    outTuple.setWeightPUtrue(PU.getWeight(e.Pileup_nTrueInt)) 
	    #print 'nPU', e.Pileup_nPU, e.Pileup_nTrueInt, PU.getWeight(e.Pileup_nPU), PU.getWeight(e.Pileup_nTrueInt), PU.getWeight(e.PV_npvs), PU.getWeight(e.PV_npvsGood)
	else : 
	    outTuple.setWeight(1.) 
	    outTuple.setWeightPU(1.) ##
	    outTuple.setWeightPUtrue(1.)


        for cat in ['ee','mm'] :

            '''            
	    if len(goodElectronListExtraLepton) > 0 and len(goodMuonListExtraLepton) > 0 :
                if e.Electron_pt[goodElectronListExtraLepton[0]]  > e.Muon_pt[goodMuonListExtraLepton[0]] : cat = cat+'e'
                else : cat = cat+'m'

	    if len(goodElectronListExtraLepton) > 0 and len(goodMuonListExtraLepton) == 0 : cat = cat+'e'
	    if len(goodElectronListExtraLepton) == 0 and len(goodMuonListExtraLepton) > 0 : cat = cat+'m'
            '''

            #if e.nbtag == 0 : continue
            if len(goodMuonListExtraLepton) == 0 and len(goodElectronListExtraLepton) == 0 and len(tauList) == 0 : continue

            if not MC : isMC = False

            outTuple.Fill3L(e,cat,LepP,LepM,lepList,goodElectronListExtraLepton, goodMuonListExtraLepton, tauList, isMC,era) 

            if maxPrint > 0 :
                maxPrint -= 1
                print("\n\nGood Event={0:d} cat={1:s}  MCcat={2:s}".format(e.event,cat,GF.eventID(e)))
                print("goodMuonList={0:s} goodElectronList={1:s} Mll={2:.1f} bestTauPair={3:s}".format(
                    str(goodMuonList),str(goodElectronList),M,str(bestTauPair)))
                print("Lep1.pt() = {0:.1f} Lep2.pt={1:.1f}".format(pairList[0].Pt(),pairList[1].Pt()))
                GF.printEvent(e)
                print("Event ID={0:s} cat={1:s}".format(GF.eventID(e),cat))
                

dT = time.time() - tStart
print("Run time={0:.2f} s  time/event={1:.1f} us".format(dT,1000000.*dT/count))

hCutFlow=[]
hCutFlowW=[]
countt=0
for cat in cats :
    print('\nSummary for {0:s}'.format(cat))
    cutCounter[cat].printSummary()
    hName="hCutFlow_"+str(cat)
    hNameW="hCutFlowWeighted_"+str(cat)
    hCutFlow.append( TH1D(hName,hName,15,0.5,15.5))
    if MC  : hCutFlowW.append( TH1D(hNameW,hNameW,15,0.5,15.5))
    lcount=len(cutCounter[cat].getYield())
    for i in range(lcount) :
        #hCutFlow[cat].Fill(1, float(cutCounter[cat].getYield()[i]))
        yields = cutCounter[cat].getYield()[i]
        hCutFlow[countt].Fill(i+1, float(yields))
        hCutFlow[countt].GetXaxis().SetBinLabel(i+1,str(cutCounter[cat].getLabels()[i]))

        if MC : 
	    yieldsW = cutCounterGenWeight[cat].getYieldWeighted()[i]
            hCutFlowW[countt].Fill(i+1, float(yieldsW))
            hCutFlowW[countt].GetXaxis().SetBinLabel(i+1,str(cutCounterGenWeight[cat].getLabels()[i]))
        #print cutCounter[cat].getYield()[i], i, cutCounter[cat].getLabels()[i]

    
    hCutFlow[countt].Sumw2()
    if MC : hCutFlowW[countt].Sumw2()
    countt+=1

if not MC : CJ.printJSONsummary()


outTuple.writeTree()

