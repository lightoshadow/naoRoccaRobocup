# Notes

## Requirements
- PyBluez:
	> pip install pybluez

## Commands
- bluetoothctl (to set the power on and discoverable true)

## Structure
- nao
	- Contains all the nao's code to run (socket)
- server
	- Contains all the server's code (use instead the `servermanager.sh` utility)
- clients
	- Contains the clients' code

## Infos
The configuration is this one: the NAO sends via a LAN cable the data to thee Raspberry, and it will forward the data through a Bluetooth server to the other clients.

## Bugs
If you run the bluetooth client and it crashes you need to open bluetoothctl and disconnect from the server.

You need to start the processes with `screen`.
