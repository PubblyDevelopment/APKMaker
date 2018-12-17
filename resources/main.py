# main.py

import os
import glob
import shutil
from shutil import *
from helper import *
import fileinput
from pathlib import Path

class APKMaker:
    def __init__(self, mn):
        self.checked = {}
        self.jsonFiles = {}
        self.entryPoint = ""

        os.chdir("..")
        self.root = os.getcwd()

        self.mapName = mn

        self.resourcePath = str(Path(self.root + '/resources'))
        self.engineNo = open(Path(self.root + '/resources/latest.txt'), 'r').read()
        self.enginePath = str(Path(self.root + '/resources/engine'))
        self.initMap = str(Path(self.root + '/map/' + self.mapName))
        self.stagePath = str(Path(self.root + '/staging/' + self.mapName))
        self.units = next(os.walk(self.initMap))[1]

        self.extToCheck = ['.ogg','.mp3','.wav']
        self.regExp = r'((relPath.*)": "(map\\/(.+\\/(.*)(png|wav|ogg|mp3|mp4|jpg|jpeg)?)))"'


    '''def getFiles(self, folderName, filetype):
        for subdir, dirs, files in os.walk(self.cwd):
            for file in files:
                if file.endswith((folderName, filetype)):
                    filepath = os.path.join(subdir, file0)
                    self.unchecked[filepath] = [self.getSize(filepath),self.getHash(filepath),file]

        for k, v in self.unchecked.items():
            print (k, "", v)

    def startChecking(self):
        if (len(self.unchecked) == 0):
            print ("Something went wrong with reading files.")
            return

        # B/c python is stupid, have to make keys into a list

        while len(self.unchecked) > 0:
            keyToCheck = list(self.unchecked.keys())[0]
            curr = self.unchecked.pop(keyToCheck)
            self.checked[keyToCheck] = curr

        for k,v in self.checked.items():
            print (k,v)'''

    def checkIfEntryPointExists(self):
        try:
            self.entryPoint = open(self.initMap + "/entryPoint.txt", "r").read()
            print ("Entry point at " + self.entryPoint)
        except:
            print("Fatal: No entry point specified.")

    def copyToStagingArea(self):
        shutil.copytree(self.initMap, self.stagePath,
                        ignore=ignore_patterns("entryPoint.*", "test.py", "*.sh", "*.html", ".DS_Store"))

    def makeSharedAssetsFolder(self):
        '''try:
            os.mkdir("sharedAssets")
        except OSError:
            print("sharedAssets already exists, overwriting contents...")'''

        os.mkdir(self.stagePath + "/sharedAssets")

    def checkJSONExistsNewerEngine(self):
        #TODO Dec 12/10/18
        for u in self.units:
            filesToCheck = os.listdir(self.stagePath + "/" + u)

            unitJSON = None
            unitXML = None
            for f in filesToCheck:
                if ".json" in f and "modified" not in f:
                    unitJSON = f
                if ".xml" in f:
                    unitXML = f


            if (unitJSON):
                if self.engineNo in unitJSON:
                    self.jsonFiles[u] = self.stagePath + "/" + u + "/" + unitJSON
                else:
                    print ("Fatal: Outdated JSON (" + captureRegEx("1\.1\.\d", 0, unitJSON) + ") at " + u + ". Current: " + self.engineNo)
            else:
                print ("Fatal: JSON missing.")

            if (unitXML):
                if (unitJSON):
                    if not isNewer(self.jsonFiles[u], self.stagePath + "/" + u + "/" + unitXML):
                        print ("Fatal: XML not parsed at " + u)
            else:
                print ("Fatal: XML missing.")

                #try:
                    # Save JSON so we can use it later, important!
                #    self.jsonFiles[u] = unitJSON

    def goThruFiles(self):
        # Walk through all files ending in png or wav
        # If png or wav, calls another function that determines whether or not to add to assets
        shared = (self.stagePath)
        for root, dirs, files in os.walk(shared):
            for f in files:
                if f.endswith("png") or f.endswith("wav") or f.endswith("ogg") or f.endswith("mp4") or f.endswith("jpg") or f.endswith("jpeg") or f.endswith("mp3"):
                    self.checkFileExistsInShared(f,os.path.join(root, f))

    def checkFileExistsInShared(self, filename, filepath):
        sharedFolder = self.stagePath + "/sharedAssets/"
        h = self.getHash(filepath)
        if not h in self.checked.keys():
            self.checked[h] = filename
            shutil.copyfile(filepath, sharedFolder + filename)

    def replaceFile(self):
        for k,v in self.jsonFiles.items():
            print (v)
            with fileinput.FileInput(v, inplace=True) as file:
                for line in file:
                    #try:
                    whatToReplace = (captureRegEx(self.regExp,
                                                  3,
                                                  line))


                    if (whatToReplace != None):

                        replaceWith = self.determineReplaceWith(line)

                        print (line.replace(whatToReplace,replaceWith), end='')
                #except:
                    else:
                        print(line, end='')



    def determineReplaceWith(self, jsonLine):
        lookupFile = (captureRegEx(self.regExp,
                                   4,
                                   jsonLine)).split(r"\/")

        hasFileExt = "NoExt" not in captureRegEx(self.regExp,
                                                 2,
                                                 jsonLine)


        rebuiltFilepath = self.stagePath + "/"

        # Remove Windows forward slashes. Unix FTW
        for i in range(1, len(lookupFile)):
            rebuiltFilepath += lookupFile[i]
            if i < len(lookupFile) - 1:
                rebuiltFilepath += "/"

        if (hasFileExt):
            return "sharedAssets/" + self.checked[self.getHash(rebuiltFilepath)]
        else:
            for ext in self.extToCheck:
                if os.path.isfile(rebuiltFilepath + ext):
                    return "sharedAssets/" + self.checked[self.getHash(rebuiltFilepath + ext)]

    def runBuildHTML(self):
        for u in self.units:
            # Copy run file from correct location
            shutil.copy(self.stagePath + "/pubbly_engine/" + self.engineNo + "/app.html", self.stagePath)

            #print(self.stagePath + "/run.html")

            with open(self.jsonFiles[u], 'r') as jsonFile:
                jsonData = jsonFile.read()

            with fileinput.FileInput(self.stagePath + "/app.html", inplace="True") as file:
                for line in file:
                    print(replaceAll(
                        line, [
                            ["{REL_ROOT}", '.'],
                            ["{ENGINE}", self.engineNo],
                            ["{PUBBLY_JSON}", jsonData],
                            ["{START_PAGE}", self.stagePath + "/" + self.entryPoint + ".html"],
                        ]), end='')

            os.rename(self.stagePath + "/app.html",
                      self.stagePath + "/" + u + ".html")

    def copyEngine(self):
        shutil.copytree(self.enginePath, self.stagePath + "/pubbly_engine")

    def makeIndex(self):
        print(self.stagePath + "/" + self.entryPoint + ".html")

        shutil.copyfile(self.stagePath + "/" + self.entryPoint + ".html", self.stagePath + "/index.html")

    def compareHashes(self,file1,file2):
        return hash_file(file1) == hash_file(file2)

    def getHash(self, file):
        return hash_file(file)

    def getSize(self, file):
        return os.path.getsize(file)

    def compareSizes(self,file1, file2):
        return os.path.getsize(file1) , os.path.getsize(file2)

    def doTheThing(self):
        self.checkIfEntryPointExists()
        self.copyToStagingArea()
        self.checkJSONExistsNewerEngine()
        self.makeSharedAssetsFolder()
        self.goThruFiles()
        self.replaceFile()
        self.copyEngine()
        self.runBuildHTML()
        self.makeIndex()

        for k, v in self.checked.items():
            print (k, v)


        #print ("done!")
        #jsonFile = r"someshitsomeshitmap\/EpicQuest\/variable-EQ_WORLD_Tanzania-EQ_WORLD_Tanzania\/images\/TEST.pngmoreshit"
        #print(self.replaceFile(jsonFile))


am = APKMaker("EpicQuest")
am.doTheThing()
#am.getFiles("images",".png")
#am.startChecking()

#message = hash_file("dog.png")
#print(message)