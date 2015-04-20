# -*- coding: utf-8 -*-
import csv
import sys

if len(sys.argv) < 2:
    print "Usage: verify_merge.py (date)"
    exit(0)

date = int(sys.argv[1])
feats = ("feature%d_1.csv"%date, "feature%d_2.csv"%date, "feature%d_5.csv"%date)

wf = open("veri_%d_feat.csv"%date, 'wb')
wp = csv.writer(wf)
wf1 = open("veri_%d_feat_user_item.csv"%date, 'wb')
wp1 = csv.writer(wf1)

# 提取特征
ui_cart = {}

for i in range(0, len(feats)):
    print i
    fp = open(feats[i], 'r')
    for line in fp:
        (ui, ii, f1, f2, f3, f4) = line.strip().split(',')
        if (ui, ii) not in ui_cart:
            ui_cart[(ui, ii)] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ui_cart[(ui, ii)][i*4 + 1] = f1
        ui_cart[(ui, ii)][i*4 + 2] = f2
        ui_cart[(ui, ii)][i*4 + 3] = f3
        ui_cart[(ui, ii)][i*4 + 4] = f4
fp = open("feature%d_tag.csv"%date, 'r')
for line in fp:
    (ui, ii, tag) = line.strip().split(',')
    if (ui, ii) not in ui_cart:
        ui_cart[(ui, ii)] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ui_cart[(ui, ii)][0] = tag
        
for (k, v) in ui_cart.iteritems():
    wp1.writerow((k[0], k[1]))
    wp.writerow(tuple(v))