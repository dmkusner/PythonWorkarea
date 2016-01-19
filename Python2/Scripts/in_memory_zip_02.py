#!/bin/env python2.7

# Write a class to support in-memory zips.

import zipfile
import io

class imZip(zipfile.ZipFile):
    """
    Inherit from 'zipfile.ZipFile', extending the
    __init__ method to read the filename into an
    in-memory buffer before passing it on to the
    parent class    
    """
    def __init__(self,zip_file,*args,**kwargs):
        #self.fd = io.open(zip_file,'rb',buffering=0)
        self.fd = io.FileIO(zip_file,'r')
        self.bd = io.BytesIO(self.fd.read())
        super(imZip, self).__init__(self.bd,*args,**kwargs)
        self.__dict__['closed'] = False

    # __enter__ and __exit__ turn this into a
    # contextmanager that supports the 'with' statement
    def __enter__(self):
        return self

    def __exit__(self, *errs):
        self.close()

    # __del__ is called during garbage collection.
    # Pass the request on to the close function if
    # it hasn't already been called.
    def __del__(self):
        if not self.closed:
            self.close()

    def close(self):
        self.bd.close()
        self.fd.close()
        super(imZip, self).close()
        self.__dict__['closed'] = True
# end class


def main():
    zip_file = '../../data/zips/venvbin.zip'

    with imZip(zip_file,'r') as zf:
        for info in zf.infolist():
            print info.filename, info.file_size

    exit(0)
# end def


if __name__ == "__main__":
    main()
