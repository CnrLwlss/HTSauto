import PIL, os, math
from PIL import Image
 
resizeWidth=500

#Get jpgs for which there are no corresponding pngs
allfiles=os.listdir(os.getcwd())
filelistJPG=[f for f in allfiles if f[-4:] in ['.jpg','.JPG','.jpeg','.JPEG']]
filelistJPG=[os.path.splitext(each)[0] for each in filelistJPG]
filelistPNG=[f for f in allfiles if f[-4:] in ['.png','.PNG']]
filelistPNG=[os.path.splitext(each)[0] for each in filelistPNG]
newfiles=set(filelistJPG)-set(filelistPNG)
newfilelist=[filename + '.JPG' for filename in newfiles]

#check to see if there are any new files, if not then ignore the rest, if there
#are then resize and build a new preview file

if len(newfilelist)>0:

    im0=Image.open(newfilelist[0])
    w,h=im0.size
    neww=resizeWidth
    newh=int(round((float(neww)/float(w))*h))

    for imname in newfilelist:
        im=Image.open(imname)
        small=im.resize((neww,newh),Image.ANTIALIAS)
        small.save(imname[0:-4]+".png")
        
        print imname
         
allfiles=os.listdir(os.getcwd())
filelist=[f for f in allfiles if f[-4:] in ['.png','.PNG']]
del filelist[-1]
Nimages=len(filelist)
im0=Image.open(filelist[0])
w,h=im0.size
neww=resizeWidth
newh=int(round((float(neww)/float(w))*h))
bigim=Image.new("RGB",(2*neww,int(math.ceil(float(Nimages)/2.0))*newh))

row,col=0,0
for imname in filelist:
    im=Image.open(imname)
    bigim.paste(im,(col*neww,row*newh,(col+1)*neww,(row+1)*newh))
    print row,col
    col=col+1
    if col>1:
        col=0
        row=row+1

    bigim.save("Preview.png")
    
    htmlroot="PlateTesting"
    Scroller="High Throughput Service QFA image browser "+htmlroot
    # Start creating html files for building the image maps
    SGAString="""<html>


    <!doctype html>
    <html lang=en> 
    <head>
    <meta charset=utf-8> 
    <title>Newcastle University HTSF Plate Testing</title> 
    <meta name="desciption" content="High Throughput Screening Facility Newcastle University.">
    <link href='http://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800' rel='stylesheet' type='text/css'>
    <link rel="stylesheet" type="text/css" href="CLstyle.css">
    </head>

    <article id="main">
    <h1>High Throughput Screening Facility</h1> 
    <hr></hr>

    <a name="intro"><h2>Introduction</h2></a>

    <body>
    <img src="preview.png" alt="SGA Image data" />


    """

    # Generate html image maps
    fout=open(htmlroot+'.html','w')
    fout.write(SGAString+"</map></body></html>")
    fout.close()
