from os import listdir
from pathvalidate.argparse import validate_filepath_arg

import hashlib
import shutil
import argparse
import time
import asyncio
import pathlib

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
class SyncFolders(SaveLog):
    def __init__(self, Instructions):
        self.sourceFilePath = Instructions[0]
        self.destinFilePath = Instructions[1]
        self.TimeInterval   = Instructions[2]
        # sourceFilePath, inputArgs.replica[index], inputArgs.interval[index]
        super().__init__(logLocation, logContent)
        pass
    async def runSync(self):
        while True:
            scanFolderTask = asyncio.create_task(coro=self.scanFolder())
            await scanFolderTask

            diffTask = asyncio.create_task(coro=self.diff())
            await diffTask
            
            operationTask = asyncio.create_task(coro=self.operationOfFolders())
            await operationTask

            await asyncio.sleep(self.TimeInterval) # wait before next scaning of folder
    async def scanFolder(self):
        #scan the folders and list the files and run the diff command
        # add md5 hash to all of the files
        diffTask = asyncio.create_task(coro=self.diff())
        await diffTask                
        pass
    async def diff(self):
        #create a new list 
        pass    
    async def operationOfFolders(self):
        pass



parser = argparse.ArgumentParser(description='Async sync folders based on in parameters', prog="Sync folders",
    epilog="""You can pass multiple instance of the parameters exept the -l/--logPath to handle multiple folders, 
              parameters are grouped by order of input parameter in groups of 3 (source, dest, intercal) and the number of those "sets" needs to be even""")

parser.add_argument('-s', '--source',   action='append', help="source folder path",          type=validate_filepath_arg, required=True)
parser.add_argument('-r', '--replica',  action='append', help="replica folder path",         type=validate_filepath_arg, required=True)
parser.add_argument('-i', '--interval', action='append', help="source folder interval scan", type=int,          required=True)
parser.add_argument('-l', '--logPath',  action='store',  help="folder for logs",             type=validate_filepath_arg, required=True)

def validateSets(inputArgs):        
    elementNames = {}    
    for argName, argValues in inputArgs.items():
        if type(argValues) is list:
            elementNames[argName] = len(argValues)    
    if(sum(elementNames.values()) % 3 != 0 and sum(elementNames.values()) > 3): raise Exception("Sorry, number or sets of arguments is not even")

inputArgs   = parser.parse_args()
validateSets(vars(inputArgs))

logLocation = inputArgs.logPath
synSet      = {}

for index, sourceFilePath in enumerate(inputArgs.source):
    synSet[sourceFilePath + inputArgs.replica[index]] = [sourceFilePath, inputArgs.replica[index], inputArgs.interval[index]]


asyncLoop = asyncio.get_event_loop()
asyncTasks = []
for job, jobParams in synSet.items():
    folderSync = SyncFolders(jobParams)
    asyncTasks.append(asyncLoop.create_task(folderSync.runSync()))
asyncLoop.run_forever()
