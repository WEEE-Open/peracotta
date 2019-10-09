#!/bin/bash

if [ $# -eq 0 ]; then
    echo "No path given: outputting files to working directory"
    OUTPATH="."
elif [ $# -eq 1 ]; then
    echo "Outputting files to "$1
    OUTPATH=$1
else
    echo -n "Unexpected number of parameters.\nUsage: sudo ./generate_files.sh /optional/path/to/files"
fi

dmidecode -t baseboard > "$OUTPATH/baseboard.txt"
dmidecode -t connector > "$OUTPATH/connector.txt"
dmidecode -t chassis > "$OUTPATH/chassis.txt"
truncate "$OUTPATH/net.txt"
NET=($(find /sys/class/net -maxdepth 1 \( -name "en*" -o -name "wl*" \) -exec basename  '{}' ';'))
for NETDEV in "${NET[@]}"
do
	ADDRESS=$(cat /sys/class/net/$NETDEV/address)
	if [[ $? -ne 0 ]]
	then
		echo The \"invalid argument\" error above is normal, disregard it
	fi
	SPEED=$(cat /sys/class/net/$NETDEV/speed)
	echo $NETDEV $ADDRESS $SPEED >> "$OUTPATH/net.txt"
done
lscpu > "$OUTPATH/lscpu.txt"
lspci -v > "$OUTPATH/lspci.txt"
glxinfo > "$OUTPATH/glxinfo.txt"
DISKZ=($(lsblk -d -I 8 -o NAME -n))
echo Found ${#DISKZ[@]} disks
for d in "${DISKZ[@]}"; do
	smartctl -x /dev/$d > "$OUTPATH/smartctl-dev-$d.txt"
done
# Already done on our custom distro, but repetita iuvant
modprobe at24
modprobe eeprom
decode-dimms > $OUTPATH/dimms.txt
