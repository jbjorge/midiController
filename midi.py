import glob
import grp
import os
import pwd
import time
import sys
from multiprocessing import Process

import keyboardleds
import rtmidi

ledkit = keyboardleds.LedKit('/dev/input/by-id/usb-CHESEN_USB_Keyboard-event-kbd')
blink = False

def drop_privileges():
    uid = pwd.getpwnam('nobody').pw_uid
    gid = grp.getgrnam('nogroup').gr_gid
    os.setgid(gid)
    os.setuid(uid)

def ledOn(number):
    blink = False
    ledOff()
    if number == 1:
        ledkit.num_lock.set()
    elif number == 2:
        ledkit.caps_lock.set()
    elif number == 3:
        ledkit.scroll_lock.set()
    elif number == 4:
        blink = True
        while blink == True:
            ledkit.num_lock.set()
            time.sleep(0.3)
            ledOff()
            time.sleep(0.3)
    elif number == 5:
        blink = True
        while blink == True:
            ledkit.num_lock.set()
            ledkit.caps_lock.set()
            time.sleep(0.3)
            ledOff()
            time.sleep(0.3)
    elif number == 6:
        blink = True
        while blink == True:
            ledkit.num_lock.set()
            ledkit.caps_lock.set()
            ledkit.scroll_lock.set()
            time.sleep(0.3)
            ledOff()
            time.sleep(0.3)

def ledOff():
    ledkit.num_lock.reset()
    ledkit.caps_lock.reset()
    ledkit.scroll_lock.reset()

def getKeypress():
    import sys, tty, termios
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def main():
    #drop_privileges()
    midiout = rtmidi.MidiOut()
    midiout.open_port(0)
    process = None

    print ('Listening for input')
    keyPress = getKeypress()
    while keyPress != "q":
        if process != None:
            process.terminate()
        print keyPress
        if (keyPress == "r"):
            midiout.send_message([0xC0, 0])
            process = Process(target = ledOn, args = (1, ))
            process.start()
        elif (keyPress == "m"):
            midiout.send_message([0xC0, 3])
            process = Process(target = ledOn, args = (2, ))
            process.start()
        elif (keyPress == "y"):
            midiout.send_message([0xC0, 2])
            process = Process(target = ledOn, args = (3, ))
            process.start()
        elif (keyPress == "g"):
            midiout.send_message([0xC0, 1])
            process = Process(target = ledOn, args = (4, ))
            process.start()
        elif (keyPress == "k"):
            midiout.send_message([0xC0, 2])
            process = Process(target = ledOn, args = (5, ))
            process.start()
        keyPress = getKeypress()

if __name__ == '__main__':
    main()


# vim:ts=4 sw=4 et

# available_ports = midiout.get_ports()

# if available_ports:
#     midiout.open_port(0)
# else:
#     midiout.open_virtual_port("My virtual output")

# note_on = [0x99, 60, 112] # channel 10, middle C, velocity 112
# note_off = [0x89, 60, 0]
# midiout.send_message(note_on)
# time.sleep(0.5)
# midiout.send_message(note_off)

# del midiout