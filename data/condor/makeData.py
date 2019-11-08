
# generate a runData.csh script that creates the .csh and .jdl files
# to process data 

import os

def getArgs() :
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("-f","--inFile",default='datasets.txt',help="Input file name.")
    parser.add_argument("-y","--year",default=2016,type=str,help="Data taking period, 2016, 2017 or 2018")
    return parser.parse_args()

args = getArgs() 
outLines = []
cwd = os.getcwd()

for line in open(args.inFile,'r').readlines() :
    dataset = line.strip() 
    if len(dataset) < 2 : continue
    nickname = dataset.split('/')[1] + '_' + dataset.split('/')[2].split('-')[0] 
    if args.year not in nickname : continue
    print("dataset={0:s} nickname={1:s}".format(dataset,nickname))

    mode = 'anaXRD'
    outLines.append("mkdir {0:s}\ncd {0:s}\n".format(nickname))
    outLines.append("python ../makeCondor.py --dataSet {0:s} --nickName {1:s} --mode {2:s} -y {3:s} \n".format(dataset,nickname, mode, args.year))
    outLines.append("cd {0:s}\n".format(cwd))
    
open('runData.csh','w').writelines(outLines)



    
    
