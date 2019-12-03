#!/bin/bash

function print_usage {
  echo "Use -h or --help to show this help."
  echo "Usage: $0 [-p|--path <optional path to generate files to>] [-c|--cpu | -g|--gpu | -b|--motherboard]"
  echo ""
  echo "If no argument is given, then this script will interactively guide you to "
  echo "run the PERACOTTA data gathering package."
  echo ""
  echo "Alternatively, you can choose to pass either the path to the directory where you want the "
  echo "files to be generated, the gpu location, or both."
  echo "In this case, the script will only become interactive when needed, and it won't ask you anything "
  echo "if you pass both the path and the gpu location."
}

function check_mutually_exclusive_args {
  if [ -n $gpu_location ]; then
    echo "Only one GPU location can be given at a time, meaning you can't pass 2 or more of the following arguments:"
    echo "-c|--cpu -g|--gpu -b|--motherboard"
    echo "See usage:"
    print_usage
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
  ./extract_data.py -$gpu_location "$OUTPUT_PATH"
}

# unknown_args=()
while [[ $# -gt 0 ]]; do
  arg="$1"
  case $arg in
    -h|--help)
    print_usage
    exit 0
    ;;
    -p|--path)
    OUTPUT_PATH="$2"
    shift
    shift
    ;;
    -c|--cpu)
    check_mutually_exclusive_args
    gpu_location="c"
    shift
    ;;
    -g|--gpu)
    check_mutually_exclusive_args
    gpu_location="g"
    shift
    ;;
    -b|--motherboard)
    check_mutually_exclusive_args
    gpu_location="b"
    shift
    ;;
    *)
    echo "Unkwown option '$1'. See usage:"
    print_usage
    exit 0
    # unknown_args+=("$1") # save it in an array for later
    # shift # past argument
    ;;
  esac
done

if [ -z $OUTPUT_PATH ]; then
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
  # if gpu_location is not given as a parameter ask the user
  if [ -z $gpu_location ]; then
    print_gpu_prompt
    read gpu_location
    if [ $gpu_location = "c" ]; then
      run_extract_data
      break
    elif [ $gpu_location = "g" ]; then
      run_extract_data
      break
    elif [ $gpu_location = "b" ]; then
      run_extract_data
      break
    else
      echo "I didn't get it, sorry."
    fi
  else
    run_extract_data
done
