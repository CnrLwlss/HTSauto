# HTSauto
Python module containing helper scripts & functions for handling files for Newcastle University's high-throughput service.  

## Installing or updating module

If you have not already done so, first, clone the HTSauto repository from GitHub:

```Shell
git clone https://github.com/CnrLwlss/HTSauto.git
```

The above command will create a new directory: HTSauto.  Navigate into the newly created HTSauto directory:

```Shell
cd HTSauto
```

To update an existing copy of the HTSauto repository, execute the following from inside HTSauto directory:

```Shell
git pull
```

Whether installing for the first time, or updating a previous installation:

```Shell
python setup.py install
```

Once python module is installed, the programs listed below should be available as comman-line tools, without directly invoking python.

## Available programs
All of these programs should be executed from [LOGS3](https://github.com/lwlss/LOGS3_scripts#archiving-experimental-metadata-and-qfa-results) directory.  Many of them have a small help facility.  To access help, at the command line, input the name of the program followed by "-h".  For example:

```Shell
C2Find -h
```

###C2Find
Finds paths to images from plates stored in the HTS [image archive](https://github.com/lwlss/LOGS3_scripts#archiving-raw-data-plate-images).  Paths returned correspond to images from a specific exptID (e.g. QFA0001) with a specific combination of plate agar medium (e.g. CSM) and treatment applied to plate (e.g. 27C), captured before a cutoff number of days since inoculation, .  Dumps relevant file paths to .json file.  Optionally copies symlinks to files to ../pdump directory.

###C2GetBarc
Finds all images in the HTS [image archive](https://github.com/lwlss/LOGS3_scripts#archiving-raw-data-plate-images) corresponding to a given imager barcode (e.g. K000352_027_004) and writes symlinks/shortcuts to those images at ../pdump.  Useful for debugging problems with individual plates from the archive.

###C2MidVid	
Get representative image of each plate in archive, sort by date, draw barcode on image and save (small) frame preview.  Useful for quick, visual scan through data looking for qualitative changes over time.

###C2Merge
Gathers completed imagelog files for a QFA experiment, concatenates them and writes files to appropriate IMAGELOGS directory.  Should be executed from LOGS3 directory.  Requires C2.json file (i.e. run C2Find before running C2Merge).

###C2MergeOutput
Gathers completed imagelog files for a QFA experiment, concatenates them and writes files to current directory.  Should be executed from a directory containing images which have been analysed by colonyzer2.

###ArchiveImager
Archives barcoded images in a directory on a HTF imager computer (moves older images into subdirectories labelled by year and month).  Usefully to avoid slow generation of directory listings.

###ArchiveServer
Archives barcoded images in a directory on main archive server: cisbanraid1 (moves older images into subdirectories labelled by year and month).  Usefully to avoid slow generation of directory listings.

