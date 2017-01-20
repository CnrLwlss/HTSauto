# Finds images from exptID in our archive and dumps file locations to .json file
# Only images where a specific treatment and medium were applied, captured before a cutoff period after inoculation, are considered
# Optionally copies symlinks to images or image files themselves to pdump directory for inspection/download
# This should read in arguments from the command line
# First argument: experiment ID (e.g. QFA0060)
# Second (optional) argument: cutoff time after inoculation (days)
# If a cutoff time not specified, include all images

import sys
import argparse
import os
import pandas
import colonyzer2.functions as c2
from datetime import datetime
import json
import shutil
import string

def toDelete(filename):
    '''Generate list of output files which should be deleted'''
    base=os.path.basename(filename).split(".")[0]
    path=os.path.dirname(filename)
    candidates=[
        # Archival format (original Colonyzer)
        os.path.join(path,base+"GriddedCorrected.png"),
        os.path.join(path,base+"GriddedThresh.png"),
        os.path.join(path,base+"Histogram.png"),
        os.path.join(path,base+"OUT.dat"),
        # Colonyzer2 format
        os.path.join(path,"Output_Data",base+".dat"),
        os.path.join(path,"Output_Data",base+".out"),
        os.path.join(path,"Output_Images",base+".png")
        ]
    return(candidates)

def parseArgs():
    parser=argparse.ArgumentParser(description="Build .json file describing location of timecourse images for a particular QFA experiment.  Also build directory of symlinks/shortcuts to images, or image files from QFA file archive.  Execute from LOGS3 directory.")
    parser.add_argument("exptID", type=str, help="QFA experiment ID, e.g. QFA00001")
    parser.add_argument("-c","--cutoff",type=float, help="Maximum number of days after inoculation, beyond which images are ignored (e.g. 4.0).")
    parser.add_argument("-t","--treatment",type=str, help="Only return images of plates from experiment to which treatment was applied (e.g. 30).")
    parser.add_argument("-m","--medium",type=str, help="Only return images of plates from experiment which contained this medium (e.g. CSM).")
    parser.add_argument("-p","--photos",action='store_true', help="Copy symlinks to images to ../pdump directory.")
    args = parser.parse_args()
    return(args)

def main():
    #sys.argv=['test', 'QFA0018']
    args=parseArgs()
    # Should execute this script from LOGS3 directory
    rootDir=os.getcwd()

    expt=str(args.exptID)
    copyphotos=args.photos

    exptType=expt[0:-4]

    dataDir=os.path.join(rootDir,exptType+"_EXPERIMENTS")
    expDescFile=os.path.join(dataDir,expt,"AUXILIARY","ExptDescription.txt")
    metaDF=pandas.read_csv(expDescFile,sep="\t")

    print("Possible treatments:")
    trts=metaDF["Treatment"].unique()
    print(string.join([str(trt) for trt in trts],sep="\t"))

    print("Possible media:")
    meds=metaDF["Medium"].unique()
    print(string.join([str(med) for med in meds],sep="\t"))

    # Default behaviour for missing optional arguments
    if args.cutoff is not None:
        cutoff=float(args.cutoff)
    else:
        cutoff=999999999.0
        
    if args.treatment is not None:
        treatment=str(args.treatment)
        metaDF=metaDF[metaDF["Treatment"].astype(str)==treatment]
        print("Only take treatment "+treatment+" for "+expt)
        
    if args.medium is not None:
        medium=str(args.medium)
        metaDF=metaDF[metaDF["Medium"].astype(str)==medium]
        print("Only take medium "+medium+" for "+expt)

    # Strip rows that have nan in barcode column (e.g. QFA0132)
    #metaDF=metaDF[pandas.notnull(metaDF["Barcode"])]

    # Search in some directories for images that can be analysed
    List_96=["/home/yeastimages/CAPTURED_IMAGES_CYTOMAT_96","/home/yeastimages/CAPTURED_IMAGES_STANDALONE_96","/home/yeastimages/CAPTURED_IMAGES_WARMROOM_96"]
    List_384=["/home/yeastimages/CAPTURED_IMAGES_CYTOMAT","/home/yeastimages/CAPTURED_IMAGES_STANDALONE","/home/yeastimages/CAPTURED_IMAGES_WARMROOM"]
    List_768=["/home/yeastimages/CAPTURED_IMAGES_CYTOMAT_768","/home/yeastimages/CAPTURED_IMAGES_STANDALONE_768","/home/yeastimages/CAPTURED_IMAGES_WARMROOM_768","/home/yeastimages/CAPTURED_IMAGES_BM5_768"]
    List_1536=["/home/yeastimages/CAPTURED_IMAGES_CYTOMAT_1536","/home/yeastimages/CAPTURED_IMAGES_STANDALONE_1536","/home/yeastimages/CAPTURED_IMAGES_WARMROOM_1536","/home/yeastimages/CAPTURED_IMAGES_BM5_1536"]
    Archive_384=["/home/yeastimages/ARCHIVE_IMAGES"]

    # Should 768 be included in QFA (e.g. Pombe QFA)? What about 96-format?
    searchOptions={"QFA":List_384+Archive_384,"MQFQFA":List_384,"SGA":List_1536+List_768,"MQFSGA":List_1536}
    searchDirs=searchOptions[exptType]

    barcLen=len(metaDF["Barcode"].iloc[0])

    bdictfname=exptType+".json"
    if not os.path.isfile(bdictfname):
        # Assume that all barcodes have the same format as the first Barcode in metaDF
        barcDict=c2.merge_lodols([c2.getBarcodes(directory,barcRange=(0,barcLen),checkDone=False) for directory in searchDirs])
        with open(bdictfname, 'wb') as f:
            json.dump(barcDict, f)
    else:
        with open(bdictfname) as f:
            barcDict=json.load(f)
        
    # Check that all the barcodes in metaDF appear in the list of files, otherwise throw an error?
    if not set(metaDF["Barcode"])<set(barcDict.keys()):
        print(set(metaDF["Barcode"]))
        raise Exception("There are barcodes in the ExptDescription.txt file for which I cannot find any images!")

    barcDict={x:barcDict[x] for x in metaDF["Barcode"]}

    barcFiles=[item for sublist in barcDict.values() for item in sublist]
    print("Deleting any pre-existing output files")
    cdelete=0
    for f in barcFiles:
        print "Deleting analysis files for: "+f
        candidates=toDelete(f)
        for c in candidates:
            if os.path.exists(c):
                os.remove(c)
                cdelete=cdelete+1
    print str(cdelete) + " analysis files (.png, .out & .dat files) deleted..."
                            
    print("Filtering images beyond cutoff from list to be analysed")
    for i in xrange(0,len(metaDF["Barcode"])):
        barc=metaDF["Barcode"].iloc[i]
        inoc=metaDF["Start.Time"].iloc[i]
        flist=barcDict[barc]
        nimages=len(barcDict[barc])
        dates=[(c2.getDate(f)-datetime.strptime(inoc,"%Y-%m-%d_%H-%M-%S")).total_seconds()/(24*60*60) for f in flist]
        barcDict[barc]=[f for ind,f in enumerate(flist) if dates[ind]<=cutoff]
        print("Will ignore last "+str(nimages-len(barcDict[barc]))+" images from "+barc)

    dictOut=os.path.join(dataDir,expt,"AUXILIARY",expt+'_C2.json')
    print("Writing dictionary of images for analysis to file: "+dictOut)
    with open(dictOut, 'wb') as fp:
        json.dump(barcDict, fp)

    if (copyphotos):
        dirname="../pdump"
        if os.path.exists(dirname):
            shutil.rmtree(dirname)
        os.mkdir(dirname)
        for barc in barcDict.keys():
            for f in barcDict[barc]:
                fname=os.path.basename(f)
                targ=os.path.join(dirname,fname)
                print("Copying "+f+" to "+targ)
                os.symlink(f,targ)



if __name__ == '__main__':
    main()
