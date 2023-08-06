#!/usr/bin/env python

import setuptools
#import sys

def readme():
    with open('TITLE.txt') as f:
         return f.readline().rstrip('\n')

def longDescription():
    with open('README.rst') as f:
         return f.read()


#from setuphelpers import get_version, require_python
#from setuptools import setup


#__version__ = get_version('unisos/icm/__init__.py')
__version__ = '0.27'


requires = [
    'flufl.bounce==2.3',
    'unisos.icm',
    'unisos.common',
    'unisos.x822Msg',
    'bisos.currents',
]

#print('Setting up under python version %s' % sys.version)
#print('Requirements: %s' % ','.join(requires))

scripts = [
    "bin/pkgMarmeManage.py",
    "bin/inMailNotmuch.py",
    "bin/marmeAcctsManage.py",
    "bin/marmeSendIcm.py",
    "bin/inMailDsnProc.py",
    "bin/bx822-qmail-remote.py",
    "bin/inMailRetrieve.py",
    "bin/marmeRuns.py",
    "bin/marmeTrackingIcm.py",
    "bin/fbxoMarmeSetup.sh",
    "bin/marmeSendExample.py",
    "bin/inMailDsnPlugin.py",
    "bin/marmeMsgLib.py",
    "bin/dsnMsgPlugin.py",
]

#
# Data files are specified in ./MANIFEST.in as:
# recursive-include unisos/marme-base *
# recursive-include unisos/marme-config *
#
    
data_files = [
]

setuptools.setup(
    name='unisos.marme',
    version=__version__,
    namespace_packages=['unisos'],
    packages=setuptools.find_packages(),
    scripts=scripts,
    #data_files=data_files,
    # data_files=[
    #     ('pkgInfo', ["unisos/pkgInfo/fp/icmsPkgName/value"]),
    # ],
    #package_dir={'unisos.marme': 'unisos'},
    # package_data={
    #     'unisos.marme': ['pkgInfo/fp/icmsPkgName/value'],
    # },
    # package_data={
    #     '': ['unisos/marme/resolv.conf'],
    # },
    include_package_data=True,
    zip_safe=False,
    author='Mohsen Banan',
    author_email='libre@mohsen.1.banan.byname.net',
    maintainer='Mohsen Banan',
    maintainer_email='libre@mohsen.1.banan.byname.net',
    url='http://www.by-star.net/PLPC/180047',
    license='AGPL',
    description=readme(),
    long_description=longDescription(),
    download_url='http://www.by-star.net/PLPC/180047',
    install_requires=requires,
    classifiers=[
        'Development Status :: 5 - Production/Stable',
        'Intended Audience :: Developers',
        'License :: OSI Approved :: GNU Affero General Public License v3',
        'Operating System :: POSIX',
        'Programming Language :: Python',
        'Topic :: Software Development :: Libraries',
        'Topic :: Software Development :: Libraries :: Python Modules',
        ]
    )

