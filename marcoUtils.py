import json
import time
import os
import sys

from pynput.keyboard import Key, Controller
from utils import throwError



keyboard = Controller()


def getJsonData():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    try:
        return json.load(
            open(os.path.join(__location__, "macros.json"), "r+")
        )
    except:
        throwError("Unable to get macro JSON data.")


def getMacros():
    __location__ = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))

    with open(os.path.join(__location__, "macros.json"), "r+") as macros_file:
        lines = [line.rstrip() for line in macros_file]
        macros = []

        for i in range(len(lines)):
            if (lines[i].startswith("    ")) and (lines[i].endswith(": [")):
                polished_macro = lines[i].replace(": [", "").replace("\"", "").strip()
                macros.append(polished_macro)

        return macros


def getMacroActions(macro: str):
    try:
        return getJsonData()[macro]
    except:
        return "Unable to get macro actions."


def getKeyType(action: str):
    if action == "alt": return Key.alt
    elif action == "alt_gr": return Key.alt_gr
    elif action == "alt_l": return Key.alt_l
    elif action == "alt_r": return Key.alt_r
    elif action == "backspace": return Key.backspace
    elif action == "caps_lock": return Key.caps_lock
    elif action == "cmd": return Key.cmd
    elif action == "cmd_l": return Key.cmd_l
    elif action == "cmd_r": return Key.cmd_r
    elif action == "ctrl": return Key.ctrl
    elif action == "ctrl_l": return Key.ctrl_l
    elif action == "ctrl_r": return Key.ctrl_r
    elif action == "delete": return Key.delete
    elif action == "end": return Key.end
    elif action == "enter": return Key.enter
    elif action == "esc": return Key.esc
    elif action == "f1": return Key.f1
    elif action == "f2": return Key.f2
    elif action == "f3": return Key.f3
    elif action == "f4": return Key.f4
    elif action == "f5": return Key.f5
    elif action == "f6": return Key.f6
    elif action == "f7": return Key.f7
    elif action == "f8": return Key.f8
    elif action == "f9": return Key.f9
    elif action == "f10": return Key.f10
    elif action == "f11": return Key.f11
    elif action == "f12": return Key.f12
    elif action == "home": return Key.home
    elif action == "insert": return Key.insert
    elif action == "media_next": return Key.media_next
    elif action == "media_pause_play": return Key.media_play_pause
    elif action == "media_previous": return Key.media_previous
    elif action == "media_volume_down": return Key.media_volume_down
    elif action == "media_volume_mute": return Key.media_volume_mute
    elif action == "media_volume_up": return Key.media_volume_up
    elif action == "menu": return Key.menu
    elif action == "num_lock": return Key.num_lock
    elif action == "page_up": return Key.page_up
    elif action == "page_down": return Key.page_down
    elif action == "pause": return Key.pause
    elif action == "print_screen": return Key.print_screen
    elif action == "right": return Key.right
    elif action == "left": return Key.left
    elif action == "scroll_lock": return Key.scroll_lock
    elif action == "shift": return Key.shift
    elif action == "shift_l": return Key.shift_l
    elif action == "shift_r": return Key.shift_r
    elif action == "space": return Key.space
    elif action == "tab": return Key.tab
    elif action == "up": return Key.up
    elif action == "down": return Key.down
    else: return action


def runMacro(macro: str):
    actions = getMacroActions(macro)

    for i in range(len(actions)):
        if str(actions[i]).startswith("tap:"):

            try:
                polished_action = str(actions[i])[4:]

                if polished_action.startswith("Key."):
                    polished_action = getKeyType(polished_action[4:])

                keyboard.tap(polished_action)
            except:
                throwError(f"Unable to run action from macro {macro} (Action: {actions[i]})")

        elif str(actions[i]).startswith("press:"):
            
            try:
                polished_action = str(actions[i])[6:]

                if polished_action.startswith("Key."):
                    polished_action = getKeyType(polished_action[4:])

                keyboard.press(polished_action)
            except:
                throwError(f"Unable to run action from macro {macro} (Action: {actions[i]})")

        elif str(actions[i]).startswith("release:"):
            
            try:
                polished_action = str(actions[i])[8:]

                if polished_action.startswith("Key."):
                    polished_action = getKeyType(polished_action[4:])

                keyboard.release(polished_action)
            except:
                throwError(f"Unable to run action from macro {macro} (Action: {actions[i]})")

        elif str(actions[i]).startswith("type:"):
            try:
                keyboard.type(str(actions[i])[5:])
            except:
                throwError(f"Unable to run action from macro {macro} (Action: {actions[i]})")

        elif str(actions[i].startswith("delay:")):
            time.sleep(float(str(actions[i])[6:]))
            
        else:
            throwError(f"Invalid action in macro {macro} (Action: {actions[i]})")
