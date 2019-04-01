#!/usr/bin/env bash

dmidecode -t baseboard >> baseboard.txt
dmidecode -t chassis >> chassis.txt
lscpu >> lscpu.txt
# add other commands
