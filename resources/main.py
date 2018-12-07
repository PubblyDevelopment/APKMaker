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

        self.engineNo = open(Path(self.root + '/resources/latest.txt'), 'r').read()
        self.initMap = str(Path(self.root + '/map/' + self.mapName))
        self.stagePath = str(Path(self.root + '/staging/' + self.mapName))
        self.units = next(os.walk(self.initMap))[1]

    '''def getFiles(self, folderName, filetype):
        for subdir, dirs, files in os.walk(self.cwd):
            for file in files:
                if file.endswith((folderName, filetype)):
                    filepath = os.path.join(subdir, file)
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

        print (self.initMap)

    def checkJSONExistsNewerEngine(self):
        #TODO Dec 12/10/18
        for u in self.units:
            filesToCheck = os.listdir(self.stagePath + "/" + u)

            unitJSON = None
            for f in filesToCheck:
                if ".json" in f and "modified" not in f:
                    unitJSON = f


            if (unitJSON):
                if self.engineNo in unitJSON:
                    self.jsonFiles[u] = self.stagePath + "/" + u + "/" + unitJSON
                else:
                    print ("Outdated JSON (" + captureRegEx("1\.1\.\d", 0, unitJSON) + ") at " + u + ". Current: " + self.engineNo)

        print(self.jsonFiles)
                #try:
                    # Save JSON so we can use it later, important!
                #    self.jsonFiles[u] = unitJSON

    def goThruFiles(self):
        # Walk through all files ending in png, wav, or JSON
        # If png or wav, calls another function that determines whether or not to add to assets
        for root, dirs, files in os.walk(self.cwd):
            for f in files:
                if f.endswith("png") or f.endswith("wav"):
                    self.checkFileExistsInShared(f,os.path.join(root, f))
                if f.endswith("json"):
                    self.jsonFiles.append(os.path.join(root, f))

    def checkFileExistsInShared(self, filename, filepath):
        h = self.getHash(filepath)
        if not h in self.checked.keys():
            self.checked[h] = filename
            shutil.copyfile(filepath, "sharedAssets/" + filename)

    def replaceFile(self, jsonLine):
        for j in self.jsonFiles:
            with fileinput.FileInput(j, inplace=True) as file:
                for line in file:
                    try:
                        whatToReplace = (captureRegEx(r"map\\/(.+\\/(images|audio).+(png|wav))",0,line))
                        #whatToReplace = "EQ_WORLD_Tanzania"
                        replaceWith = self.determineReplaceWith(line)
                        #print (line, end='')
                        print (line.replace(whatToReplace,replaceWith), end='')
                    except:
                        print(line, end='')


        # Regex grab group 1 so we don't get map/etcetc
        # Might need to rewrite later but FOR NOW...........
        origFilepath = captureRegEx(r"map\\/(.+\\/(images|audio).+(png|wav))",1,jsonLine).split(r"\/")


        # What if it can't find it in SharedAssets for some ungodly reason?
        #print (rebuiltFilepath)
        #return "sharedAssets/" + self.checked[self.getHash(rebuiltFilepath)]
        #return self.getHash()
        #return self.jsonFiles

    def determineReplaceWith(self, jsonLine):
        lookupFile = (captureRegEx(r"map\\/(.+\\/(images|audio).+(png|wav))", 1, jsonLine)).split(r"\/")
        rebuiltFilepath = ""

        # Remove Windows forward slashes. Unix FTW
        for i in range(0, len(lookupFile)):
            rebuiltFilepath += lookupFile[i]
            if i < len(lookupFile) - 1:
                rebuiltFilepath += "/"

        ## Lookup the file in checked, attach to sharedAssets
        return "sharedAssets/" + self.checked[self.getHash(rebuiltFilepath)]


    def compareHashes(self,file1,file2):
        return hash_file(file1) == hash_file(file2)

    def getHash(self, file):
        return hash_file(file)

    def getSize(self, file):
        return os.path.getsize(file)

    def compareSizes(self,file1, file2):
        return os.path.getsize(file1) , os.path.getsize(file2)

    def doTheThing(self):
        #self.copyToStagingArea()
        self.checkIfEntryPointExists()
        self.checkJSONExistsNewerEngine()
        #self.goThruFiles()
        #print ("done!")
        #jsonFile = r"someshitsomeshitmap\/EpicQuest\/variable-EQ_WORLD_Tanzania-EQ_WORLD_Tanzania\/images\/TEST.pngmoreshit"
        #print(self.replaceFile(jsonFile))


am = APKMaker("EpicQuest")
am.doTheThing()
#am.getFiles("images",".png")
#am.startChecking()

#message = hash_file("dog.png")
#print(message)