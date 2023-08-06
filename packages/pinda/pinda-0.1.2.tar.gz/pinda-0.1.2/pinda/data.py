"""
data.py - the pinda database
"""
import os
import yaml
import glob
import shutil
import pinda

template = """
# A template for a file to add a new application to your local database of
# pinda-installable applications. This file is written in YAML format.
# Once complete, use 'pinda update' to update the database.
#
id: <a string made from <name>_<version> values below, e.g. gromacs_2018>
  name: <name of the application>
  version: <version of the application>
  package: <name of the underlying python package (in setup.py)>
  repository: <repository link, e.g. git+https://bitbucket.org/<user>/<repo>.git@<branch>
  description: <one-line summary of the application>
  info: |
    <Multi-line information about the application 
    and distribution.>
"""

default_database = {
            'amber_16':
            {
             'name': 'amber',
             'version': '16',
             'package': 'amberdocker',
             'repository': 'git+https://bitbucket.org/claughton/amber_docker.git@v16',
             'description': 'Amber and AmberTools version 16',
             'info': '''
Amber and AmberTools version 16

This pinda distribution provides the following commands:

    "pmemd"       : The Amber "pmemd" command
    "sander"      : the Amber/Ambertools "sander" command
    "amber-shell" : drops you into a bash shell from which all other
                    Amber/AmberTools commands are accessible (e.g. tleap).

*NB*: Because of license restrictions, you may need to build your own 
version of this distribution. Visit https://bitbucket.org/claughton/amber_docker
for more information.

For full license and usage information, please visit http://ambermd.org

'''
            },
            'amber_18':
            {
             'name': 'amber',
             'version': '18',
             'package': 'amberdocker',
             'repository': 'git+https://bitbucket.org/claughton/amber_docker.git@v18',
             'description': 'Amber and AmberTools version 18',
             'info': '''
Amber and AmberTools version 18

This pinda distribution provides the following commands:

    "pmemd"       : The Amber "pmemd" command
    "sander"      : the Amber/Ambertools "sander" command
    "amber-shell" : drops you into a bash shell from which all other
                    Amber/AmberTools commands are accessible (e.g. tleap).

*NB*: Because of license restrictions, you may need to build your own 
version of this distribution. Visit https://bitbucket.org/claughton/amber_docker
for more information.

For full license and usage information, please visit http://ambermd.org

'''

            },
            'ambertools_16':
            {
             'name': 'ambertools',
             'version': '16',
             'package': 'amberdocker',
             'repository': 'git+https://bitbucket.org/claughton/amber_docker.git@v16-tools',
             'description': 'AmberTools version 16',
             'info': '''
AmberTools version 16

This pinda distribution provides the following commands:

    "sander"      : the Amber/Ambertools "sander" command
    "amber-shell" : drops you into a bash shell from which all other
                    AmberTools commands are accessible (e.g. tleap).

For full license and usage information, please visit http://ambermd.org

'''
            },
            'ambertools_18':
            {
             'name': 'ambertools',
             'version': '18',
             'package': 'amberdocker',
             'repository': 'git+https://bitbucket.org/claughton/amber_docker.git@v18-tools',
             'description': 'AmberTools version 18',
             'info': '''
AmberTools version 18

This pinda distribution provides the following commands:

    "sander"      : the Amber/Ambertools "sander" command
    "amber-shell" : drops you into a bash shell from which all other
                    AmberTools commands are accessible (e.g. tleap).

For full license and usage information, please visit http://ambermd.org

'''
            },
            'fpocket_3.0':
            {
             'name': 'fpocket',
             'version': '3.0',
             'package': 'fpocketdocker',
             'repository': 'git+https://bitbucket.org/claughton/fpocket_docker.git',
             'description': 'FPocket version 3.0',
             'info': '''
FPocket version 3.0

This pinda distribution provides the following commands:

    fpocket:  the original pocket prediction on a single protein structure 
    mdpocket: extension of fpocket to analyse conformational ensembles of 
              proteins (MD trajectories for instance) 
    dpocket: extract pocket descriptors 
    tpocket: test your pocket scoring function

For full license and usage instructions, please visit https://github.com/Discngine/fpocket

'''
            },
            'gromacs_2018':
            {
             'name': 'gromacs',
             'version': '2018',
             'package': 'gromacsdocker',
             'repository': 'git+https://bitbucket.org/claughton/gromacs_docker.git@v2018',
             'description': 'Gromacs version 2018',
             'info': '''
Gromacs version 2018

This pinda distribution provides the following Gromacs commands:

    "gmx"        : The Gromacs "gmx" command
    "gmx-select" : A command to set the instruction set for optimal 
                   performance

For full license and usage instructions, please visit http://gromacs.org

'''
            },
            'gromacs_2018-cuda':
            {
             'name': 'gromacs',
             'package': 'gromacsdocker',
             'version': '2018-cuda',
             'repository': 'git+https://bitbucket.org/claughton/gromacs_docker.git@v2018-cuda',
             'description': 'Gromacs version 2018 with CUDA support',
             'info': '''
Gromacs version 2018 with CUDA support

This pinda distribution provides the following Gromacs commands:

    "gmx"        : The Gromacs "gmx" command
    "gmx-select" : A command to set the instruction set for optimal 
                   performance

For full license and usage instructions, please visit http://gromacs.org

'''
            },
            'obabel_2.4.1':
            {
             'name': 'obabel',
             'version': '2.4.1',
             'package': 'babeldocker',
             'repository': 'git+https://bitbucket.org/claughton/babel_docker.git',
             'description': 'Open Babel version 2.4.1',
             'info': '''
Open Babel version 2.4.1

This pinda distribution provides the following OpenBabel commands:

    "obabel"        : The OpenBabel "obabel" command

For full license and usage instructions, please visit http://openbabel.orgg

'''
            },
            'vina_1.1.2':
            {
             'name': 'vina',
             'version': '1.1.2',
             'package': 'vinadocker',
             'repository': 'git+https://bitbucket.org/claughton/vina_docker.git',
             'description': 'AutoDock Vina and selected AutoDock Tools',
             'info': '''
AutoDock Vina and selected AutoDock Tools

This pinda distribution provides the following commands from AutoDock Vina
and AutoDock tools:

    "vina" : The "vina" command from AutoDock Vina 1.1.2
    "adt"  : An interface to selected Python tools from AutoDock Tools
             version 4.2.6, including those for preparing PDBQT format
             input files for AutoDock Vina

For full license and usage instructions, please visit http://vina.scripps.edu
and http://autodock.scripps.edu

'''
            },
           }

if not os.path.exists(pinda.PINDA_CONFIGDIR):
    os.mkdir(pinda.PINDA_CONFIGDIR)

if not os.path.exists(pinda.PINDA_DEFAULT_DATABASE):
    with open(pinda.PINDA_DEFAULT_DATABASE, 'w') as f:
        yaml.dump(default_database, f, default_flow_style=False)
    database = default_database
else:
    with open(pinda.PINDA_DEFAULT_DATABASE) as f:
        database = yaml.load(f)
    for databasefile in glob.glob(pinda.PINDA_CONFIGDIR + '/*.y*ml'):
        if databasefile != pinda.PINDA_DEFAULT_DATABASE:
            with open(databasefile,'r') as f:
                d = yaml.load(f)
                for k in d:
                    database[k] = d[k]

def update_from(yaml_file, overwrite=False):
    """
    Update or add an entry to the database.
    """
    with open(yaml_file) as f:
        try:
            new_packages = yaml.load(f)
        except:
            raise TypeError('Error: cannot parse {} - check format'.format(yaml_file))
    for package in new_packages:
        for k in ['name', 'version', 'package', 'repository', 
              'description', 'info']:
            if not k in new_packages[package]:
                raise KeyError('Error in description of package {}: key {} is required'.format(package, k))

    global database
    for package in new_packages:
        if package in database and not overwrite:
            raise ValueError('Error - {name} {version} is already in the database'.format(**database[package]))
    shutil.copy(yaml_file, pinda.PINDA_CONFIGDIR)
