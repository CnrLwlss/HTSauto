# Find all photos corresponding to a given QFA barcode

import sys
import argparse
import os
import pandas
import colonyzer2.functions as c2
from datetime import datetime
import json
import shutil
import string


def parseArgs():
    parser=argparse.ArgumentParser(description="Build directory of symlinks/shortcuts to images, or image files from QFA file archive for a single barcode.  Execute from LOGS3 directory to use archived file paths.")
    parser.add_argument("barcode", type=str, help="QFA barcode e.g. K000352_027_004")
    args = parser.parse_args()
    return(args)

def main():
    #sys.argv=['test', 'K000352_027_004']
    args=parseArgs()
    rootDir=os.getcwd()

    barc=str(args.barcode)

    # Search in some directories for images that can be analysed
    List_96=["/home/yeastimages/CAPTURED_IMAGES_CYTOMAT_96","/home/yeastimages/CAPTURED_IMAGES_STANDALONE_96","/home/yeastimages/CAPTURED_IMAGES_WARMROOM_96"]
    List_384=["/home/yeastimages/CAPTURED_IMAGES_CYTOMAT","/home/yeastimages/CAPTURED_IMAGES_STANDALONE","/home/yeastimages/CAPTURED_IMAGES_WARMROOM"]
    List_768=["/home/yeastimages/CAPTURED_IMAGES_CYTOMAT_768","/home/yeastimages/CAPTURED_IMAGES_STANDALONE_768","/home/yeastimages/CAPTURED_IMAGES_WARMROOM_768"]
    List_1536=["/home/yeastimages/CAPTURED_IMAGES_CYTOMAT_1536","/home/yeastimages/CAPTURED_IMAGES_STANDALONE_1536","/home/yeastimages/CAPTURED_IMAGES_WARMROOM_1536"]
    Archive_384=["/home/yeastimages/ARCHIVE_IMAGES"]

    # Should 768 be included in QFA (e.g. Pombe QFA)? What about 96-format?
    searchOptions={"QFA":List_384+Archive_384,"MQFQFA":List_384,"SGA":List_1536+List_768,"MQFSGA":List_1536}
    ##searchDirs=searchOptions[exptType]

    barcLen=len(args.barcode)

    jsonfiles=[f for f in os.listdir(".")  if f.endswith("_file_locations.json")]
    barclist=[]
    for jsonfile in jsonfiles:
        with open(jsonfile) as f:
            barclist.append(json.load(f))
    barcdict=c2.merge_lodols(barclist)

    barcdict={x:set(barcdict[x]) for x in [args.barcode]}

    barcFiles=[item for sublist in barcdict.values() for item in sublist]
                    
    ##    print("Filtering images beyond cutoff from list to be analysed")
    ##    for i in xrange(0,len(metaDF["Barcode"])):
    ##        barc=metaDF["Barcode"].iloc[i]
    ##        inoc=metaDF["Start.Time"].iloc[i]
    ##        flist=barcDict[barc]
    ##        nimages=len(barcDict[barc])
    ##        dates=[(c2.getDate(f)-datetime.strptime(inoc,"%Y-%m-%d_%H-%M-%S")).total_seconds()/(24*60*60) for f in flist]
    ##        barcDict[barc]=[f for ind,f in enumerate(flist) if dates[ind]<=cutoff]
    ##        print("Will ignore last "+str(nimages-len(barcDict[barc]))+" images from "+barc)

    dirname="../pdump"
    if os.path.exists(dirname):
        shutil.rmtree(dirname)
    os.mkdir(dirname)
    os.mkdir(os.path.join(dirname,"Output_Images"))
    os.mkdir(os.path.join(dirname,"Output_Data"))
    for barc in barcdict.keys():
        for f in barcdict[barc]:
            fname=os.path.basename(f)
            im=os.path.join(os.path.dirname(f),"Output_Images",fname.split(".")[0]+".png")
            dat=os.path.join(os.path.dirname(f),"Output_Data",fname.split(".")[0]+".dat")
            out=os.path.join(os.path.dirname(f),"Output_Data",fname.split(".")[0]+".out")
            targ=os.path.join(dirname,fname)
            print("Copying "+f+" to "+targ)
            os.symlink(f,targ)
            os.symlink(im,os.path.join(dirname,"Output_Images",os.path.basename(im)))
            os.symlink(dat,os.path.join(dirname,"Output_Data",os.path.basename(dat)))
            os.symlink(out,os.path.join(dirname,"Output_Data",os.path.basename(out)))

if __name__ == '__main__':
    main()




