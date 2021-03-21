#! /usr/bin/env python3

# This script will be in charge of starting, stopping and restarting of the sender script

## this probably should be a bash script

import subprocess, signal
import os
from time import sleep
from threading import Thread

thread = Thread(target=os.system, args=["./sender.py"], daemon=True)
thread.start()

sleep(5)

# p = subprocess.Popen(['ps'], stdout=subprocess.PIPE)
# out, err = p.communicate()

# for line in out.splitlines():
#     print(line)
#     if 'python3' in line:
#         pid = int(line.split(None, 1)[0])
#         os.kill(pid, signal.SIGKILL)

