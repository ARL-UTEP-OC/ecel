from threading import Timer, Thread, Event
import os
import sys
import time
import shutil
from tarFormat import tar, untar
from zipFormat import zip, unzip

__all__ = ['Archive']
DEST_DIR = "compressed"
DEBUG = False

SIZE_REACHED = "Archived reason: SIZE reached"
TIME_REACHED = "Archived reason: TIME reached"

class Archive():
    """ Archiver is a dynamic class that allows each plugin to have their own settings for:
        - fileFormat: 'zip' and 'tar' (tar-with bzip2 compression)
        - archiverSize: data is compressed when limit is reached (in bytes).
        - sizeCheckPeriod: how often to check if the data's size has been exceeded (in seconds).
        - archiverTimeInterval: data is compressed, regardless of size, at set intervals (in seconds).
        - logSource: the path location where the data to compress is located (path location). """

    def __init__(self, plugin, arch_configs):
        self.plugin = plugin
        self.fileFormat = str(arch_configs["File Format"]["Selected"])
        self.archiverTimeInterval = int(arch_configs["Archive Time Interval"]["Value"])
        #self.archiverSize = int(arch_configs["Archive Size"]["Value"])
        #self.sizeCheckPeriod = int(arch_configs["Size Check Period"]["Value"])

        self.raw_dir = os.path.join(plugin.output_dir, '')
        self.compressed_dir = self.getDestPath()

        #Flag to execute or not
        self.executeArchiverFunction = True    #1 for true, yes

        # keep for checks in method start/stop
        self.timeIntervalArchiver = None
        self.fileSizeArchiver = None
        self.currentFileSize = 0

        # 2 Archivers (2 threads) could run if both archiverTimeInterval and sizeCheckPeriod are given.
        # If archiver time is given, it has precedence above the checkFileSize option
        if self.archiverTimeInterval > 0:
            self.timeIntervalArchiver = PerpetualTimer(self.archiverTimeInterval, self.compress)
            self.timeIntervalArchiver.start()

        #if self.archiverSize > 0 and self.sizeCheckPeriod > 0:
        #    self.fileSizeArchiver = PerpetualTimer(self.sizeCheckPeriod, self.checkFileSize)
        #    self.fileSizeArchiver.start()

    def getDestPath(self):
        # Returns the full destination path with newly appended file name without the file extension
        # e.g. "../Users/../log"
        compressDir = os.path.join(self.plugin.base_dir, DEST_DIR)
        fileName = os.path.splitext(os.path.basename(self.raw_dir))[0]
        dest_path = os.path.join(compressDir, fileName)
        rawDir = os.path.join(self.plugin.base_dir, "raw")
        parsedDir = os.path.join(self.plugin.base_dir, "parsed")

        if not os.path.exists(dest_path):
            print("  Creating archiver destination directory: %s" % dest_path)
            os.makedirs(dest_path)
        if not os.path.exists(rawDir):
            print("  Creating raw destination directory: %s" % rawDir)
            os.makedirs(rawDir)
        if not os.path.exists(parsedDir):
            print("  Creating parsed destination directory: %s" % parsedDir)
            os.makedirs(parsedDir)
        return dest_path

    def getSourceSize(self):
        if os.path.isfile(self.raw_dir):
            return os.path.getsize(self.raw_dir)
        elif os.path.isdir(self.raw_dir):
            totalSize = 0
            for dirPath, dirNames, fileNames in os.walk(self.raw_dir):
                for aFile in fileNames:
                    filePath = os.path.join(dirPath, aFile)
                    totalSize += os.path.getsize(filePath)
            return totalSize

    def checkFileSize(self):
        self.currentFileSize = self.getSourceSize()
        if self.currentFileSize >= self.archiverSize:
            print("   File size limit %i-B reached, compressing: %s" % (self.archiverSize, self.raw_dir))
            print(" Current file size: %s " % self.currentFileSize)
            self.compress()

    def compress(self):
        if self.has_data():
            if self.executeArchiverFunction == True:
                self.suspend()
                self.printDebugInfo("Compress function")

                doPluginInterrupt = self.plugin.is_live()
                if doPluginInterrupt:
                    self.plugin.terminate()

                self.append_to_metafile()

                if self.fileFormat == "zip":
                    zip(self.raw_dir, self.compressed_dir)
                elif self.fileFormat == "tar":
                    tar(self.raw_dir, self.compressed_dir)
                else:
                    print ("   Invalid file format given: %s (compression will continue with zip)" % self.fileFormat)
                    zip(self.raw_dir, self.compressed_dir)

                self.delDirContents(self.raw_dir)

                if doPluginInterrupt:
                    print(" [Archiver starting: %s]" % self.plugin.name)
                    self.plugin.run()

                self.resume()

    # TODO test decompress further
    def decompress(self):
        if self.executeArchiverFunction == True:
            self.suspend()                      # Make sure no compression is done while un-compressing
            self.plugin.stop()

            if self.fileFormat == "zip":
                unzip(self.raw_dir, self.compressed_dir)
                self.delDirContents(self.compressed_dir)
            elif self.fileFormat == "tar":
                untar(self.raw_dir, self.compressed_dir)
                self.delDirContents(self.compressed_dir)
            else:
                print ("   Could not decompress plugin: %s" % self.plugin.name)

            self.plugin.start()
            self.resume()                       # Resume Archiver compression

    def has_data(self):
        for entry in os.listdir(self.raw_dir):
            if entry != "META":
                return True
        return False

    # Removes the contents inside a directory, but not the directory itself.
    def delDirContents(self, dir):
        if os.path.exists(dir):
            for aFile in os.listdir(dir):
                path = os.path.join(dir, aFile)
                try:
                    if os.path.isfile(path):
                        os.unlink(path)
                    elif os.path.isdir(path):
                        shutil.rmtree(path, ignore_errors=True)
                except Exception as e:
                    print (e)

    def append_to_metafile(self):
        epoch_time = str(int(time.time()))
        for metadata_file_path in self.plugin.metadata_file_paths:
            try:
                with open(metadata_file_path, "a") as metafile:
                    if self.currentFileSize > self.archiverSize:
                        metafile.write("\n\nArchive Reason  = reached SIZE" + "\n")
                    else:
                        metafile.write("\n\nArchive Reason  = reached TIME" + "\n")

                    metafile.write("timestamp       = " + epoch_time + "\n")
                    metafile.write("archive time    = " + str(self.archiverTimeInterval) + "\n")
                    metafile.write("size check time = " + str(self.sizeCheckPeriod) + "\n")
                    metafile.write("size limit      = " + str(self.archiverSize)+ "\n")
                    metafile.write("probed size     = " + str(self.currentFileSize) + "\n")
                    metafile.write("file type       = " + str(self.plugin.ext) + "\n")
                    metafile.close()
                    print "finished"
            except IOError, e:
                pass

    def start(self):
        if self.timeIntervalArchiver is not None:
            self.timeIntervalArchiver.start()

        if self.fileSizeArchiver is not None:
            self.fileSizeArchiver.start()

    def stop(self):
        if self.timeIntervalArchiver is not None:
            self.timeIntervalArchiver.cancel()

        if self.fileSizeArchiver is not None:
            self.fileSizeArchiver.cancel()

    def suspend(self):
        # The threads cannot be suspended that easy, so a way to do it is to keep the timer threads running,
        # but do not execute the archiver function if it is in the suspend state
        if self.timeIntervalArchiver is not None:
            self.executeArchiverFunction = False

        if self.archiverTimeInterval is not None:
            self.executeArchiverFunction = False

    def resume(self):
        # if the archiver function is suspended, then resume it to enable execution
        if self.timeIntervalArchiver is not None:
            self.executeArchiverFunction = True

        if self.archiverTimeInterval is not None:
            self.executeArchiverFunction = True

    def printDebugInfo(self, callerKey):
        # Debug info:
        if DEBUG:
            print ("------------------------------------------------------------------")
            print ("Archiver DEBUG info, from %s"% callerKey)
            print ("    File Format: %s" % self.fileFormat)
            print ("    Archiver Size: %s" % self.archiverSize)
            print ("    Size Check Period: %s" % self.sizeCheckPeriod)
            print ("    Archiver TImer Interval: %s" % self.archiverTimeInterval)
            print ("    Log Source: %s" % self.raw_dir)
            print ("    Log Destination: %s" % self.compressed_dir)
            print ("------------------------------------------------------------------")

# TODO Source file might need to be rotated in order to compress. Then, raw duplicate data is deleted afterwards.

class PerpetualTimer:
    def __init__(self, t, hFunction):
        self.t = t
        self.hFunction = hFunction
        self.thread = Timer(self.t*60, self.handle_function)

    def handle_function(self):
        self.hFunction()
        self.thread = Timer(self.t*60, self.handle_function)
        self.thread.start()

    def start(self):
        self.thread.start()

    def cancel(self):
        self.thread.cancel()
