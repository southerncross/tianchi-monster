import csv
import sys

file1 = 'naive_method_2_2.csv'
file2 = 'naive_method_1_2.csv'

feat1 = {}
f = open(file1, 'r')
for line in f:
    (ui, ii) = line.strip().split(',')
    feat1[(ui, ii)] = 1
f.close()
print len(feat1)

alll = 0
count = 0
f = open(file2, 'r')
for line in f:
    (ui, ii) = line.strip().split(',')
    if (ui, ii) in feat1:
        count += 1
    alll += 1
f.close()

print alll
print count

    