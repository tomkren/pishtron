set xdata time
set timefmt '%Y-%m-%d %H:%M:%S'
plot '~/logs/temp_history_tail.dat' using 1:3 with lines
