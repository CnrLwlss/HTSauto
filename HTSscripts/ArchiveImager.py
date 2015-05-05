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
	for year in YearMonths:        
			for month in YearMonths[str(year)]:
				if not os.path.exists(os.path.join(fullpath,"Year_"+str(year),"Month_"+str(month))):
					os.mkdir(os.path.join(fullpath,"Year_"+str(year),"Month_"+str(month)))

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
					iname=os.path.join(fullpath,JPG+".JPG")
					itarg=os.path.join(fullpath,"Year_"+ym[0],"Month_"+ym[1],JPG+".JPG")
					# If files have already been backed up, delete them from folder
					if os.path.exists(iname):
						if os.path.exists(itarg):
							os.remove(iname)
						else:
							# If files have not already been backed up:
							shutil.copyfile(iname,itarg)
							toDelete.append(JPG)
				else:
					print JPG, "too recent"
			else:
				print JPG, "filename not in archivable format"
		except:
			print JPG, "failed, possibly no room on hard-drive"

	# If that's been successful, let's delete the remaining files
	for JPG in toDelete:
		iname=os.path.join(fullpath,JPG+".JPG")
		if os.path.exists(iname):
			os.remove(iname)

if __name__ == '__main__':
    main()