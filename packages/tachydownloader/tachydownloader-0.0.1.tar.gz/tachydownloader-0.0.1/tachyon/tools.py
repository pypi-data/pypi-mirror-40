#!/usr/bin/env python3
# coding: utf-8

import sys

try:
    import os, re, threading, math, requests, click, time
    from tqdm import tqdm

except:
    print("Ensure the following modules are installed:\n requests, click, tqdm\n\nError: Module not found")
    exit()

class textEffects:
   PURPLE = '\033[95m'
   CYAN = '\033[96m'
   DARKCYAN = '\033[36m'
   BLUE = '\033[94m'
   GREEN = '\033[92m'
   YELLOW = '\033[93m'
   RED = '\033[91m'
   BOLD = '\033[1m'
   UNDERLINE = '\033[4m'
   END = '\033[0m'

   def formatText(self, operation, text):
       return getattr(self, operation) + text + self.END

def printText(text, asciiArt=False, font="banner3"):
    if "pyfiglet" in sys.modules and asciiArt:
        output = Figlet(font=font)
        print(output.renderText(text))
    else:
        print(text)

def downloadDirectory():
    desktopPath = os.path.join(os.path.expanduser("~"), "Desktop")
    downloadFolder = os.path.join(desktopPath, "Downloads by Tachyon")

    if not os.path.exists(downloadFolder):
        try:
            os.makedirs(downloadFolder)
            return downloadFolder
        except:
            return None
    else:
        return downloadFolder
