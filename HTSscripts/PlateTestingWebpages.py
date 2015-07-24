import PIL, os, math
from PIL import Image
import pandas
import numpy

def createPlateImage(outfile,density="Intensity"):
    '''Read in file describing ideal plate and generate image.  outfile should be tab-delimited file containing Row, Column and density (e.g. Intensity by default) columns'''
    ideal=pandas.read_csv(outfile,sep="\t")
    Nrow=max(ideal.Row)
    Ncol=max(ideal.Column)
    arr=numpy.zeros((Nrow,Ncol),dtype=numpy.float)
    dmax=max(ideal[density])
    dmin=min(ideal[density])
    ideal["DENS"]=ideal[density]-dmin
    ideal["DENS"]=ideal["DENS"]/(dmax-dmin)
    arr[ideal.Row-1,ideal.Column-1]=ideal.DENS
    rgbarr=numpy.zeros((Nrow,Ncol,3),dtype=numpy.uint8)
    rgbarr[...,0]=numpy.round(arr*256)
    rgbarr[...,1]=numpy.round(arr*256)
    rgbarr[...,2]=numpy.round(arr*256)
    idealim=Image.fromarray(rgbarr,"RGB")
    return(idealim)
 
resizeWidth=500
buildPreview=False

#Get jpgs for which there are no corresponding pngs
allfiles=os.listdir(os.getcwd())
filelistJPG=[os.path.splitext(f)[0] for f in allfiles if f[-4:] in ['.jpg','.JPG','.jpeg','.JPEG']]
filelistPNG=[os.path.splitext(f)[0] for f in allfiles if f[-4:] in ['.png','.PNG']]
newfiles=set(filelistJPG)-set(filelistPNG)
newfilelist=[f for f in allfiles if os.path.splitext(f)[0] in newfiles]
pngfilenames=[os.path.splitext(f)[0]+".png" for f in newfilelist]

#check to see if there are any new files, if not then ignore the rest, if there
#are then resize and build a new preview file
maxh=0
if len(newfilelist)>0:
    for jpg,png in zip(newfilelist,pngfilenames):
        im=Image.open(jpg)
        w,h=im.size
        newh=int(round((float(resizeWidth)/float(w))*h))
        if newh>maxh:
            maxh=newh
        print jpg+" -> shrinking -> "+png
        small=im.resize((resizeWidth,newh),Image.ANTIALIAS)
        small.save(png)

# If we have already generated individual .pngs, probably better NOT to generate one big preview in this case
# Especially if we are not going to build a massive image map
if buildPreview:
    Nimages=len(pngfilenames)
    bigim=Image.new("RGB",(2*resizeWidth,int(math.ceil(float(Nimages)/2.0))*maxh))

    row,col=0,0
    for imname in pngfilenames:
        im=Image.open(imname)
        bigim.paste(im,(col*resizeWidth,row*maxh,(col+1)*resizeWidth,(row+1)*maxh))
        print row,col
        col=col+1
        if col>1:
            col=0
            row=row+1
        bigim.save("Preview.png")

if maxh>0:
    idealim=createPlateImage("IdealPlate.out")
    idealim=idealim.resize((resizeWidth,maxh),Image.NEAREST)
    idealim.save("Ideal.PNG")

# Start creating html files for building the image maps
HTML='''<html>

<!doctype html>
<html lang=en> 
<head>
<meta charset=utf-8> 
<title>Newcastle University HTSF Plate Testing</title> 
<meta name="desciption" content="High Throughput Screening Facility Newcastle University.">
<link href='http://fonts.googleapis.com/css?family=Open+Sans:300italic,400italic,600italic,700italic,800italic,400,300,600,700,800' rel='stylesheet' type='text/css'>
<link rel="stylesheet" type="text/css" href="CLstyle.css">
</head>

<body>
<article id="main">
<h1>High Throughput Screening Facility</h1> 
'''

for jpg,png in zip(newfilelist,pngfilenames):
	fname=os.path.splitext(png)[0]
	batchno=fname[1:7]
	datetime=fname[-19:]
	HTML+='<h2>{}<h2>\n'.format("Batch: "+batchno+" Date: "+datetime)
	HTML+='<a href="{}"><img src="{}"></a>\n'.format(jpg,png)
	HTML+='<a href="Ideal.png"><img src="Ideal.png"></a>\n'

HTML+='''</article>
</body>
</html>
'''
	
# Generate html
fout=open('PlateTesting.html','w')
fout.write(HTML)
fout.close()
