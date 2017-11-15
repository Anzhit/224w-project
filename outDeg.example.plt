#
# Directed graph - out-degree Distribution. G(216966, 1852847). 14892 (0.0686) nodes with out-deg > avg deg (17.1), 0 (0.0000) with >2*avg.deg (Tue Nov 14 17:31:37 2017)
#

set title "Directed graph - out-degree Distribution. G(216966, 1852847). 14892 (0.0686) nodes with out-deg > avg deg (17.1), 0 (0.0000) with >2*avg.deg"
set key bottom right
set logscale xy 10
set format x "10^{%L}"
set mxtics 10
set format y "10^{%L}"
set mytics 10
set grid
set xlabel "Out-degree"
set ylabel "Count"
set tics scale 2
set terminal png font arial 10 size 1000,800
set output 'outDeg.example.png'
plot 	"outDeg.example.tab" using 1:2 title "" with linespoints pt 6
