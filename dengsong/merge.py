# -*- coding: utf-8 -*-
import csv
import sys

if len(sys.argv) < 3:
    print "Usage: merge.py (date) [date]"
    exit(0)

# 读取全局热度记录
item_hotness = {}
user_behavior = {}
cate_hotness = {}
item_cate_map = {}
fp_item_hotness = open("feature_item_hotness.csv", 'r')
for line in fp_item_hotness:
    (ii, all, h1, h2, h3, h4) = line.strip().split(',')
    item_hotness[ii] = [all, h1, h2, h3, h4]
fp_user_behavior = open("feature_user_behavior.csv", 'r')
for line in fp_user_behavior:
    (ui, all, h1, h2, h3, h4) = line.strip().split(',')
    user_behavior[ui] = [all, h1, h2, h3, h4]
fp_cate_hotness = open("feature_item_category_hotness.csv", 'r')
for line in fp_cate_hotness:
    (ci, all, h1, h2, h3, h4) = line.strip().split(',')
    cate_hotness[ci] = [all, h1, h2, h3, h4]
fp_item_cate_map = open("tianchi_mobile_recommend_train_item.csv", 'r')
for line in fp_item_cate_map:
    (ii, geo, ci) = line.strip().split(',')
    item_cate_map[ii] = ci
print "pre load finished"

# 按固定日期merge， 或日期范围merge
date1 = int(sys.argv[1])
if len(sys.argv) == 2:
    date2 = date1
else:
    date2 = int(sys.argv[2])

for date in range(date1, date2+1):
    print "dealing date %d" % date
    feats = ("feature%d_1.csv"%date, "feature%d_2.csv"%date, "feature%d_5.csv"%date, "feature%d_7.csv"%date, "feature%d_14.csv"%date, "feature%d_21.csv"%date)
    feats = map(lambda s: "E:/tianchi_feature/"+s, feats)
    # feature 数目
    FEAT_SIZE = 24 + 1
    default_feat = [0] * FEAT_SIZE

    wf = open("E:/tianchi_feature/%d_feat.csv"%date, 'wb')
    wp = csv.writer(wf)
    wf1 = open("E:/tianchi_feature/%d_feat_user_item.csv"%date, 'wb')
    wp1 = csv.writer(wf1)


    ui_feature = {}
    # 特征提取
    for i in range(0, len(feats)):
        print "\r"+feats[i],
        sys.stdout.flush()
        fp = open(feats[i], 'r')
        for line in fp:
            (ui, ii, f1, f2, f3, f4) = line.strip().split(',')
            if (ui, ii) not in ui_feature:
                ui_feature[(ui, ii)] = default_feat
            ui_feature[(ui, ii)][i*4 + 1] = f1
            ui_feature[(ui, ii)][i*4 + 2] = f2
            ui_feature[(ui, ii)][i*4 + 3] = f3
            ui_feature[(ui, ii)][i*4 + 4] = f4
        fp.close()
    # tag提取
    print "\ndealing tag"
    fp = open("E:/tianchi_feature/tag%d.csv"%date, 'r')
    for line in fp:
        (ui, ii, tag) = line.strip().split(',')
        if (ui, ii) not in ui_feature:
            ui_feature[(ui, ii)] = default_feat
        # 如果买了就是1，不管买了多少
        ui_feature[(ui, ii)][0] = 1 if int(tag) != 0 else 0
    fp.close()
            
    print "writing back with item_num: ", len(ui_feature)
    pos_count = 0
    neg_count = 0
    for k in ui_feature:
        # 处理数据倾斜
        print "\r", pos_count+neg_count,
        sys.stdout.flush()
        v = ui_feature[k]
        if v[0] == 1:
            pos_count += 1
        elif v[0] == 0:
            if neg_count >= pos_count:
                continue
            neg_count += 1
        # 添加商品、用户相关的特征
        v += user_behavior[k[0]]
        v += item_hotness[k[1]]
        v += cate_hotness[item_cate_map[k[1]]] if k[1] in item_cate_map else [0,0,0,0,0]
        wp1.writerow((k[0], k[1]))
        wp.writerow(tuple(v))
    wf.close()
    wf1.close()

    print pos_count, neg_count, pos_count + neg_count