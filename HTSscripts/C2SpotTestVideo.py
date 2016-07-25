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
    parser=argparse.ArgumentParser(description="Get all .JPGs in a 'spot test' directory and patch all together as a video.")
    parser.add_argument("dir", type=str, nargs="+", help="Directory in which to search (recursively) for spot test images.")
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

def findJPEGs(rootdir):
    flist=[]
    for dirname, dirnames, filenames in os.walk(rootdir):
        for filename in filenames:
            if filename[-4:] in ('.jpg','.JPG'):
                flist.append(os.path.join(dirname, filename))
    return(flist)

def main():
    sys.argv=['test', "Y:\\Marta\\Marta\\Spot tests\\"]
    args=parseArgs()
    searchDirs=args.dir
    # Should execute this script from LOGS3 directory
    rootDir=os.getcwd()

    imLists=[findJPEGs(directory) for directory in searchDirs]
    flist=[item for sublist in imLists for item in sublist]
    
    dirname="pdump_spots_4K"
    if os.name=="posix":
        font = ImageFont.truetype("/usr/share/fonts/truetype/msttcorefonts/arial.ttf", 80)
    else:
        font = ImageFont.truetype("arial.ttf", 80)
    if os.path.exists(dirname):
        shutil.rmtree(dirname)
    os.mkdir(dirname)
    flist=sorted(flist)
    for i,im in enumerate(flist):
        im=Image.open(im)
        im=reframe(im,3840,2160,fill="black")
        draw = ImageDraw.Draw(im)
        #draw.text((400, 200),barc,(255,255,255),font=font)
        #draw.text((400, 300),str(barcDate[barc]),(255,255,255),font=font)
        im.save(os.path.join(dirname,"Frame{:06d}.jpg".format(i)))

if __name__ == '__main__':
    main()

        
        
