import hashlib
import re
import os

def captureRegEx(regex, group, string):
    m = re.search(regex, string)
    return m.group(group)

def replaceFile(line):


    whatToReplace = (captureRegEx(r'(relPath.*)": "(map\\/(.+\\/(.*)(png|wav|mp4|jpg|jpeg)?))',
                                                      2,
                                                      line))



    print (whatToReplace)

def determineReplaceWith(jsonLine):
    extToCheck = ['.ogg', '.mp3', '.wav']


    lookupFile = (captureRegEx(,
                               3,
                               jsonLine)).split(r"\/")

    hasFileExt = 'NoExt' not in (captureRegEx(r'(relPath.*)": "(map\\/(.+\\/(.*)(png|wav|mp4|jpg|jpeg)?))',
                                              1,
                                              jsonLine))

    rebuiltFilepath = "replacewithstagepath" + "/"

    # Remove Windows forward slashes. Unix FTW
    for i in range(1, len(lookupFile)):
        rebuiltFilepath += lookupFile[i]
        if i < len(lookupFile) - 1:
            rebuiltFilepath += "/"

    print ("poop")

    if (hasFileExt):
        print ("farts")
        #return "sharedAssets/" + self.checked[self.getHash(rebuiltFilepath)]
    else:
        for ext in extToCheck:
            #if os.path.isfile(rebuiltFilepath + ext):
            print (rebuiltFilepath + ext)


#replaceFile(r'relPath": "map\/EpicQuest\/unit-EpicQuest-Books-Books-EQ_B1_Petros\/images\/P_Petros_01_cover.jpeg')
#replaceFile(r'relPathNoExt": "map\/EpicQuest\/unit-EpicQuest-Books-Books-EQ_B1_Petros\/audio\/P_SW_Books_petros_cover_page_W01_petros')
determineReplaceWith(r'relPathNoExt": "map\/EpicQuest\/unit-EpicQuest-Books-Books-EQ_B1_Petros\/audio\/P_SW_Books_petros_cover_page_W01_petros')