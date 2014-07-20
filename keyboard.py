import glob
import grp
import os
import pwd
import time

import keyboardleds


def drop_privileges():
    uid = pwd.getpwnam('nobody').pw_uid
    gid = grp.getgrnam('nogroup').gr_gid
    os.setgid(gid)
    os.setuid(uid)


def main():
    ledkit = keyboardleds.LedKit('/dev/input/by-id/usb-CHESEN_USB_Keyboard-event-kbd')
    drop_privileges()
    while True:
        ledkit.num_lock.reset()
        ledkit.caps_lock.set()
        time.sleep(0.1)
        ledkit.caps_lock.reset()
        ledkit.scroll_lock.set()
        time.sleep(0.1)
        ledkit.scroll_lock.reset()
        ledkit.num_lock.set()
        time.sleep(0.1)

if __name__ == '__main__':
    main()

# vim:ts=4 sw=4 et