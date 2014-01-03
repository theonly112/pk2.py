from pk2Reader import pk2Reader
from sys import stdin, argv
import os


def printUsage():
    print("Usage: pk2.py filename.pk2")
def printCommands():
    print("Commands: \n ls : prints all files and directories in the current directory. \n cd 'directory': change directory \n extract 'filename' : extracts into the current directory");
def inputLoop():
    userInput = ""
    while userInput != "exit":
        userInput = stdin.readline()[:-1]
        processInput(userInput)
    reader.close() #Close open file when done.

def processInput(input):
    if input.startswith("cd"):
        reader.changeDirectory(input[input.find(" ") + 1:])
    elif input.startswith("extract"):
        clearConsole()
        reader.extractFile(input[input.find(" ") + 1:])
    elif input == "ls":
        clearConsole()
        reader.ls()

def clearConsole():
    os.system(['clear','cls'][os.name == 'nt']) #Clear console. Should work on most platforms

if __name__ == "__main__":
    try:
        filename = argv[1]
        reader = pk2Reader(filename)
        clearConsole()
        reader.ls()
        printCommands()
    except IndexError as e:
        printUsage()
    inputLoop()
