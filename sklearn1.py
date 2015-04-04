import numpy as np
import csv
from sklearn import linear_model

feat_data = np.loadtxt('feat1.csv', delimiter=',')
feat_new = np.loadtxt('feat_new.csv', delimiter=',')
reswriter = csv.writer(open("pred_res.csv", "wb"))

print 'load finished'

logistic = linear_model.LogisticRegression()
print feat_data[:, 2]
logistic.fit(feat_data[:, 3:], feat_data[:, 2])
res = logistic.predict(feat_new[:, 3:])

for i in range(len(res)):
    reswriter.writerow((feat_new[i][0], feat_new[i][1], res[i]))