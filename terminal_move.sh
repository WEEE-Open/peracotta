#!/bin/bash

echo 'I need root permission to move the file just this one time'
sudo mv "./generate_files_pkexec.policy" "/usr/share/polkit-1/actions/generate_files_pkexec.policy"
