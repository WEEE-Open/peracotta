#!/bin/bash

function print_usage {
    echo "Use -h or --help to show this help."
    echo "Usage: $0 <optional path_to_generate_files_to>"
    echo ""
    echo "If no argument is given, then this script will "
    echo "interactively guide you to run the PERACOTTA "
    echo "data gathering package."
    exit 0
}

function print_gpu_prompt {
  echo ""
  echo "Where is the GPU in your PC? c/g/b"
  echo "c for integrated in CPU"
  echo "g for discrete graphics card"
  echo "b for integrated in motherboard"
}

function run_extract_data {
  echo ""
  echo "The following output can be copy-pasted "
  echo "into the 'Bulk Add' page of the TARALLO, "
  echo "from '[' to ']':"
  echo ""
  ./extract_data.py -$ans $OUTPUT_PATH
}

if [ $# -eq 1 ]; then
  if [ $1 = "-h" -o $1 = "--help" ]; then
    print_usage
  else
    OUTPUT_PATH=$1
  fi
else
  if [ -d tmp ]; then
    echo "Overwrite existing files in tmp dir? y/N"
    read ans_tmp
    if [ $ans_tmp = "y" -o $ans_tmp = "Y" ]; then
      echo "Overwriting..."
      OUTPUT_PATH="tmp"
    else
      echo "Output files to working directory? y/N"
      read ans_wd
      if [ $ans_wd = "y" -o $ans_wd = "Y" ]; then
        echo "Outputting files to working directory..."
        OUTPUT_PATH="."
      else
        echo "Quitting..."
        exit -1
      fi
    fi
  else
    mkdir tmp
    OUTPUT_PATH="tmp"
  fi
fi

sudo ./generate_files.sh $OUTPUT_PATH

# evaluates to while true but slightly faster
while : ; do
  print_gpu_prompt
  read ans
  if [ $ans = "c" ]; then
    run_extract_data
    break
  elif [ $ans = "g" ]; then
    run_extract_data
    break
  elif [ $ans = "b" ]; then
    run_extract_data
    break
  else
    echo "I didn't get it, sorry."
  fi
done
