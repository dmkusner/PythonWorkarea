#!/bin/env python2.7

# Test whether reading a zip file into an in-memory buffer
# actually speeds things up or not. 
#
# The answer appears to be no for the file in question.
# However, this might vary depending on the size of the
# file, the operating environment, and the type and number
# of accesses being done. This test on my laptop showed
# some gain in accessing files, but not enough to make up
# for the cost of reading the file into memory in the first
# place.

import zipfile
import io
import shutil
import time
from functools import wraps

def timeme(func):
    @wraps(func)
    def wrapper(*args, **kw):
        startTime = int(round(time.time() * 1000))
        result = func(*args, **kw)
        endTime = int(round(time.time() * 1000))

        print(endTime - startTime,'ms')
        return result

    return wrapper
# end def


# use @profile with "kernprof -lv SCRIPTFILE"
#@profile
def func1(zip_file):
    """
    read zip from disk
    """
    with zipfile.ZipFile(zip_file) as zf:
        for info in zf.infolist():
            for _ in xrange(1,10):
                with zf.open(info,'r') as src, io.open("outfile","wb") as dst:
                    shutil.copyfileobj(src,dst)
# end def


#@timeme
def func2(zip_file):
    """
    read zip into memory
    """
    with io.FileIO(zip_file,'r') as fd, io.BytesIO(fd.read()) as bd, zipfile.ZipFile(bd) as zd:
        for info in zd.infolist():
            for _ in xrange(1,10):
                with zd.open(info,'r') as src, io.open("outfile","wb") as dst:
                    shutil.copyfileobj(src,dst)
# end def


def main():
    zip_file = '../../data/zips/venvbin.zip'
    func1(zip_file)
    func2(zip_file)

if __name__ == "__main__":
    main()
