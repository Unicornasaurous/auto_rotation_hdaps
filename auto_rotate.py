#!/usr/bin/env python3

import sys, os, sh, threading, time
from tablet_mode_detection import pipe_switch_output, listen_for_switch_state

DNAME = "LVDS-1" #This is your display name--may be different
STYLUS_NAME = "Wacom Serial Penabled Pen stylus" #This is your stylus device name

def rotate():
    while True:
        from tablet_mode_detection import tablet_mode
        if tablet_mode:
            print("[Tablet Mode] On")
            while True:
                from tablet_mode_detection import tablet_mode
                with open('/sys/devices/platform/hdaps/position', 'r') as f: 
                    coordinates = f.read()
                x1 = abs(int(((coordinates.split("(")[1]).split(")")[0]).split(",")[0]))
                y1 = abs(int(((coordinates.split("(")[1]).split(")")[0]).split(",")[1]))
                if not tablet_mode:
                    print("[Tablet Mode] Off")
                    sh.xrandr("--output", DNAME, "--rotate", "normal")
                    sh.xsetwacom("set", STYLUS_NAME, "Rotate", "none")
                    break
                elif x1 < 350:
                    sh.xrandr("--output", DNAME, "--rotate", "right")
                    sh.xsetwacom("set", STYLUS_NAME, "Rotate", "cw")
                elif x1 > 620:
                    sh.xrandr("--output", DNAME, "--rotate", "left")
                    sh.xsetwacom("set", STYLUS_NAME, "Rotate", "ccw")
                elif y1 < 350:
                    sh.xrandr("--output", DNAME, "--rotate", "inverted")
                    sh.xsetwacom("set", STYLUS_NAME, "Rotate", "half")
                elif y1 > 620:
                    sh.xrandr("--output", DNAME, "--rotate", "normal")
                    sh.xsetwacom("set", STYLUS_NAME, "Rotate", "none")

switch_output_thread = threading.Thread(target=pipe_switch_output)
switch_output_thread.start()
time.sleep(.5)
listen_switch_thread = threading.Thread(target=listen_for_switch_state)
listen_switch_thread.start()
rotate()
