#!/bin/bash

if [[ $1 == "True" ]] ; then
    python3 clock_game.py -ng True
else
    python3 clock_gui.py &
    sleep 1
    python3 clock_game.py &
fi