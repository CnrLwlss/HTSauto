import os,sys, shutil, time

def getfiles(fullpath):
    return os.listdir(fullpath)

def getfolders(fullpath):
    allfiles=getfiles(fullpath)
    allfolders=[]
    for f in allfiles:
        if "." not in f:
            allfolders.append(f)
    return allfolders

def getJPG(fullpath):
    allfiles=getfiles(fullpath)
    allJPG=[]
    for f in allfiles:
        if f[-4:]==".JPG" or f[-4:]==".jpg":
            allJPG.append(f[0:-4])
    return allJPG

def getDAT(fullpath):
    allfiles=getfiles(fullpath)
    allDAT=[]
    for f in allfiles:
        if f[-7:]=="OUT.dat":
            allDAT.append(f[0:-7])
        elif f[-4:]==".dat":
            allDAT.append(f[0:-4])
    return allDAT

def getDate(fname):
    dt=fname.split("_")[-2]
    year=dt.split("-")[0]
    month=dt.split("-")[1]
    return([year,month])

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        return False
		
def main():
	syspath = os.path.dirname(sys.argv[0])
	fullpath = os.getcwd()
	today=time.gmtime()
	fltoday=float(today.tm_year)+(float(today.tm_mon)-1.0)/12
		
	# Get name of all unarchived JPGs in main directory
	JPGs=getJPG(fullpath)

	# Get all the .dat names in the Output_Data directory
	datdirect=os.path.join(fullpath,"Output_Data")
	predirect=os.path.join(fullpath,"Output_Images")
	if (os.path.exists(datdirect)):
		DATs=getDAT(datdirect)
	else:
		print(datdirect)
		print("Output_Data directory does not exist!")
		sys.exit(0)

	# Find years and months of images
	YearMonths={}
	for JPG in JPGs:
		ym=getDate(JPG)
		# Check if date is valid (if filename is parseable)
		if len(ym[0])==4 and len(ym[1])==2 and is_number(ym[0]) and is_number(ym[1]):
			if ym[0] not in YearMonths:
				YearMonths[ym[0]]=[ym[1]]
			if ym[1] not in YearMonths[ym[0]]:
				YearMonths[ym[0]].append(ym[1])

	# For every year month in list above, generate directory if missing
	for year in YearMonths:
		if not os.path.exists(os.path.join(fullpath,"Year_"+year)):
			os.mkdir(os.path.join(fullpath,"Year_"+year))
			for month in YearMonths[year]:
				if not os.path.exists(os.path.join(fullpath,"Year_"+year,"Month_"+month)):
					os.mkdir(os.path.join(fullpath,"Year_"+year,"Month_"+month))
					os.mkdir(os.path.join(fullpath,"Year_"+year,"Month_"+month,"Output_Data"))
					os.mkdir(os.path.join(fullpath,"Year_"+year,"Month_"+month,"Output_Images"))
					shutil.copyfile(os.path.join(fullpath,"Colonyzer.py"),os.path.join(fullpath,"Year_"+year,"Month_"+month,"Colonyzer.py"))
					shutil.copyfile(os.path.join(fullpath,"Colonyzer.txt"),os.path.join(fullpath,"Year_"+year,"Month_"+month,"Colonyzer.txt"))

	# Copy JPGS, DATS and previews across
	toDelete=[]
	for JPG in JPGs:
		try:
			# Check if it is too soon to archive this file
			ym=getDate(JPG)
			# Check if date is valid (if filename is parseable)
			if len(ym[0])==4 and len(ym[1])==2 and is_number(ym[0]) and is_number(ym[1]):
				fldate=float(ym[0])+(float(ym[1])-1.0)/12.0
				if fltoday-fldate>3.0/12.0:
					fname=os.path.join(datdirect,JPG+"OUT.dat")
					iname=os.path.join(fullpath,JPG+".JPG")
					pname=os.path.join(predirect,JPG+"GriddedThresh.png")
					
					ftarg=os.path.join(fullpath,"Year_"+ym[0],"Month_"+ym[1],"Output_Data",JPG+"OUT.dat")
					itarg=os.path.join(fullpath,"Year_"+ym[0],"Month_"+ym[1],JPG+".JPG")
					ptarg=os.path.join(fullpath,"Year_"+ym[0],"Month_"+ym[1],"Output_Images",JPG+"GriddedThresh.png")
					# If files have already been backed up, delete them from folder
					if os.path.exists(itarg) and os.path.exists(iname):
						os.remove(iname)
					if os.path.exists(ftarg) and os.path.exists(fname):
						os.remove(fname)
					if os.path.exists(ptarg) and os.path.exists(pname):
						os.remove(pname)
					# If files have not already been backed up and analysis complete:
					if os.path.exists(fname) and os.path.exists(iname) and os.path.exists(pname):
						shutil.copyfile(fname,ftarg)
						shutil.copyfile(iname,itarg)
						shutil.copyfile(pname,ptarg)
						toDelete.append(JPG)
					else:
						print JPG, "Missing files."
				else:
					print JPG, " too recent"
		except:
			print JPG, " failed"

	# If that's been successful, let's delete the remaining files
	for JPG in toDelete:
		fname=os.path.join(datdirect,JPG+"OUT.dat")
		iname=os.path.join(fullpath,JPG+".JPG")
		pname=os.path.join(predirect,JPG+"GriddedThresh.png")
		if os.path.exists(fname):
			os.remove(fname)
		if os.path.exists(iname):
			os.remove(iname)
		if os.path.exists(pname):
			os.remove(pname)

if __name__ == '__main__':
    main()
    
    

