import numpy as np
import csv
import sys
from sklearn import linear_model


print 'start'
item_rate={}
user_rate={}

fp_item_rate = open('item_1_4_rate.csv', 'r')
for line in fp_item_rate:
    (ii, type3, type4, rate) = line.strip().split(',')
    item_rate[ii] = [type3, rate]
fp_item_rate.close()

fp_user_rate = open('user_1_4_rate.csv', 'r')
for line in fp_user_rate:
    (ui, type3, type4, rate) = line.strip().split(',')
    user_rate[ui] = [type3, rate]
fp_user_rate.close()


test = 31

test_tag = {}
fp_tag = open('../tag_limit/tag_limit%d.csv'%test, 'r')
for line in fp_tag:
    (ui, ii, count) = line.strip().split(',')
    test_tag[(ui, ii)] = 1
fp_tag.close()

test_feature = []
test_label = []
test_feature_u = {}
test_feature_i = {}
max_recall = 0
fp = open('train3/naive_method_%d_1_2.csv'%test, 'r')
for line in fp:
    (ui, ii) = line.strip().split(',')
    cur = []
    cur += user_rate[ui]
    cur += item_rate[ii]
    test_feature.append(cur)
    test_label.append((ui, ii))
    test_feature_u[ui] = 1
    test_feature_i[ii] = 1
    if (ui, ii) in test_tag:
        max_recall += 1
fp.close()

pos_count = 0
neg_count = 0
feature = []
day = [5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18, 19, 20, 21, 22, 23, 24, 25, 26, 27, 28, 29, 30, 31]
for i in day:
    print 'train3/naive_method_%d_1_2.csv'%i
    if i >= test:
        break
    tag = {}
    fp_tag = open('../tag_limit/tag_limit%d.csv'%i, 'r')
    for line in fp_tag:
        (ui, ii, count) = line.strip().split(',')
        tag[(ui, ii)] = 1
    fp_tag.close()
    
    fp = open('train3/naive_method_%d_1_2.csv'%i, 'r')
    for line in fp:
        (ui, ii) = line.strip().split(',')
        cur = []
        cur += user_rate[ui]
        cur += item_rate[ii]
        cur.append(1 if (ui, ii) in tag else 0)
        # if cur[4] == 1:
        #     pos_count += 1
        # else:
        #     if neg_count >= pos_count:
        #         continue;
        #     neg_count += 1;
        # feature.append(cur)
        if(ui in test_feature_u or ii in test_feature_i):
            if cur[4] == 1:
                pos_count += 1
            else:
                if neg_count >= pos_count:
                    continue
                neg_count += 1
            feature.append(cur)
    fp.close()
    
print 'finish cal feature'
print 'begin regression'

feat = np.array(feature, dtype=float)
logistic = linear_model.LogisticRegression()
logistic.fit(feat[:,:4], feat[:,4])



test_feat = np.array(test_feature, dtype=float)
res = logistic.predict(test_feat[:,:4])


# reswriter = csv.writer(open("naive_method_1_2.csv", "wb"))
result = 0
find = 0
for i in range(len(res)):
    if res[i] == 1:
        result += 1
        # print test_label[i]
        # reswriter.writerow(test_label[i])
        if test_label[i] in test_tag:
            find += 1

print len(res)
print result
print max_recall
print find
        