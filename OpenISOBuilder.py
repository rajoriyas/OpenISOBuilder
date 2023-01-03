import subprocess 

modules=str(subprocess.run('pip list', shell=True, stdout=subprocess.PIPE))
if 'pycdlib' not in modules:
    subprocess.run('pip -q install pycdlib', shell=True)
    
try:
    from cStringIO import StringIO as BytesIO
except ImportError:
    from io import BytesIO

import pycdlib, os

iso = pycdlib.PyCdlib()
iso.new(interchange_level=4)

folderPath = input('Directory Full Path: ')
for path, subdirs, files in os.walk(folderPath):
    childPath = path.replace(folderPath, '').replace('\\', '', 1).replace('\\', '/')
    if childPath != '':
        iso.add_directory('/'+childPath)
    for file in files:
        print('File: '+childPath+'/'+file)
        fileFullPath = os.path.join(path, file)
        fileHandle = open(fileFullPath, 'rb')
        fileBody = bytes(fileHandle.read())
        iso.add_fp(BytesIO(fileBody), len(fileBody), '/'+childPath+'/'+file)
        fileHandle.close()

isoPath = input('ISO Path: ')
isoName = input('ISO Name (exclude .iso extension): ')
iso.write('{}/{}.iso'.format(isoPath, isoName))
iso.close()
