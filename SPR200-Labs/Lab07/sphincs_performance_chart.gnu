set terminal png size 1400,900
set output 'sphincs_performance_chart.png'
set title 'File Signing Performance with Different Algorithms'
set style data histogram
set style fill solid 1.0 border -1
set boxwidth 0.8
set bmargin 8
set lmargin 10
set rmargin 10
set xtics rotate by -30 offset -1.5,-1
set key below
set ylabel "Time (seconds)"

# Define custom colors
set style line 1 lc rgb "#FF4444"  # Red
set style line 2 lc rgb "#44FF44"  # Green  
set style line 3 lc rgb "#4444FF"  # Blue

# Plot multiple columns with different colors
plot 'signing_performance.dat' using 2:xticlabels(1) title "KeyGen" ls 1, \
     'signing_performance.dat' using 3:xticlabels(1) title "Sign" ls 2, \
     'signing_performance.dat' using 4:xticlabels(1) title "Verify" ls 3
