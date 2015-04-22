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
hit = 0
positive = 0
true_pos = 0
for i in range(len(res)):
    count += 1
    if res[i] != 0 and feat_new[i, 0] != 0:
        hit += 1
    if res[i] != 0:
        positive += 1
    if feat_new[i, 0] != 0:
        true_pos += 1
precision = float(hit)/positive
recall = float(hit)/true_pos
f1 = 2 * precision * recall / (precision + recall)
print "count=%d, hit=%d, pos=%d, true_pos=%d, precision=%f, recall=%f, f1=%f" % (count, hit, positive, true_pos, precision, recall, f1)

# count = 0
# for line in fr:
#     if res[count] != 0:
#         fw.write(line)
#     count += 1
# print count, len(res)