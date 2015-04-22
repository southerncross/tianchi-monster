# -*- coding: utf-8 -*-
import csv
import sys
import numpy as np
from sklearn import linear_model
from sklearn.ensemble import RandomForestClassifier
import math
import copy
from sets import Set

if len(sys.argv) < 3:
    print "Usage: merge.py (train_date) [...train_date] (predict date)"
    exit(0)

train_date_num = len(sys.argv) - 2


item_cate_map = {}
fp_item_cate_map = open("E:/tianchi_feature_filtered/tianchi_mobile_recommend_train_item.csv", 'r')
fp_item_cate_map.readline()
for line in fp_item_cate_map:
    (ii, geo, ci) = line.strip().split(',')
    item_cate_map[int(ii)] = int(ci)

user_habit = {}
fp_user_habit = open("E:/tianchi_feature_filtered/hotness/f_user_full.csv", 'r')
for line in fp_user_habit:
    habits = map(lambda x:float(x), line.strip().split(','))
    user_habit[habits[0]] = habits[1:]


def load_raw_feature(date):
    print "dealing date %d" % date
    # how many days of features to be involved
    feat_opes_range = (1,2)
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
    print ""

    # tag提取
    #print "\ndealing tag"
    fp = open("E:/tianchi_feature_filtered/tag_limit_%d.csv"%date, 'r')
    for line in fp:
        (ui, ii, tag) = map(lambda x:int(x), line.strip().split(','))
        if (ui, ii) in ui_feature:
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
    #print "balancing positive and negetive data"
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
    #print pos_count, neg_count, pos_count + neg_count
    return copy.deepcopy(ret_feature)

def add_global_feature(ui_feature, date):
    #print "adding global features of date %d" % date
    item_hotness = {}
    user_behavior = {}
    cate_hotness = {}
    fp_item_hotness = open("E:/tianchi_feature_filtered/hotness/hotness_item_%d.csv" % date, 'r')
    for line in fp_item_hotness:
        (ii, f_all, h1, h2, h3, h4) = map(lambda x:float(x), line.strip().split(','))
        item_hotness[ii] = [h1, h2, h3, h4]
    fp_user_behavior = open("E:/tianchi_feature_filtered/hotness/hotness_user_%d.csv" % date, 'r')
    for line in fp_user_behavior:
        (ui, f_all, h1, h2, h3, h4) = map(lambda x:float(x), line.strip().split(','))
        user_behavior[ui] = [h1, h2, h3, h4]
    fp_cate_hotness = open("E:/tianchi_feature_filtered/hotness/hotness_category_%d.csv" % date, 'r')
    for line in fp_cate_hotness:
        (ci, f_all, h1, h2, h3, h4) = map(lambda x:float(x), line.strip().split(','))
        cate_hotness[ci] = [h1, h2, h3, h4]
    for k in ui_feature:
        v = ui_feature[k]
        v += user_behavior[k[0]] if k[0] in user_behavior else [0,0,0,0]
        v += item_hotness[k[1]] if k[1] in item_hotness else [0,0,0,0]
        v += cate_hotness[item_cate_map[k[1]]] if k[1] in item_cate_map and item_cate_map[k[1]] in cate_hotness else [0,0,0,0]
        v += user_habit[k[0]]

def add_u_i_feature(ui_feature, date):
    return
    """user item features from shun, 7 dimensions
    """
    curr_feat = {}
    fp_u_i_feature = open("E:/tianchi_feature_filtered/hotness/user_item_%d.csv" % date, 'r')
    for line in fp_u_i_feature:
        feat_items = map(lambda x:float(x), line.strip().split(','))
        curr_feat[tuple(feat_items[:2])] = feat_items[6:]
    for k in ui_feature:
        v = ui_feature[k]
        v += curr_feat[k]

def delete_yesterday_buy(ui_pre, res, date):
    print "delete bought items yesterday"
    # 加载昨天购买的信息
    yes_buy = Set()
    with open("E:/tianchi_feature_filtered/tag_limit_%d.csv"%(date-1), 'r') as yes_fp:
        for line in yes_fp:
            (ui, ii, tag) = map(lambda x:int(x), line.strip().split(','))
            if (ui, ii) not in yes_buy:
                yes_buy.add((ui, ii))
    with open("E:/tianchi_feature_filtered/tag_limit_%d.csv"%(date-2), 'r') as yes_fp:
        for line in yes_fp:
            (ui, ii, tag) = map(lambda x:int(x), line.strip().split(','))
            if (ui, ii) not in yes_buy:
                yes_buy.add((ui, ii))
    for i in range(len(res)):
        if ui_pre[i] in yes_buy:
            res[i] = 0



# 加载多天的数据
print "load train features of dates: ", sys.argv[1:train_date_num+1]
ui_train = []
feat_train = []
for di in range(1, train_date_num+1):
    date1 = int(sys.argv[di])
    # "deal with day %d" % date1
    ui_raw_feat_train = load_raw_feature(date1)
    ui_feat_train = balance_pos_neg(ui_raw_feat_train, 12)
    add_global_feature(ui_feat_train, date1)
    add_u_i_feature(ui_feat_train, date1)

    for k in ui_feat_train:
        ui_train.append(list(k))
        feat_train.append(ui_feat_train[k])

print "load finished with entries: ", len(ui_train), len(feat_train)
feat_data = np.array(feat_train)

print "feat dimension: ", len(feat_data[0,1:])
logistic = linear_model.LogisticRegression(penalty='l1')
#logistic = RandomForestClassifier(n_estimators=8, random_state=1)
logistic.fit(feat_data[:, 1:], feat_data[:, 0])
print 'Fit finished'

# "deal with day %d" % date2
date2 = int(sys.argv[-1])
ui_feat_pre = load_raw_feature(date2)
add_global_feature(ui_feat_pre, date2)
add_u_i_feature(ui_feat_pre, date2)

print "One entry of date %d for verification" % date2
for k in ui_feat_pre:
    print k, ui_feat_pre[k]
    break

ui_pre = []
feat_pre = []
for k in ui_feat_pre:
    ui_pre.append(k)
    feat_pre.append(ui_feat_pre[k])
feat_new = np.array(feat_pre)
print len(feat_new)

res = logistic.predict(feat_new[:, 1:])
print 'Predict finished'

# 剔除昨天刚刚购买过的数据
delete_yesterday_buy(ui_pre, res, date2)

if sys.argv[-1] != '32':
    # 加载真实结果集
    pos_set = Set()
    with open("E:/tianchi_feature_filtered/tag_limit_%d.csv"%date2, 'r') as pos_fp:
        for line in pos_fp:
            (ui, ii, tag) = map(lambda x:int(x), line.strip().split(','))
            if (ui, ii) not in pos_set:
                pos_set.add((ui, ii))
    count = 0
    hit = 0
    positive = 0
    true_pos = len(pos_set)
    for i in range(len(res)):
        count += 1
        if res[i] != 0 and ui_pre[i] in pos_set:
            hit += 1
        if res[i] != 0:
            positive += 1
    precision = float(hit)/positive
    recf_all = float(hit)/true_pos
    f1 = 2 * precision * recf_all / (precision + recf_all)
    print "count=%d, hit=%d, pos=%d, true_pos=%d, precision=%f, recf_all=%f, f1=%f" % (count, hit, positive, true_pos, precision, recf_all, f1)
else:
    fw = open("pred_res.csv", "wb")
    csvw = csv.writer(fw)
    count = 0
    for k in ui_pre:
        if res[count] != 0:
            csvw.writerow(k)
        count += 1