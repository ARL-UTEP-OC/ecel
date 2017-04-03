# !/bin/python
# file : tarFormat.py

import os
import sys
import time
import shutil
import tarfile

SEPARATOR = "_"
EXT = ".tar.bz2" # Alternate extension form is .tbz2

def tar(source, dest):
    """Compresses a file/dir, given a source path, using tar archiving
        with bzip2 compression. The resulting file will be created in
        the given dest path. """

    if os.path.exists(source):
        if os.listdir(source):  # Compress files, not an empty directory
            epochTime = str(int(time.time()))

            with tarfile.open(dest + SEPARATOR + epochTime + EXT, "w:bz2") as tarBall:
                tarBall.add(source, arcname=os.path.basename(source))
                tarBall.close()
    else:
        print("   File: " + source + " Doesn't exist! tar function aborted.")

# Decompresses all files from the source directory into the dest directory
# - Can decompress and preserve the folder structure
# - Only decompresses tar bzip2 files.
def untar(source, dest):
    if os.path.exists(source):
        for elem in os.listdir(source):
            elemPath = os.path.join(source, elem)

            if os.path.splitext(elemPath)[-1].lower() == EXT: # Omission raises error
                tarBall = tarfile.open(elemPath, "r:bz2")
                for tarElem in tarBall:

                    if tarElem.isreg():
                        tarBall.extractall(path=dest)

                print ("   Decompressed into: %s" % dest)
                tarBall.close()
    else:
        print ("   Path does not exist: %s" %source)


# Removes the contents inside a directory, but not the directory itself.
def delDirContents(dir):
    for aFile in os.listdir(dir):
        path = os.path.join(dir, aFile)
        try:
            if os.path.isfile(path):
                os.unlink(path)
            elif os.path.isdir(path):
                shutil.rmtree(path, ignore_errors=True)
        except Exception as e:
            print (e)

# TODO Used for testing.
def main(args):
    print("")

if __name__ == '__main__':
    main(sys.argv)