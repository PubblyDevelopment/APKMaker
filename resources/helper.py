import hashlib
import re
import os

def replaceAll(origStr, replacementList):
    #origStr -- STRING of shit you want to replace other shti with
    #replacementList -- [[STRING, STRING], [REPLACETHIS, WITH THIS]]

    result = origStr

    for r in replacementList:
        if r[0] in origStr:
            result = result.replace(r[0], r[1])

    return result

def replaceRegEx(regex, orig, repl):
    return re.sub(regex, orig, repl)

def captureRegEx(regex, group, string):
    m = re.search(regex, string)
    return m.group(group)

def hash_file(filename):
    h = hashlib.md5()

    with open(filename, 'rb') as file:
        chunk = 0
        while chunk != b'':
            chunk = file.read(1024)
            h.update(chunk)

    return h.hexdigest()

def isNewer(self, new, old):

    result = os.path.getmtime(new) - os.path.getmtime(old)
    if (result is 0):
       self.warnings.append("Warning: The files were created at the same exact time. Weird.")
    else:
        return (result < 0)

'''print(replaceRegEx(r"\\/.+\\/(images|audio).+(png|wav)",
                   "FARTS",
                   r"ertermap\/EpicQuest\/variable-EQ_WORLD_Tanzania-EQ_WORLD_Tanzania\/images\/P_EQ_2_tanzania_map_background.pngerte"))'''