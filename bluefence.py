#!/usr/bin/python

# BlueFence version 0.1 (Prototype)
# Author: Yeni Setiawan
# Email	: sandalian@protonmail.ch
# Blog	: https://sandalian.com

import bluetooth
import time
import sys
import os

SCAN_PERIOD = 2
IF_BT_GONE = 'tmux new-session -ds \'nightswatch\' /home/pedrohlc/.local/bin/nightswatch-vow'
YOUR_WATCH_HAS_ENDED = 'rm -f /home/pedrohlc/.local/tmp/nightswatch/.onpatrol'
MAX_MISSED = 3    
VERBOSE =  True

def file_get_contents(filename):
    with open(filename) as f:
        return f.read()

btAddr = file_get_contents('/home/pedrohlc/.config/nightswatch-commander.mac')
btInRange = True
screenLocked = False
awayCounter = 0

print("Identifying device...")

try:
	# initial check, see if mentioned BT device active. If it's not, clean exit
	
	btName =  bluetooth.lookup_name(btAddr,timeout=5)

	if btName:
		if VERBOSE:
			print('OK: Found your device',btName)
		
		while True:
			who =  bluetooth.lookup_name(btAddr,timeout=2)

			if who:

				status = 'near'
				btInRange=True
				awayCounter=0
				os.system(YOUR_WATCH_HAS_ENDED)

			else:
				awayCounter+=1
				status = 'away'

			if awayCounter > MAX_MISSED:
				os.system(IF_BT_GONE)
				status = 'MATI!'
				awayCounter = 0
				btInRange=False

			time.sleep(SCAN_PERIOD)

			print(status, '|', awayCounter, '|', btInRange, '|', time.strftime('%H:%M:%S'))
	else:
		print('ER: Your bluetooth device is not active')
		sys.exit
	

# this usually happen when your PC's bluetooth is disabled.
except:
	print('ER: Bluetooth on PC is not active')
