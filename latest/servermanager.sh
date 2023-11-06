#!/bin/bash

BTSERVER=server/bluetoothserver.py
LANSERVER=server/lanserver.py
BTSNAME=btserver
LANSNAME=lanserver
RESTARTNAME=restartcmd

# Help page
if [ -z "$1" ]; then
	echo "$0 start - Starts the servers"
	echo "$0 btlogs - Opens Bluetooth logs"
	echo "$0 lanlogs - Opens Lan logs"
	echo "$0 stop - Stops the servers"
	echo "$0 restart - Sends the restart command" 
fi

# Start Bluetooth and Lan Server
if [ "$1" = "start" ]; then
	# Kill other screens
	screen -XS $BTSNAME kill
	screen -XS $LANSNAME kill

	# Power on
	bluetoothctl power on
	bluetoothctl discoverable on

	screen -S $LANSNAME -d -m bash
	screen -r $LANSNAME -X stuff "python3 $LANSERVER 0.0.0.0 8080"$(echo -ne '\015')
	sleep 2
	screen -S $BTSNAME -d -m bash
	screen -r $BTSNAME -X stuff "python3 $BTSERVER"$(echo -ne '\015')
fi

if [ "$1" = "restart" ]; then
	screen -S $RESTARTNAME -d -m bash
	screen -r $RESTARTNAME -X stuff "echo riavvia | python3 client.py 0.0.0.0 8080"$(echo -ne '\015')
	screen -XS $RESTARTNAME kill
fi

if [ "$1" = "btlogs" ]; then
	screen -x $BTSNAME
fi

if [ "$1" = "lanlogs" ]; then
	screen -x $LANSNAME
fi

if [ "$1" = "stop" ]; then
	screen -XS $BTSNAME kill
	screen -XS $LANSNAME kill
fi

