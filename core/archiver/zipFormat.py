# !/bin/python
# file : zipFormat.py

import os
import sys
import shutil
import zipfile
import time

FILE_NAME_SEPARATOR = "_"
ZIP_EXT = ".zip"
DEBUG = 0


def zip(source, dest):
    """Compresses a file/dir, given a source path, to the zip format
        The resulting file will be created in the given dest path. """

    dest_directory = os.path.dirname(dest)

    if not os.path.exists(dest_directory):
        print("Created zip destination folder. %s" % dest_directory)
        os.makedirs(dest_directory)

    if os.path.exists(source):
        epoch_time = str(int(time.time()))
        # moved the creation of the zip file inside each case below in order to create the zip only if necessary.

        if os.path.isfile(source):

            printDebugInfo(" inside zip, the source is a file ")

            zOut = zipfile.ZipFile(dest + FILE_NAME_SEPARATOR + epoch_time + ZIP_EXT, mode='w')
            zOut.write(source, compress_type=zipfile.ZIP_DEFLATED, arcname=os.path.basename(
                source))  # This fixes the bug where the compressed file in the zip did not have the correct file extension
            zOut.close()
            print ("   Compressed: %s into %s" % (source, dest))
        elif os.path.isdir(source):
            printDebugInfo(" inside zip, the source is a directory ")

            with zipfile.ZipFile(dest + FILE_NAME_SEPARATOR + str(epoch_time) + ZIP_EXT, mode='w') as myzip:
                rootlen = len(source)  # use the sub-part of path which you want to keep in your zip file
                for base, dirs, files in os.walk(source):
                    for ifile in files:
                        fn = os.path.join(base, ifile)
                        myzip.write(fn, fn[rootlen:], compress_type=zipfile.ZIP_DEFLATED)

    else:
        print("File: " + source + " Doesn't exist! zip function aborted.")


def unzip_single_file(source, dest):
    if os.path.isfile(source):
        zip_ref = zipfile.ZipFile(source, 'r')
        zip_ref.extractall(dest)
        zip_ref.close()
    else:
        print("Unzip Single File function, file not found: " + source)


def unzip(source, dest):
    # TODO if a file inside a zip is the same (for example out.txt) as an already decompressed file, append data to the same file from different zip
    # this is because the same log file has been compressed several times, but each zip contains different data
    if os.path.isfile(source):
        filename, file_extension = os.path.splitext(source)
        print ("Given path is a file")

        if file_extension.lower() == ZIP_EXT:
            unzip_single_file(source, dest)
    elif os.path.isdir(source):
        print ("Given path is a directory")

        for dir, subDirs, files in os.walk(source):
            for file in files:
                filename, file_extension = os.path.splitext(file)
                if file_extension.lower() == ZIP_EXT:
                    unzip_single_file(os.path.join(dir, file), dest)
    else:
        print ("Not found: ", source)


def countFilesInDirectory(directory):
    path, dirs, files = os.walk(directory).next()
    printDebugInfo("Path: %s \n Dirs: %s \n Files: %s" % (path, dirs, files))
    filesAndDirecotriesCount = len(files) + len(dirs)
    return filesAndDirecotriesCount


def printDebugInfo(callerKey):
    # Debug info:
    if DEBUG:
        print ("------------------------------------------------------------------")
        print ("Archiver DEBUG info, %s" % callerKey)
        print ("------------------------------------------------------------------")


# TODO Used for testing.
def main():
    print("")


if __name__ == '__main__':
    main()