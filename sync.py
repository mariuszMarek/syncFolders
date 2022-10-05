from os import listdir

import shutil
import argparse
import time
import asyncio
import pathlib

parser = argparse.ArgumentParser(description='Async sync folders based on in parameters', prog="Sync folders",
    epilog="""You can pass multiple instance of the parameters exept the -l/--logPath to handle multiple folders, 
              parameters are grouped by order of input parameter in groups of 3 (source, dest, intercal) and the number of those parameters needs to be even""")

parser.add_argument('-s', '--source',   action='append', help="source folder path", type=pathlib.Path)
parser.add_argument('-r', '--replica',  action='append', help="replica folder path", type=pathlib.Path)
parser.add_argument('-i', '--interval', action='append', help="source folder interval scan", type=int)
parser.add_argument('-l', '--logPath', action='store',  help="folder for logs", type=pathlib.Path)

inputArgs = parser.parse_args()
# print(inputArgs.replica)


