from os import listdir
from pathvalidate.argparse import validate_filepath_arg

import hashlib
import shutil
import argparse
import time
import asyncio
import pathlib



parser = argparse.ArgumentParser(description='Async sync folders based on in parameters', prog="Sync folders",
    epilog="""You can pass multiple instance of the parameters exept the -l/--logPath to handle multiple folders, 
              parameters are grouped by order of input parameter in groups of 3 (source, dest, intercal) and the number of those "sets" needs to be even""")

parser.add_argument('-s', '--source',   action='append', help="source folder path",          type=validate_filepath_arg, required=True)
parser.add_argument('-r', '--replica',  action='append', help="replica folder path",         type=validate_filepath_arg, required=True)
parser.add_argument('-i', '--interval', action='append', help="source folder interval scan", type=int,          required=True)
parser.add_argument('-l', '--logPath',  action='store',  help="folder for logs",             type=validate_filepath_arg, required=True)

inputArgs = parser.parse_args()
# print(inputArgs.replica)

def validateSets(inputArgs):        
    elementNames = {}
    mapOfArgs = vars(inputArgs)
    for argName, argValues in mapOfArgs.items():
        if type(argValues) is list:
            elementNames[argName] = len(argValues)        
    if(sum(elementNames.values()) % 3 != 0 and sum(elementNames.values()) > 3): raise Exception("Sorry, number or sets of arguments is not even")
    else : return sum(elementNames.values()) %3



logLocation = inputArgs.logPath
totalSets   = validateSets(inputArgs)
synSet      = {}

for setNum in range (totalSets):
    pass