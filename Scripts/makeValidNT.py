import json
import sys
import argparse

parser = argparse.ArgumentParser(description='Makes a valid normtag given a CSV from brilcalc')
parser.add_argument('-i', '--input', type=str, default="", help='CSV file from brilcalc.')
parser.add_argument('-o', '--output', type=str, default="mynormtag.json", help='output file name')
parser.add_argument('-n', '--normtag', type=str, default="pccLUM15001", help='String of normtag')
parser.add_argument('-s', '--skiplist', type=str, default="", help='List of runs to filter out')
parser.add_argument('--jsontype', type=str, default="normtag", help='normtag or cert')
args = parser.parse_args()

def CondensedList(fullList):
    condensedList=[]
    lastLS=0
    for iLS in fullList:
        if iLS==fullList[0]:
            condensedList.append([iLS,-1])
        elif iLS-lastLS>1:
            condensedList[-1][1]=lastLS
            condensedList.append([iLS,-1])
        
        if iLS==fullList[-1]:
            condensedList[-1][1]=iLS

        lastLS=iLS

    return condensedList


if args.input=="":
    print "File needed to analyze"
    sys.exit(-1)
else:
    try:
        csvfile=open(args.input)
    except:
        print "Can't open",args.input,"... exiting"
        sys.exit(-1)

skipList=args.skiplist.split(",") #just runs 

lines=csvfile.readlines()
csvfile.close()

validData={}

for line in lines:
    try:
        items=line.split(",")
        run=int(items[0].split(":")[0])
        LS=int(items[1].split(":")[0])

    except:
        print "Can't parse",line
        continue

    if str(run) in skipList:
        continue

    if run not in validData.keys():
        validData[run]=[]

    validData[run].append(LS)

runs=validData.keys()
runs.sort()

outputFile=open(args.output,"w")
if args.jsontype.find("normtag")==0:
    outputFile.write("[\n")
elif args.jsontype.find("cert")==0:
    outputFile.write("{\n")
else:
    print "didn't find normtag or cert in",args.jsontype

for run in runs:
    validData[run].sort()
    print run, 
    print "condensed",CondensedList(validData[run])

    # example line:    ["hfoc16v1",{"271037":[[1,15]]}],
    if args.jsontype.find("normtag")==0:
        outputFile.write("[\""+args.normtag+"\",{\""+str(run)+"\":"+str(CondensedList(validData[run]))+"}]")
    elif args.jsontype.find("cert")==0:
        outputFile.write("\""+str(run)+"\":"+str(CondensedList(validData[run])))
    if run != runs[-1]:
        outputFile.write(",\n")
        
if args.jsontype.find("normtag")==0:
    outputFile.write("\n]\n")
elif args.jsontype.find("cert")==0:
    outputFile.write("\n}\n")
outputFile.close()
