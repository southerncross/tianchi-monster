import csv
import sys
import random

if len(sys.argv) < 2:
	print "usage: .py infile outfile rate"

ifile = open(sys.argv[1], 'r')
ofile = open(sys.argv[2], 'w')

rate = float(sys.argv[3])

for line in ifile:
	if random.random() <= rate:
		ofile.write(line)

ofile.close()
ifile.close()