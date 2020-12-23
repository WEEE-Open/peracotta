#!/bin/bash
# apt remove may leave some config files which can lead to dpkg detect an uninstalled package as installed
# apt purge works
dpkg -s pciutils i2c-tools mesa-utils smartmontools dmidecode &> /dev/null

exit $?