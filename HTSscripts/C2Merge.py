import os
import sys
import pandas
import json
import argparse

def parseArgs():
    parser=argparse.ArgumentParser(description="Gathers completed imagelog files for a QFA experiment, concatenates them and writes files to appropriate IMAGELOGS directory.  Should be executed from LOGS3 directory.  Requires C2.json file (i.e. run C2Find before running C2Merge).")
    parser.add_argument("exptID", type=str, help="QFA experiment ID, e.g. QFA00001")
    args = parser.parse_args()
    return(args)

def checkFile(f,verbose=True,deleteEmpty=False):
    if os.path.isfile(f):
        if sum(1 for line in open(f))<1:
            if verbose: print(f+" EMPTY")
            if deleteEmpty:
                print("Deleting "+f)
                os.remove(f)
            return(False)
    else:
        if verbose: print(f+" MISSING")
        return(False)
    return(True)

def main():
	args=parseArgs()
	# Should execute this script from LOGS3 directory
	rootDir=os.getcwd()

	expt=str(args.exptID)
	exptType=expt[0:-4]
	dataDir=os.path.join(rootDir,exptType+"_EXPERIMENTS")
	dictOut=os.path.join(dataDir,expt,"AUXILIARY",expt+'_C2.json')

	print("Reading in dictionary describing image locations")
	with open(dictOut, 'rb') as fp:
		barcDict = json.load(fp)

	print("Generating expected output filenames for images")
	barcFiles=[item for sublist in barcDict.values() for item in sublist]
	barcFiles.sort()
	outFiles=[os.path.join(os.path.dirname(f),"Output_Data",os.path.basename(f).split(".")[0]+".out") for f in barcFiles]
	datFiles=[os.path.join(os.path.dirname(f),"Output_Data",os.path.basename(f).split(".")[0]+".dat") for f in barcFiles]

	for i,f in enumerate(outFiles):
            outf=f
            datf=datFiles[i]
            checkout=checkFile(outf,deleteEmpty=True)
            checkdat=checkFile(datf,deleteEmpty=True)

	print("Reading in expected output files")
	outDFs=[pandas.read_csv(f,sep="\t") if (os.path.isfile(f) and sum(1 for line in open(f))>0)  else pandas.DataFrame() for f in outFiles]
	datDFs=[pandas.read_csv(f,sep="\t",header=None) if (os.path.isfile(f) and sum(1 for line in open(f))>0)  else pandas.DataFrame() for f in datFiles]

	print("Merging output files")
	outDF=pandas.concat(outDFs)
	datDF=pandas.concat(datDFs)

	print("Archiving existing output files in IMAGELOGS directory")
	imlogs=os.path.join(dataDir,expt,"IMAGELOGS")
	for f in os.listdir(imlogs):
		if f.endswith(".out") or f.endswith(".dat"):
			os.rename(os.path.join(imlogs,f),os.path.join(imlogs,f+"_ARCHIVE"))

	print("Writing merged output to file")
	outDF.to_csv(os.path.join(dataDir,expt,"IMAGELOGS",expt+"_Concatenated.out"),"\t",index=False,header=True)
	datDF.to_csv(os.path.join(dataDir,expt,"IMAGELOGS",expt+"_Concatenated.dat"),"\t",index=False,header=False)
	
if __name__ == '__main__':
    main()


