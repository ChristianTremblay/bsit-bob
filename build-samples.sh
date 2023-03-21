#!/bin/bash

#
#  Build the samples
#

# usage information
if [ "$#" == "0" ] ; then
cat << EOF
usage: ./build-samples.sh [-p] [-s] [-q]
    -p         prompt for each sample
    -s         spawn each command then wait for children
    -q         quiet
EOF
exit
fi

# default values for options
PROMPT=""
GO="y"
SPAWN=""
QUIET=""

# get the options
while getopts psq OPTION
do
    case $OPTION in
        p)
            PROMPT=1
            GO=""
            ;;
        s)
            SPAWN=1
            ;;
        q)
            QUIET=1
            ;;
    esac
done
shift $((OPTIND-1))

# loop through the samples
for sample in samples/sample*.py
do
    if [ -n "$PROMPT" ] ; then
        read -p "$sample (y/n/x)? " GO
        if [ "$GO" = "x" ] ; then
            exit
        fi
    else
        if [ -z "$QUIET" ] ; then
            echo -en '\033[1;35m-----' $sample '-----\033[0m\n'
            echo python3 $sample "$@"
        fi
    fi
    if [ "$GO" = "y" ] ; then
        if [ -n "$SPAWN" ] ; then
            python3 $sample "$@" &
            if [ -z "$QUIET" ] ; then
                echo $sample process: $!
            fi
        else
            python3 $sample "$@"
        fi
    fi
    if [ -z "$QUIET" ] ; then
        echo
    fi
done
if [ "$SPAWN" != "" ] ; then
    if [ -z "$QUIET" ] ; then
        echo "Waiting for children..."
    fi
    wait
fi
