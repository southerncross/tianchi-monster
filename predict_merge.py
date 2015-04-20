# -*- coding: utf-8 -*-
import csv
import sys
import numpy as np
from sklearn import linear_model
import copy

if len(sys.argv) < 3:
    print "Usage: merge.py (train_date) [...train_date] (predict date)"
    exit(0)

train_date_num = len(sys.argv) - 2


# 读取全局热度记录
print "preprocess: load global features"
item_hotness = {}
user_behavior = {}
cate_hotness = {}
item_cate_map = {}
fp_item_hotness = open("E:/tianchi_feature_filtered/feature_item_hotness.csv", 'r')
for line in fp_item_hotness:
    (ii, all, h1, h2, h3, h4) = map(lambda x:int(x), line.strip().split(','))
    item_hotness[ii] = [all, h1, h2, h3, h4]
fp_user_behavior = open("E:/tianchi_feature_filtered/feature_user_behavior.csv", 'r')
for line in fp_user_behavior:
    (ui, all, h1, h2, h3, h4) = map(lambda x:int(x), line.strip().split(','))
    user_behavior[ui] = [all, h1, h2, h3, h4]
fp_cate_hotness = open("E:/tianchi_feature_filtered/feature_item_category_hotness.csv", 'r')
for line in fp_cate_hotness:
    (ci, all, h1, h2, h3, h4) = map(lambda x:int(x), line.strip().split(','))
    cate_hotness[ci] = [all, h1, h2, h3, h4]
fp_item_cate_map = open("E:/tianchi_feature_filtered/tianchi_mobile_recommend_train_item.csv", 'r')
fp_item_cate_map.readline()
for line in fp_item_cate_map:
    (ii, geo, ci) = line.strip().split(',')
    item_cate_map[int(ii)] = int(ci)
print "pre load finished"


def load_raw_feature(date):
    print "dealing date %d" % date
    feat_opes_range = [1] # (1, 2, 5, 7, 14)
    feat_files = map(lambda r: "feature_limit_%d_%d.csv"%(date, r), feat_opes_range)
    feat_files = map(lambda s: "E:/tianchi_feature_filtered/"+s, feat_files)
    # feature 数目
    FEAT_SIZE = 4*len(feat_files) + 1
    default_feat = [0] * FEAT_SIZE

    # 特征提取
    ui_feature = {}
    for i in range(0, len(feat_files)):
        print "\r"+feat_files[i],
        sys.stdout.flush()
        fp = open(feat_files[i], 'r')
        for line in fp:
            (ui, ii, f1, f2, f3, f4) = map(lambda x:int(x), line.strip().split(','))
            if (ui, ii) not in ui_feature:
                ui_feature[(ui, ii)] = default_feat[:]
            ui_feature[(ui, ii)][i*4 + 1] = f1
            ui_feature[(ui, ii)][i*4 + 2] = f2
            ui_feature[(ui, ii)][i*4 + 3] = f3
            ui_feature[(ui, ii)][i*4 + 4] = f4
        fp.close()
    # tag提取
    print "\ndealing tag"
    fp = open("E:/tianchi_feature_filtered/tag_limit%d.csv"%date, 'r')
    for line in fp:
        (ui, ii, tag) = map(lambda x:int(x), line.strip().split(','))
        if (ui, ii) not in ui_feature:
            ui_feature[(ui, ii)] = default_feat[:]
        # 如果买了就是1，不管买了多少
        ui_feature[(ui, ii)][0] = 1 if tag != 0 else 0
    fp.close()
    return copy.deepcopy(ui_feature)
            
def balance_pos_neg(ui_feature, proportion = 1.0):
    """balance positive and negetive data
    Args:
        ui_feature: init data
        proportion: neg / pos
    """
    print "balancing positive and negetive data"
    pos_count = 0
    neg_count = 0
    
    ret_feature = {}
    for k in ui_feature:
        # 处理数据倾斜
        v = ui_feature[k]
        if v[0] == 1:
            pos_count += 1
        elif v[0] == 0:
            if neg_count >= pos_count * proportion:
                continue
            neg_count += 1
        ret_feature[k] = v
    print pos_count, neg_count, pos_count + neg_count
    return ret_feature

def add_global_feature(ui_feature):
    print "adding global features"
    for k in ui_feature:
        v = ui_feature[k]
        v += user_behavior[k[0]]
        v += item_hotness[k[1]]
        v += cate_hotness[item_cate_map[k[1]]] if k[1] in item_cate_map else [0,0,0,0,0]


# 加载多天的数据
print "load train features of dates: ", sys.argv[1:train_date_num+1]
ui_train = []
feat_train = []
for di in range(1, train_date_num+1):
    date1 = int(sys.argv[di])
    # "deal with day %d" % date1
    ui_raw_feat_train = load_raw_feature(date1)
    ui_feat_train = balance_pos_neg(ui_raw_feat_train, 10)
    add_global_feature(ui_feat_train)

    for k in ui_feat_train:
        ui_train.append(list(k))
        feat_train.append(ui_feat_train[k])

print "load finished with entries: ", len(ui_train), len(feat_train)
feat_data = np.array(feat_train)

# "deal with day %d" % date2
date2 = int(sys.argv[-1])
ui_feat_pre = load_raw_feature(date2)
add_global_feature(ui_feat_pre)

ui_pre = []
feat_pre = []
for k in ui_feat_pre:
    ui_pre.append(k)
    feat_pre.append(ui_feat_pre[k])
feat_new = np.array(feat_pre)

# print ui_train[0], feat_data[0,:]
# print ui_pre[0], feat_new[0,:]

logistic = linear_model.LogisticRegression(penalty='l1')
logistic.fit(feat_data[:, 1:], feat_data[:, 0])
print 'Fit finished'
res = logistic.predict(feat_new[:, 1:])
print 'Predict finished'

if sys.argv[-1] != 32:
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

fw = open("pred_res.csv", "wb")
csvw = csv.writer(fw)
count = 0
for k in ui_pre:
    if res[count] != 0:
        csvw.writerow(k)
    count += 1