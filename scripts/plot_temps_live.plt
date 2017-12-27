bind "Close" "reread_loop = 0"
reread_loop = 1

set xdata time
set timefmt '%Y-%m-%d %H:%M:%S'
plot '~/logs/temp_history_tail.dat' using 1:3 with lines

pause 1

if (reread_loop == 1) reread
