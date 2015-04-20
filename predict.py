import numpy as np
import csv
import sys
from sklearn import linear_model

if len(sys.argv) < 4:
    print "Usage: verify.py (*.csv) (*.csv) (ui.csv)"
    exit(0)

feat_data = np.loadtxt(sys.argv[1], delimiter=',', dtype=np.int16)
feat_new = np.loadtxt(sys.argv[2], delimiter=',', dtype=np.int16)
fr = open(sys.argv[3], 'r')
fw = open("pred_res.csv", "wb")

print 'load finished'

logistic = linear_model.LogisticRegression()
logistic.fit(feat_data[:, 1:], feat_data[:, 0])
print 'Fit finished'
res = logistic.predict(feat_new[:, 1:])
print 'Predict finished'

count = 0
for line in fr:
    if res[count] != 0:
        fw.write(line)
    count += 1
print count, len(res)