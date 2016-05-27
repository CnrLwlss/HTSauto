# Finds images from ID in our archive and dumps file locations to .json file
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
from PIL import Image
from PIL import ImageOps
from PIL import ImageFont
from PIL import ImageDraw 

def parseArgs():
    parser=argparse.ArgumentParser(description="Get representative image of each plate in archive, sort by date, draw barcode on image and save (small) frame preview.")
    parser.add_argument("pfmt", type=str, help="Format of experiment.  Can be one of 96, 384, 76, 1536 or Archive")
    parser.add_argument("-d","--dt",type=float, help="Look for photos taken as close as possible to dt days after first photo.", default=1.5)
    args = parser.parse_args()
    return(args)

def reframe(im,wtarg,htarg=0,fill="black"):
    '''Resize image to new target width and height, preserving aspect ratio by adding borders (instead of by cropping).'''
    w,h=im.size
    if htarg==0:
        wsize,hsize=wtarg,int(round((float(wtarg)/w)*h))
        out=im.resize((wsize,hsize),Image.ANTIALIAS)
    elif float(w)/float(h)>=float(wtarg)/float(htarg):
        wsize,hsize=wtarg,int(round((float(wtarg)/float(w))*float(h)))
        tmp=im.resize((wsize,hsize),Image.ANTIALIAS)
        diff=htarg-hsize
        above=sum([x%2 for x in range(diff)])
        below=diff-above
        out=ImageOps.expand(tmp,border=(0,above,0,below),fill=fill)
    else:
        wsize,hsize=int(round((float(htarg)/float(h))*float(w))),htarg
        tmp=im.resize((wsize,hsize),Image.ANTIALIAS)
        diff=wtarg-wsize
        left=sum([x%2 for x in range(diff)])
        right=diff-left
        out=ImageOps.expand(tmp,border=(left,0,right,0),fill=fill)
    return(out)

def main():
    #sys.argv=['test', '384']
    args=parseArgs()
    pfmt=str(args.pfmt)
    dt=float(args.dt)
    # Should execute this script from LOGS3 directory
    rootDir=os.getcwd()    

    # Search in some directories for images that can be analysed
    List_96=["/home/yeastimages/CAPTURED_IMAGES_CYTOMAT_96","/home/yeastimages/CAPTURED_IMAGES_STANDALONE_96","/home/yeastimages/CAPTURED_IMAGES_WARMROOM_96"]
    List_384=["/home/yeastimages/CAPTURED_IMAGES_CYTOMAT","/home/yeastimages/CAPTURED_IMAGES_STANDALONE","/home/yeastimages/CAPTURED_IMAGES_WARMROOM"]
    List_768=["/home/yeastimages/CAPTURED_IMAGES_CYTOMAT_768","/home/yeastimages/CAPTURED_IMAGES_STANDALONE_768","/home/yeastimages/CAPTURED_IMAGES_WARMROOM_768"]
    List_1536=["/home/yeastimages/CAPTURED_IMAGES_CYTOMAT_1536","/home/yeastimages/CAPTURED_IMAGES_STANDALONE_1536","/home/yeastimages/CAPTURED_IMAGES_WARMROOM_1536"]
    Archive_384=["/home/yeastimages/ARCHIVE_IMAGES"]

    searchOptions={"96":List_96,"384":List_384+Archive_384,"768":List_768,"1536":List_1536,"Archive":Archive_384}
    searchDirs=searchOptions[pfmt]

    barcLen=15 # Make this more general...  Detect barcode based on date format instead...

    barcDict=c2.merge_lodols([c2.getBarcodes(directory,barcRange=(0,barcLen),checkDone=False) for directory in searchDirs])
    barcBest=c2.getNearest(barcDict,dt)
    barcDate={b:c2.getDate(barcBest[b]) for b in barcBest.keys()}
    sortedDate=sorted(barcDate,key=barcDate.get)
    
    dirname="../pdump"
    font = ImageFont.truetype("arial.ttf", 80)
    if os.path.exists(dirname):
        shutil.rmtree(dirname)
    os.mkdir(dirname)
    for i,barc in enumerate(sortedDate):
        im=Image.open(barcBest[barc])
        im=reframe(im,1920,1080,fill="black")
        draw = ImageDraw.Draw(im)
        draw.text((400, 200),barc,(255,255,255),font=font)
        draw.text((400, 300),str(barcDate[barc]),(255,255,255),font=font)
        im.save(os.path.join(dirname,pfmt+"_Frame{:06d}.jpg".format(i)))

if __name__ == '__main__':
    main()
        
        
