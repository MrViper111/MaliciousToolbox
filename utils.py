import os
from Command import Command



def clearScreen():
    try:
        if os.name == "nt":
            os.system("cls")
        else:
            os.system("clear")
    except:
        for i in range(50):
            print()


def setWindowTitle(title: str):
    if os.name == "nt":
        os.system(f"title {title}")
    else:
        pass


def throwError(message):
    print("\033[91m[ERROR] " + message + "\033[97m")

def throwMissingArgsError(command: Command):
    throwError(f"Missing arguments! Usage: {command.name} {' '.join(command.arguments)}")


def filterArguments(input):
    return str(input).replace(str(input).split()[0], "").split()
    

def deleteFile(file_name: str):
    os.system("del " + file_name)
