#!/bin/env python2.7

import zipfile
import io
import shutil

def main():
    zip_file = '../../data/zips/venvbin.zip'
    with io.FileIO(zip_file,'r') as fd, io.BytesIO(fd.read()) as bd, zipfile.ZipFile(bd) as zd:
        for info in zd.infolist():
            print info.filename, info.file_size

if __name__ == "__main__":
    main()
