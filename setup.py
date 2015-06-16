from setuptools import setup, find_packages
setup(name='HTSauto',
      version='1.0.2',
      packages=['HTSscripts'],
      description='Helper functions for handling QFA data',
      long_description=open('README.txt').read(),
      entry_points={"console_scripts":["C2Find = HTSscripts.C2Find:main",
                                       "C2Merge = HTSscripts.C2Merge:main",
                                       "ArchiveImager = HTSscripts.ArchiveImager:main",
                                       "ArchiveServer = HTSscripts.ArchiveServer:main"]},
      author='Conor Lawless',
      author_email='conor.lawless@ncl.ac.uk',
      url='http://research.ncl.ac.uk/colonyzer/',
      classifiers=[
        'Development Status :: 3 - Alpha',
        'Topic :: Scientific/Engineering :: Image Recognition',
        'Intended Audience :: Science/Research'
        ]
      )
