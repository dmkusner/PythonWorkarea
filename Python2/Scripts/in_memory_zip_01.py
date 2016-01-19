#!/bin/env python2.7

import zipfile
import io
import shutil
import os
import sys

def main():
    script_dir = os.path.abspath(os.path.dirname(sys.argv[0]))
    data_dir = os.sep.join(script_dir.split(os.sep)[:-2] + ['data', 'zips'])
    zip_file = os.path.join(data_dir,'venvbin.zip')

    with io.FileIO(zip_file,'r') as fd, io.BytesIO(fd.read()) as bd, zipfile.ZipFile(bd) as zd:
        for info in zd.infolist():
            print info.filename, info.file_size

if __name__ == "__main__":
    main()
