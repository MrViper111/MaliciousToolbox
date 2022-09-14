import os
import time
import requests
import sys
import json

import subprocess
from win32comext.shell import shell

from Command import Command
from utils import *
from marcoUtils import getMacros, runMacro



version = "2.0" # Do not change
show_title = True
show_toolbox_prefix = True
startup_task = None # This will run on startup. If you want nothing, put None. Otherwise put the name of the task


# Custom Commands

commandhelp_command = Command(
    name="commandhelp",
    description="Lists all commands and information",
    arguments=[],
    aliases=["cmdhelp"]
)
wifinetworks_command = Command(
    name="wifinetworks",
    description="Spams the terminal",
    arguments=["<text>"],
    aliases=["wifilist", "networklist"]
)
wifiinfo_command = Command(
    name="wifiinfo",
    description="Gets information on a WiFi network",
    arguments=["<network_name>"],
    aliases=["wifidata"]
)
dos_command = Command(
    name="dos",
    description="Performs a DoS attack",
    arguments=["<host>", "<amount>", "<delay>"],
    aliases=[]
)
firewall_command = Command(
    name="firewall",
    description="Sets the status of a firewall",
    arguments=["<on/off>"],
    aliases=[]
)
listmacros_command = Command(
    name="listmacros",
    description="Lists all existing macros",
    arguments=[],
    aliases=["macros", "macrolist"]
)
runmacro_command = Command(
    name="runmacro",
    description="Runs a macro",
    arguments=["<macro_name>"],
    aliases=[]
)



# Actual code

# ok figure out how to change directories without it throwing 500 errors

setWindowTitle(f"Malicious Toolbox v{version}")
clearScreen()

if show_title:
    print("-----------------------------")
    print(f"   Malicious Toolbox v{version}")
    print("-----------------------------")
    print()
    print(f"Type '{commandhelp_command.name}' for a list of custom commands and information.")
    if os.name != "nt":
        print("NOTICE: Most custom commands only work on Windows!")
    print()

if show_toolbox_prefix:
    toolbox_prefix = "\033[92m[TOOLBOX]\033[97m "
else:
    toolbox_prefix = ""


if startup_task:
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    try:
        startup_data = json.load(open(os.path.join(__location__, "startuptasks.json"), "r+"))
    except:
        throwError("Unable to get startup JSON data.")

    try:
        task_data = startup_data[startup_task]
    except:
        throwError(f"Unable to get startup task data for the task {startup_task}.")

    for i in range(len(task_data)):
        os.system(task_data[i])


while True:
    command_input = input(f"{toolbox_prefix}{os.path.realpath(os.path.dirname(__file__))} \033[1;30;40m>\033[97m ")

    if commandhelp_command.matches(command_input):
        print(
            f"\n{commandhelp_command.getCommandData()}\n" + 
            f"{wifinetworks_command.getCommandData()}\n" +
            f"{dos_command.getCommandData()}\n" +
            f"{firewall_command.getCommandData()}\n" +
            f"{listmacros_command.getCommandData()}\n" +
            f"{runmacro_command.getCommandData()}\n"
        )
        


    elif wifinetworks_command.matches(command_input):
        if os.name == "nt":
            os.system("netsh wlan show profiles")
        else:
            os.system("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport scan")



    elif wifiinfo_command.matches(command_input):
        arguments = filterArguments(command_input)

        if wifiinfo_command.checkAllArguments(arguments) == "ERROR":
            throwMissingArgsError(wifiinfo_command)
        else:
            os.system(f"netsh wlan show profiles {arguments[0]} key=clear")

    

    elif dos_command.matches(command_input):
        arguments = filterArguments(command_input)

        if dos_command.checkAllArguments(arguments) == "ERROR":
            throwMissingArgsError(dos_command)
        else:
            expected_requests = arguments[1]
            successful_requests = 0

            for i in range(int(expected_requests)):
                try:
                    os.system(f"ping {arguments[0]} -n 1")

                    successful_requests += 1
                except:
                    throwError(f"Failed while trying to ping {arguments[0]}.")

                time.sleep(float(arguments[2]))

            if successful_requests == expected_requests:
                print(f"DoS fully completed! ({successful_requests}/{expected_requests} sent)")
            elif successful_requests == 0:
                print(f"DoS failed! ({successful_requests}/{expected_requests} sent)")
            else:
                print(f"DoS partially completed! ({successful_requests}/{expected_requests} sent)")



    elif firewall_command.matches(command_input):
        arguments = filterArguments(command_input)

        if firewall_command.checkAllArguments(arguments) == "ERROR":
            throwMissingArgsError(firewall_command)
        else:

            if arguments[0] == ("on" or "enabled" or "enable"):
                try:
                    shell.ShellExecuteEx(
                        lpVerb='runas', 
                        lpFile='cmd.exe', 
                        lpParameters='/c '+ "NetSh Advfirewall set allprofiles state on"
                    )
                    print("The firewall has been enabled!")
                except:
                    throwError("Unable to enable the firewall.")

            elif arguments[0] == ("off" or "disabled" or "disable"):
                try:
                    shell.ShellExecuteEx(
                        lpVerb='runas', 
                        lpFile='cmd.exe', 
                        lpParameters='/c '+ "NetSh Advfirewall set allprofiles state off"
                    )
                    print("The firewall has been disabled!")
                except:
                    throwError("Unable to disable the firewall.")

            else:
                throwMissingArgsError(firewall_command)



    elif listmacros_command.matches(command_input):
        try:
            print("Current macros: " + (", ".join(getMacros())))
        except:
            throwError("There was somehow an error while trying to access the macros.json file. Was it moved?")
            print(os.path.join(sys.path[0]) + "\macros.json")



    elif runmacro_command.matches(command_input):
        arguments = filterArguments(command_input)

        if runmacro_command.checkAllArguments(arguments) == "ERROR":
            throwMissingArgsError(runmacro_command)
        else:
            print(f"Running {arguments[0]}...")
            runMacro(str(arguments[0]))
            print("Macro execution completed!")



    else:
        if command_input == "":
            pass
        else:
            if str(subprocess.getoutput(command_input)) == f"'{command_input.split()[0]}' is not recognized as an internal or external command,\noperable program or batch file.":
                throwError(subprocess.getoutput(command_input))
            else:
                os.system(command_input)