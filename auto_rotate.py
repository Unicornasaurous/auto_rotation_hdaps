#!/usr/bin/env python3

import sys, os, sh, threading, time
from tablet_mode_detection import pipe_switch_output, listen_for_switch_state

def find_monitor_name():
    os.system("xrandr --listmonitors | grep '0:' > /tmp/showmonitor.txt")
    with open("/tmp/showmonitor.txt", "rb") as f:
        byts = 0
        f.seek(-2, os.SEEK_END)
        while f.read(1) != b' ':
            byts += 1
            f.seek(-2, os.SEEK_CUR)
        return f.read(byts).decode("utf-8")

MONITOR_NAME = find_monitor_name()
STYLUS_NAME = "Wacom Serial Penabled Pen stylus" #This is your stylus device name. Use 'xsetwacom list devices' 
                                                 #in the command line to display your touch devices. Change this 
                                                 #variable as needed. 
    ##rotate() method:
#Loops until tablet_mode, the mode-indicating-variable, is true. Once such case is met, 
#it loops through, continuously opening and reading the output file that contains accelerometer
#coordinates from HDAPS. It uses these coordinates with a series of statements to determine which 
#set of commands to invoke using sh. These commands, of course, rotate the x11 display along with 
#the stylus input matrix according to the position of your laptop/tablet. The moment tablet_mode is 
#found to be false, it breaks out of the subloop and goes back into the main loop, awaiting tablet_mode
#to be true again.
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
                    sh.xrandr("--output", MONITOR_NAME, "--rotate", "normal")
                    sh.xsetwacom("set", STYLUS_NAME, "Rotate", "none")
                    break
                elif x1 < 350:
                    sh.xrandr("--output", MONITOR_NAME, "--rotate", "right")
                    sh.xsetwacom("set", STYLUS_NAME, "Rotate", "cw")
                elif x1 > 620:
                    sh.xrandr("--output", MONITOR_NAME, "--rotate", "left")
                    sh.xsetwacom("set", STYLUS_NAME, "Rotate", "ccw")
                elif y1 < 350:
                    sh.xrandr("--output", MONITOR_NAME, "--rotate", "inverted")
                    sh.xsetwacom("set", STYLUS_NAME, "Rotate", "half")
                elif y1 > 620:
                    sh.xrandr("--output", MONITOR_NAME, "--rotate", "normal")
                    sh.xsetwacom("set", STYLUS_NAME, "Rotate", "none")

switch_output_thread = threading.Thread(target=pipe_switch_output)
switch_output_thread.start()
time.sleep(.5)
listen_switch_thread = threading.Thread(target=listen_for_switch_state)
listen_switch_thread.start()
print(f"Starting autorotation...\n==>Please confirm that the following monitor name\nmatches with the monitor name found in the command output that proceeds it\n(should be something like 'LVDS-1' or a similarly lengthed string in capital letters)\n<==\nMonitor Name: {MONITOR_NAME}\n[xrandr --listmonitors | grep '0:'] Output:")
os.system("xrandr --listmonitors | grep '0:'")
print(f"\n==>Please confirm that the following wacom device matches with the one that you wish to use from the output that proceeds it.\n<==\nWacom Device: {STYLUS_NAME}\n[xsetwacom list devices] Output:")
os.system("xsetwacom list devices")
print("\nNote: When you physically convert your laptop into tablet mode,\n'[Tablet Mode] On' should be echoed in the terminal/console.\nConversely, '[Tablet Mode] Off' should be echoed.")
rotate()
