import os
import sys
import pandas
import json

def main():

	args=sys.argv
	# Should execute this script from LOGS3 directory
	rootDir=os.getcwd()
	#rootDir="F://LOGS3"
	#args=["dummy","QFA0060"]

	expt=args[1]
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

	print("Reading in expected output files")
	outDFs=[pandas.read_csv(f,sep="\t") for f in outFiles]
	datDFs=[pandas.read_csv(f,sep="\t",header=None) for f in datFiles]

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


