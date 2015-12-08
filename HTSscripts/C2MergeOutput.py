import os
import sys
import pandas
import json
import argparse

def parseArgs():
    parser=argparse.ArgumentParser(description="Gathers completed imagelog files for a QFA experiment, concatenates them and writes files to current directory.  Should be executed from a directory containing images which have been analysed by colonyzer2.")
    parser.add_argument("-i","--id", type=str, help="ID for labelling output", default="Concatenated")
    args = parser.parse_args()
    return(args)

def main():
    args=parseArgs()
    # Should execute this script from LOGS3 directory
    rootDir=os.getcwd()

    expt=str(args.id)

    datdir="Output_Data"
    print("Finding images")
    flist=os.listdir(datdir)

    outFiles=[f for f in flist if os.path.basename(f).split(".")[-1]=="out"]
    datFiles=[f for f in flist if os.path.basename(f).split(".")[-1]=="dat"]

    print("Reading in expected output files")
    outDFs=[pandas.read_csv(os.path.join(datdir,f),sep="\t") for f in outFiles]
    datDFs=[pandas.read_csv(os.path.join(datdir,f),sep="\t",header=None) for f in datFiles]

    print("Merging output files")
    outDF=pandas.concat(outDFs)
    datDF=pandas.concat(datDFs)

    print("Writing merged output to file")
    outDF.to_csv(os.path.join(rootDir,expt+".out"),"\t",index=False,header=True)
    datDF.to_csv(os.path.join(rootDir,expt+".dat"),"\t",index=False,header=False)
	
if __name__ == '__main__':
    main()


