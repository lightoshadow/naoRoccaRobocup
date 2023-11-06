#!/bin/bash

WORKSPACE=$(pwd)
BTSCLIENT=btclient

# Help page
if [ -z "$1" ]; then
	echo "!!! BLACK DRAGON !!!"
	echo "$0 start - Starts the client"
	echo "$0 btlogs - Opens Bluetooth logs (client)"
	echo "$0 stop - Stops the client"
fi

# Start Bluetooth Client
if [ "$1" = "start" ]; then
	# Kill other screens
	screen -XS $BTSCLIENT kill
	screen -S $BTSCLIENT -d -m bash
	screen -r $BTSCLIENT -X stuff "python3 black_client.py"$(echo -ne '\015')
fi

if [ "$1" = "btlogs" ]; then
	screen -x $BTSCLIENT
fi

if [ "$1" = "stop" ]; then
	screen -XS $BTSCLIENT kill
fi

