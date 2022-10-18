import os
import time
import requests
import sys
import json
import socket

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
spamping_command = Command(
    name="spamping",
    description="Performs a DoS attack",
    arguments=["<target>", "<amount>", "<delay>"],
    aliases=["pingspam"]
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
injectfile_command = Command(
    name="injectfile",
    description="Injects a file into a certain directory",
    arguments=["<file>", "<directory>"],
    aliases=[]
)
sendfile_command = Command(
    name="sendfile",
    description="Sends information via email",
    arguments=["<file>", "<email>"],
    aliases=["transferfile"]
)
deletefiles_command = Command(
    name="deletefiles",
    description="Deletes files",
    arguments=[],
    aliases=[]
)
portscan_command = Command(
    name="portscan",
    description="Scans for open ports",
    arguments=["<target>", "<start_port>", "<end_port>"],
    aliases=["pscan"]
)
customcommand_command = Command(
    name="customcommand",
    description="Kind of like a BAT file",
    arguments=["<command>"],
    aliases=["cc"]
)



# Actual code

# ok figure out how to change directories without it throwing 500 errors (Kinda... not really)

def main():

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
                f"{spamping_command.getCommandData()}\n" +
                f"{firewall_command.getCommandData()}\n" +
                f"{listmacros_command.getCommandData()}\n" +
                f"{runmacro_command.getCommandData()}\n" +
                f"{injectfile_command.getCommandData()}\n" +
                f"{sendfile_command.getCommandData()}\n" +
                f"{deletefiles_command.getCommandData()}\n" +
                f"{portscan_command.getCommandData()}\n" +
                f"{customcommand_command.getCommandData()}\n"
            )
            


        elif wifinetworks_command.matches(command_input):
            if os.name == "nt":
                os.system("netsh wlan show profiles")
            else:
                os.system("/System/Library/PrivateFrameworks/Apple80211.framework/Versions/A/Resources/airport scan")



        elif wifiinfo_command.matches(command_input):
            arguments = filterArguments(command_input)

            if wifiinfo_command.checkAllArguments(arguments) == False:
                throwMissingArgsError(wifiinfo_command)
            else:
                os.system(f"netsh wlan show profiles {arguments[0]} key=clear")

        

        elif spamping_command.matches(command_input):
            arguments = filterArguments(command_input)

            if spamping_command.checkAllArguments(arguments) == False:
                throwMissingArgsError(spamping_command)
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
                    print(f"Spam ping fully completed! ({successful_requests}/{expected_requests} sent)")
                elif successful_requests == 0:
                    print(f"Spam ping failed! ({successful_requests}/{expected_requests} sent)")
                else:
                    print(f"Spam ping partially completed! ({successful_requests}/{expected_requests} sent)")



        elif firewall_command.matches(command_input):
            arguments = filterArguments(command_input)

            if firewall_command.checkAllArguments(arguments) == False:
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

            if runmacro_command.checkAllArguments(arguments) == False:
                throwMissingArgsError(runmacro_command)

            else:
                print(f"Running {arguments[0]}...")

                try:
                    runMacro(str(arguments[0]))
                    print("Macro execution completed!")
                except:
                    throwError("An error occured while trying to run this macro.")



        elif injectfile_command.matches(command_input):
            arguments = filterArguments(command_input)

            if runmacro_command.checkAllArguments(arguments) == False:
                throwMissingArgsError(injectfile_command)
            else:

                print("Do the inject stuff")



        elif sendfile_command.matches(command_input):
            arguments = filterArguments(command_input)

            if sendfile_command.checkAllArguments(arguments) == False:
                throwMissingArgsError(sendfile_command)
            else:

                print("Do the send file stuff")



        elif deletefiles_command.matches(command_input):
            arguments = filterArguments(command_input)

            if deletefiles_command.checkAllArguments(arguments) == False:
                throwMissingArgsError(deletefiles_command)
            else:

                print("delete file stuff")



        elif portscan_command.matches(command_input):
            arguments = filterArguments(command_input)

            if portscan_command.checkAllArguments(arguments) == False:
                throwMissingArgsError(portscan_command)
            else:

                target = arguments[0]
                start_port = int(arguments[1])
                end_port = int(arguments[2])
                ports_scanned = 0
                open_ports = []
                port_amount = end_port - start_port


                if start_port > end_port:
                    throwError("The starting port cannot be greater than the ending port.")
                    break

                print(f"Scanning {target} for open ports on ports {start_port}-{end_port}...")

                try:
                    for port in range(start_port, end_port + 1):
                        socket_connection = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                        socket.setdefaulttimeout(1)

                        result = socket_connection.connect_ex((target, port))
                        ports_scanned += 1

                        if result == 0:
                            open_ports.append(str(port))
                            print(f"[{round((ports_scanned/port_amount)*100, 1)}% | {ports_scanned}/{port_amount}] Port {port} is open!")
                        else:
                            print(f"[{round((ports_scanned/port_amount)*100, 1)}% | {ports_scanned}/{port_amount}] Port {port} is closed.")

                        socket_connection.close()

                except socket.gaierror:
                    throwError("The hostname could not be resolved.")
                except socket.error:
                    throwError("The server is not responding.")
                except KeyboardInterrupt:
                    print("Quit port scan process.")

                if open_ports == []:
                    open_ports = "None"
                else:
                    open_ports = ", ".join(open_ports)

                print("\nPort scan complete!\n---------------------------------------------")
                print("Target: " + target)
                print("Starting port: " + str(start_port))
                print("Ending port: " + str(end_port))
                print(f"Scanned {ports_scanned} ports.")
                print("Open ports: " + open_ports)
                print("---------------------------------------------")



        elif customcommand_command.matches(command_input):
            arguments = filterArguments(command_input)

            if customcommand_command.checkAllArguments(arguments) == False:
                throwMissingArgsError(customcommand_command)
            else:

                __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

                try:
                    customcommands_data = json.load(open(os.path.join(__location__, "customcommands.json"), "r+"))
                except:
                    throwError("Unable to get custom commands JSON data.")

                try:
                    customcommand_data = customcommands_data[arguments[0]]
                except:
                    throwError(f"Unable to get custom command data for the command {startup_task}.")

                for i in range(len(customcommand_data)):
                    os.system(customcommand_data[i])




        else:
            if command_input == "":
                pass
            else:
                if str(subprocess.getoutput(command_input)) == f"'{command_input.split()[0]}' is not recognized as an internal or external command,\noperable program or batch file.":
                    throwError(subprocess.getoutput(command_input))
                else:
                    os.system(command_input)

main()