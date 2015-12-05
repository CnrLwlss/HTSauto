from twitter import *
import sys
import os
import datetime
import time

# Set working directory to location of this script
pathname = os.path.dirname(sys.argv[0]) 
os.chdir(os.path.abspath(pathname))

CONSUMER_KEY="pFK31kDzE73b4HtyQLliyB9Yf"
CONSUMER_SECRET="dC3Ey73pfVd7mTBIrZ9AWfiLoqz75BHxP12VVxSc7BqWZZf2rt"

MY_TWITTER_CREDS = ".twitter_credentials"
if not os.path.exists(MY_TWITTER_CREDS):
    oauth_dance("nclHTS", CONSUMER_KEY, CONSUMER_SECRET,MY_TWITTER_CREDS)

oauth_token, oauth_secret = read_token_file(MY_TWITTER_CREDS)

t = Twitter(auth=OAuth(oauth_token, oauth_secret, CONSUMER_KEY, CONSUMER_SECRET))

#t.statuses.update(status='Hello from Python!')

def checkFiles(fullpath,delta=1.0):
    '''Find files in fullpath that have been modified within delta hours of current time'''
    allfiles=[]
    nowtime=datetime.datetime.now()
    if (os.path.isfile(fullpath)):
        ftime=datetime.datetime.fromtimestamp(os.path.getmtime(fullpath))
        dt=(nowtime-ftime).total_seconds()/(60*60)
        if(dt<=delta):
            allfiles=[fullpath]
    elif os.path.isdir(fullpath):
        for filename in os.listdir(fullpath):
            fpath=os.path.join(fullpath,filename)
            imtime=datetime.datetime.fromtimestamp(os.path.getmtime(fpath))
            dt=(nowtime-imtime).total_seconds()/(60*60)
            if(dt<=delta):
                allfiles.append(fpath)
    else:
        print(fullpath+" is neither a file nor a directory...")
    return(allfiles)

def reportFile(fullpath,tag,delta=1.0):
    '''Check if a single log file has been updated'''
    fpath=checkFiles(fullpath,delta)
    if len(fpath)>0:
        print("This file has been updated:")
        print("\t"+os.path.basename(fullpath))
        message=tag+": "+os.path.basename(fullpath)+" updated in last "+str(delta)+" hrs: "+time.strftime("%H:%M:%S")
    else:
        message=""
    return(message)

def reportFiles(dirlist,tag,delta=1.0):
    '''Check if new files have been written to a directory'''
    newfiles=[item for sublist in (checkFiles(dirname,delta) for dirname in dirlist) for item in sublist]
    newfiles.sort
    if(len(newfiles)>0):
        print("I've discovered these new files:")
        for f in newfiles: print("\t"+f)
        message=tag+": "+str(len(newfiles))+" new files in past "+str(delta)+" hrs: "+time.strftime("%H:%M:%S")+", e.g.: "+os.path.basename(newfiles[-1])
    else:
        message=""
    return(message)

def checkOnce(tag,delta=4.0,toTwitter=False,watchDirs=[],watchFiles=[]):
    '''Check current status of files/directories.  Can be controlled by monitor function, or by OS scheduler.'''
    timeline=t.statuses.user_timeline()
    print("My last tweet read as follows:")
    print("\t"+timeline[0]["text"])

    if(len(watchDirs)>0):
        message=reportFiles(dirlist=watchDirs,tag=tag,delta=delta)
        print(message)
        if(toTwitter and len(message)>0): t.statuses.update(status=message[0:140])

    if(len(watchFiles)>0):
        for f in watchFiles:
            message=reportFile(f,tag=tag,delta=delta)
            if(toTwitter and len(message)>0): t.statuses.update(status=message[0:140])

def monitor(tag,update=1.0,delta=4.0,updates=float("inf"),toTwitter=False,watchDirs=[],watchFiles=[]):
    '''Python daemon which runs in background and watches over specified files/directories'''
    i=0
    while(i<updates):
        checkOnce(tag,delta,toTwitter,watchDirs,watchFiles)
        time.sleep(update*60*60)
        i=i+1
        
if __name__ == '__main__':
    checkOnce("Cytmt",delta=4,toTwitter=True,watchDirs=["C:/IMAGES_TO_BACKUP","C:/IMAGES_TO_BACKUP_96","C:/IMAGES_TO_BACKUP_768","C:/IMAGES_TO_BACKUP_1536","C:/PeterImages"])
    #checkOnce("CONORtest",delta=4,toTwitter=True,watchDirs=[os.getcwd()])
    #monitor("CONORtest",update=0.001,delta=4,toTwitter=False,watchDirs=[os.getcwd()])
    #monitor("Cytmt",update=1,delta=4,toTwitter=True,watchDirs=["C:/IMAGES_TO_BACKUP","C:/IMAGES_TO_BACKUP_96","C:/IMAGES_TO_BACKUP_768","C:/IMAGES_TO_BACKUP_1536","C:/PeterImages"])
    #monitor("Wrmrm",update=1,delta=4,toTwitter=True,watchDirs=[])
    #monitor("Bckmn",update=1,delta=4,toTwitter=True,watchDirs=["C:\Documents and Settings\All Users\Documents\Biomek\Logs"])
    #monitor("SPBM3",update=1,delta=4,toTwitter=True,watchDirs=[],watchFiles=["C:\User\RoboSoftPro V1.1.5\Log\err.log"])
    

        
