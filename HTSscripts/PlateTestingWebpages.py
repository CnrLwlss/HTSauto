import PIL, os, math
from PIL import Image
 
resizeWidth=500

#Get jpgs for which there are no corresponding pngs
allfiles=os.listdir(os.getcwd())
filelistJPG=[os.path.splitext(f)[0] for f in allfiles if f[-4:] in ['.jpg','.JPG','.jpeg','.JPEG']]
filelistPNG=[os.path.splitext(f)[0] for f in allfiles if f[-4:] in ['.png','.PNG']]
newfiles=set(filelistJPG)-set(filelistPNG)
newfilelist=[f for f in allfiles if os.path.splitext(f)[0] in newfiles]
pngfilenames=[os.path.splitext(f)[0]+".png" for f in newfilelist]

#check to see if there are any new files, if not then ignore the rest, if there
#are then resize and build a new preview file

if len(newfilelist)>0:
    im0=Image.open(newfilelist[0])
    w,h=im0.size
    neww=resizeWidth
    newh=int(round((float(neww)/float(w))*h))
    for jpg,png in zip(newfilelist,pngfilenames):
		print jpg+" -> shrinking -> "+png
        im=Image.open(jpg)
        small=im.resize((neww,newh),Image.ANTIALIAS)
        small.save(png)

# If we have already generated individual .pngs, probably better NOT to generate one big preview in this case
# Especially if we are not going to build a massive image map
Nimages=len(pngfilenames)
bigim=Image.new("RGB",(2*neww,int(math.ceil(float(Nimages)/2.0))*newh))

row,col=0,0
for imname in pngfilenames:
    im=Image.open(imname)
    bigim.paste(im,(col*neww,row*newh,(col+1)*neww,(row+1)*newh))
    print row,col
    col=col+1
    if col>1:
        col=0
        row=row+1
    bigim.save("Preview.png")

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
	HTML+='<h2>{}<h2>\n'.format(fname)
	HTML+='<a href="{}"><img src="{}></a>\n'.format(jpg,png)

HTML+='''</article>
</body>
</html>
'''
	
# Generate html
fout=open('PlateTesting.html','w')
fout.write(HTML)
fout.close()