#!/bin/bash

set -eu

# apt remove may leave some config files which can lead to dpkg detect an uninstalled package as installed
# apt purge works
# hence we check first for an error exit code, then we look for any string that is not "installed" in the output
# from the dpkg 1.19.7 manual:
#  Package States
#    not-installed
#       The package is not installed on your system.
#    config-files
#       Only the configuration files of the package exist on the system.
#    half-installed
#       The installation of the package has been started, but not completed for some reason.
#    unpacked
#       The package is unpacked, but not configured.
#    half-configured
#       The package is unpacked and configuration has been started, but not yet completed for some reason.
#    triggers-awaited
#       The package awaits trigger processing by another package.
#    triggers-pending
#       The package has been triggered.
#    installed
#       The package is unpacked and configured OK.

_TMP_FILE=.tmp_$(date +%s)
_ERR_STRINGS=("not-installed" "config-files" "half-installed" "unpacked" "half-configured" "triggers-awaited" "triggers-pending")

function safe_exit() {
    rm $_TMP_FILE
    exit $1
}

dpkg -s pciutils i2c-tools mesa-utils smartmontools dmidecode &> $_TMP_FILE
_RET_CODE=$?

# if dpkg return code is an error return it directly
[[ $_RET_CODE != 0 ]] && safe_exit $_RET_CODE

# else if any error string is contained in the output return 1 for error
for _STR in ${_ERR_STRINGS[@]}; do
    [[ $(grep $_STR $_TMP_FILE) != "" ]] && safe_exit 1
done

# else, all packages are correctly installed
safe_exit 0
