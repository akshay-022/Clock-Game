#!/bin/bash

if [[ $1 == "True" ]] ; then
<<<<<<< HEAD
	python clock_game.py -ng $1 -s $2
else
	python clock_gui.py -s $2 &
	sleep 1
	python clock_game.py -s $2 &
=======
    python clock_game.py -ng $1 -s $2
else
    python clock_gui.py -s $2 &
    sleep 1
    python clock_game.py -s $2 &
>>>>>>> 57424c6858998b97c5dfa2aa2ce1cb92284f1e1b
fi