#
# Directed graph - in-degree Distribution. G(216966, 1852847). 22918 (0.1056) nodes with in-deg > avg deg (17.1), 4417 (0.0204) with >2*avg.deg (Tue Nov 14 17:31:37 2017)
#

set title "Directed graph - in-degree Distribution. G(216966, 1852847). 22918 (0.1056) nodes with in-deg > avg deg (17.1), 4417 (0.0204) with >2*avg.deg"
set key bottom right
set logscale xy 10
set format x "10^{%L}"
set mxtics 10
set format y "10^{%L}"
set mytics 10
set grid
set xlabel "In-degree"
set ylabel "Count"
set tics scale 2
set terminal png font arial 10 size 1000,800
set output 'inDeg.example.png'
plot 	"inDeg.example.tab" using 1:2 title "" with linespoints pt 6
