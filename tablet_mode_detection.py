import os, sh, sys, threading, time, re
input_device = "/dev/input/by-path/platform-thinkpad_acpi-event" 
tablet_mode = False

    ##pipe_switch_output() method:
#invokes the command to create a subprocess that illicits 
#output indicating what state the tablet-laptop is in(tablet mode on or off). 
#This process's output is piped into 'output.txt')
def pipe_switch_output():
    os.system(f"stdbuf -oL -eL libinput debug-events --device {input_device} > output.txt")
    
    ##listen_for_switch_state() method:
#continuously opens 'output.txt' to determine what state the laptop is in. 
#Opens in binary mode, uses the seek method to go to the last character of
#the file, and iterates over every character going to the left until a '\n'
#byte character is detected(This implies the start of last line). After
#finding the last line of the file, it uses the readline and decode methods
#to store that line as an object in order for the search method to determine the state.
def listen_for_switch_state():
    global tablet_mode
    while True:
        with open('output.txt', 'rb') as f:
            try:
                f.seek(-2, os.SEEK_END)
                while f.read(1) != b'\n':
                    f.seek(-2, os.SEEK_CUR)
            except OSError:
                f.seek(0)
            new_output_line = f.readline().decode()
            #print(new_output_line)
            #print(re.search("state 1", new_output_line, re.IGNORECASE))
            if re.search("state 1", new_output_line, re.IGNORECASE) != None:
                tablet_mode = True
            else:
                tablet_mode = False



            

