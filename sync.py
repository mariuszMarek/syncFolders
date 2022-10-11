from os import listdir
from pathvalidate.argparse import validate_filepath_arg
from threading import Thread

import hashlib, shutil, argparse, time, pathlib, glob
import keyboard, pynput, sys, os

is_quit      = False
quit_char    = 'b'
KeyComb_Quit = [
    {pynput.keyboard.Key.ctrl, pynput.keyboard.KeyCode(char=quit_char)},
    {pynput.keyboard.Key.ctrl_l, pynput.keyboard.KeyCode(char=quit_char)},
    {pynput.keyboard.Key.ctrl_r, pynput.keyboard.KeyCode(char=quit_char)}
]
def on_press(key):
    global is_quit
    if any([key in comb for comb in KeyComb_Quit]):
        current.add(key)
        if any(all(k in current for k in comb) for comb in KeyComb_Quit):
            is_quit = True

def on_release(key):
    try:
        current.remove(key)
    except KeyError:
        pass
current = set()
listener = pynput.keyboard.Listener(on_press=on_press, on_release=on_release)
listener.start()


class SaveLog:
    def __init__(self, logLocation):
        self.logLocation = logLocation
        pass
    async def parseData(self, logContent):
        # make some CSV structure + some translations?
        self.saveToFile()
        pass
    async def saveToFile(self):
        pass
class SyncFolders(SaveLog, Thread):
    def __init__(self, Instructions, saveLogLocation):
        Thread.__init__(self)
        self.sourceFilePath = Instructions[0]
        self.destinFilePath = Instructions[1]
        self.TimeInterval   = Instructions[2] # * 30
        self.mapOfSouFiles  = {}
        self.mapOfDesFiles  = {}
        self.diffMap        = {}
        
        super().__init__(saveLogLocation)
    def run(self):
        self._runSync()
    def _runSync(self):
        global is_quit
        while True:
                self._scanFolder()
                self._diff()
                self._operationOfFolders()                
                time.sleep(self.TimeInterval)
                if is_quit: break 
    def _extractMetaAndScan(self,scanRoot, folderMapped):
        searchString =  os.path.join(scanRoot, "**", "**")
        for files in glob.iglob(searchString, recursive=True):            
            if files == os.path.join(scanRoot, "") : continue
            fileLoc   = files
            meta      = os.stat(files)
            modTime   = meta.st_mtime
            fileSize  = meta.st_size
            fileLoc   = fileLoc.replace(scanRoot, "")

            # print(f"{files} == {fileLoc}")

            hashMD5   = hashlib.md5( (fileLoc + str(modTime) + str(fileSize)).encode('utf-8') ).hexdigest()
            # hashMD5   = (fileLoc + ":" + str(modTime) + str(fileSize)).encode('utf-8') 
            # print(f"fileLoc -> {fileLoc}")
            folderMapped[hashMD5] = fileLoc
    def _scanFolder(self):        
        self._extractMetaAndScan(self.sourceFilePath, self.mapOfSouFiles)        
        self._extractMetaAndScan(self.destinFilePath, self.mapOfDesFiles)
    def _createNewDiffDict(self,DictA,DictB):
        return dict( sorted( {hashKey: dictValue for hashKey, dictValue in DictA.items() if hashKey not in DictB}.items(), key=operator.itemgetter(1), reverse=True))
    def _diff(self):        
        self.diffMap['Copy'] = self._createNewDiffDict(self.mapOfSouFiles, self.mapOfDesFiles)
        self.diffMap['Del'] = self._createNewDiffDict(self.mapOfDesFiles, self.mapOfSouFiles)
        print(self.diffMap)
    def _operationOfFolders(self):
        for instructions, listOfFilesDict in self.diffMap.items():
            for hashKeys, items in listOfFilesDict.items():
                sourceFile = os.path.join(self.sourceFilePath, items)
                destFile   = os.path.join(self.destinFilePath, items)
                if(instructions == "Copy") : 
                    # os.makedirs(os.path.dirname(destFile), exist_ok=True)
                    # shutil.copy2(sourceFile, destFile)                
                    pass
                if(instructions == "Del") :
                    #check if it's folder
                    if(os.path.isfile(destFile)):
                        try:
                            #try to delete empty file
                            # os.rmdir(destFile)
                            pass
                        except:
                            pass
                            #folder not empty do nothing                        
                    else :
            #zmienic sortowanie by katalogi byly ostatnie
        


def main():
    parser = argparse.ArgumentParser(description='Async sync folders based on in parameters', prog="Sync folders",
        epilog="""You can pass multiple instance of the parameters exept the -l/--logPath to handle multiple folders, 
                parameters are grouped by order of input parameter in groups of 3 (source, dest, intercal) and the number of those "sets" needs to be even
                maximum of folders per process is around 500""")

    parser.add_argument('-s', '--source',   action='append', help="source folder path",          type=validate_filepath_arg, required=True)
    parser.add_argument('-r', '--replica',  action='append', help="replica folder path",         type=validate_filepath_arg, required=True)
    parser.add_argument('-i', '--interval', action='append', help="source folder interval scan", type=int,                   required=True)
    parser.add_argument('-l', '--logPath',  action='store',  help="folder for logs",             type=validate_filepath_arg, required=True)
    
        
    inputArgs   = parser.parse_args()
    validateSets(vars(inputArgs))

    logLocation = inputArgs.logPath
    synSet      = {}

    for index, sourceFilePath in enumerate(inputArgs.source):
        synSet[sourceFilePath + inputArgs.replica[index]] = [sourceFilePath, inputArgs.replica[index], inputArgs.interval[index]]
    
    for job, jobParams in synSet.items():        
        folderSync = SyncFolders(jobParams,logLocation)
        folderSync.run()


def validateSets(inputArgs):        
    elementNames = {}    
    for argName, argValues in inputArgs.items():
        if type(argValues) is list:
            elementNames[argName] = len(argValues)    
    if(sum(elementNames.values()) % 3 != 0 and sum(elementNames.values()) > 3): raise Exception("Sorry, number or sets of arguments is not even")

if __name__ == "__main__":
    main()

