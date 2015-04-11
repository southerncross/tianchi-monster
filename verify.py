import numpy as np
import csv
from sklearn import linear_model

feat_data = np.loadtxt('2014-12-02 0_feat.csv', delimiter=',', dtype=np.int8)
feat_new = np.loadtxt('2014-12-18 0_feat.csv', delimiter=',', dtype=np.int8)
reswriter = csv.writer(open("pred_res.csv", "wb"))

print 'load finished'

logistic = linear_model.LogisticRegression()
logistic.fit(feat_data[:, 1:], feat_data[:, 0])
print 'Fit finished'
print logistic.score(feat_new[:, 1:], feat_new[:, 0])
print 'Score finished'
res = logistic.predict(feat_new[:, 1:])
print 'Predict finished'

count = 0
hit = 0
positive = 0
d_pos = 0
for i in range(len(res)):
    count += 1
    if count % 100000 == 0:
        print count
    if res[i] == feat_new[i, 0]:
        hit += 1
    if res[i] != 0:
        positive += 1
    if feat_new[i, 0] != 0:
        d_pos += 1
    reswriter.writerow((res[i]) + tuple(feat_new[i, :]))
    
print "count=%d, hit=%d, pos=%d, d_pos=%d" % (count, hit, positive, d_pos)