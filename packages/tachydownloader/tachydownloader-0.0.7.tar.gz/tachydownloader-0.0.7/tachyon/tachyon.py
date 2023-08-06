#!/usr/bin/env python3
# coding: utf-8

try:
    import tachyon.tools as tools
except:
    import tools as tools

import sys

import os, re, threading, math, requests, click, time
from tqdm import tqdm


class tachydownload():
    global text
    text = tools.textEffects()

    global chunkSize
    global threadNum
    global downloadUrl
    global fileName
    global filePath
    global fileSize
    global pythonCompatible
    global verboseState

    def __init__(self, downloadUrl, fileName, fileSize, verboseState):
        self.downloadUrl = downloadUrl
        self.fileName = fileName
        self.fileSize = fileSize
        self.threadNum = 0
        self.threadDivisor()
        self.variableSetup()
        self.verboseState = verboseState
        self.isPythonCompatible()
        tools.printText(text.formatText("BOLD", "Downloading file: \"" + self.fileName + "\""))

    def consoleMsg(self, type, oldTime=time.time()):
        if type=="header":
            tools.printText("Tachyon", asciiArt=True)
            tools.printText(text.formatText("BOLD", "\nThe faster than light media downloader"))
        elif type=="completion":
            tools.printText(text.formatText("BOLD", "\nSuccess! 🎉 🎉 🎉\nTime taken: " + str(time.time() - oldTime) + " seconds\n" + "File located at: ~/Desktop/Downloads by Tachyon/" + self.fileName))
        elif type=="sysfail":
            tools.printText(text.formatText("BOLD", "One of the modules has not been imported\nEnsure the following modules are installed:\nos, re, threading, math, requests, click, time"))

    def isPythonCompatible(self):
        if sys.version_info <= (3, 0):
            self.pythonCompatible = False
        else:
            self.pythonCompatible = True

    def threadDivisor(self):
        '''for newThreadNum in range(1, 200):
            chunkDivider = self.fileSize % newThreadNum
            if chunkDivider == 0 and newThreadNum > self.threadNum:
        '''
        self.threadNum = 98
        self.chunkSize = math.ceil(self.fileSize/self.threadNum)
        self.threadNum += 1

        if self.verboseState:
            print("Filesize: %s     Chunksize: %s     Threadnum: %s" % (self.fileSize, self.chunkSize, self.threadNum))

    def cleanHiddenFiles(self):
        for file in os.listdir(tools.downloadDirectory()):
            if re.search(r'^\.\d+$', file):
                os.remove(os.path.join(tools.downloadDirectory(), file))

    def variableSetup(self):
        if tools.downloadDirectory() is not None:
            self.filePath = os.path.join(tools.downloadDirectory(), self.fileName)
        else:
            self.filePath = os.path.join(os.path.join(os.path.expanduser("~"), "Desktop"), self.fileName)

    def newThread(self, origin):
        '''with tqdm(total=130, ascii=True, ncols=100) as progBar:
            for i in range(130):
                with open(self.filePath, mode='a') as outputFile:
                    outputFile.write("01")
                    progBar.update(1)
        '''
        range = {"Range": "bytes=%s-%s" % (origin, origin+self.chunkSize-1)}
        fileReq = requests.get(self.downloadUrl, headers=range, stream=True)

        file = fileReq.content
        # Each thread creates a hidden dotfile within the tachyon folder
        with open(os.path.join(tools.downloadDirectory(), "." + str(origin)), "wb") as  hiddenFile:
            hiddenFile.write(file)

    def main(self):
        if not self.pythonCompatible:
            print("Error: Python2 detected.\nPlease install python3 and run:\n'python3 -m tachyon'")
            sys.exit()

        oldTime = time.time()
        threads = []

        with tqdm(total=self.threadNum*2, ascii=True, ncols=100) as progBar:
            for threadID in range(0, self.threadNum):
                thread = threading.Thread(target = self.newThread, args=(threadID*self.chunkSize,))
                thread.start()
                threads.append(thread)
                progBar.update(1)

            for thread in threads:
                thread.join()
                progBar.update(1)


        self.filePath = open(self.filePath, "wb")
        for sections in range(0, self.threadNum):
            readFile = open(os.path.join(tools.downloadDirectory(), "." + str(sections*self.chunkSize)), "rb")
            self.filePath.write(readFile.read())
            os.remove(os.path.join(tools.downloadDirectory(), "." + str(sections*self.chunkSize)))

        self.filePath.close()
        self.cleanHiddenFiles()
        self.consoleMsg("completion", oldTime)


settings = dict(help_option_names=['--help', '-h'])
@click.command(context_settings=settings)
@click.option("--name", "-n", metavar="[TEXT]", help="The name which the downloaded file will be saved under.")
@click.option("--verbose", "-vv", default=False,help="Toggles verbose mode, showing chunksize, filesize, etc.")
@click.argument("download_url", type=click.Path())
def executeDownload(name, verbose, download_url):
    """\b
    ########    ###     ######  ##     ## ##    ##  #######  ##    ##
       ##      ## ##   ##    ## ##     ##  ##  ##  ##     ## ###   ##
       ##     ##   ##  ##       ##     ##   ####   ##     ## ####  ##
       ##    ##     ## ##       #########    ##    ##     ## ## ## ##
       ##    ######### ##       ##     ##    ##    ##     ## ##  ####
       ##    ##     ## ##    ## ##     ##    ##    ##     ## ##   ###
       ##    ##     ##  ######  ##     ##    ##     #######  ##    ##

    Tachyon — The faster than light media downloader.

    (c) 2018 Akshat Bisht under the MIT license."""
    global filename
    global filesize
    global verboseActivated

    verboseActivated = verbose
    try:
        urlInfo = requests.head(download_url)
        filesize = int(urlInfo.headers["Content-Length"])
    except:
        print("Try another download URL or type \"tachyon.py --help\" for help.\n\nError: Input argument \"DOWNLOAD_URL\" appears to be corrupt.")
        return

    if name:
        filename = name
    else:
        filename = download_url.split('/')[-1]

    run = tachydownload(downloadUrl=download_url, fileName=filename, fileSize=filesize, verboseState=verboseActivated)
    run.main()

if __name__ == '__main__':
    executeDownload()
