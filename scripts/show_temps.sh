#!/bin/bash

cd

N=${1:-3600}

echo "Showing $N last CPU temperature records."
tail -n $N logs/temp_history.log > logs/temp_history_tail.dat


gnuplot -persist scripts/plot_temps.plt



