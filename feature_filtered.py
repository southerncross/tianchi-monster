import time as s_time
import csv
import sys
import os
from sets import Set

date_table = {'2014-11-18 0': 1416240000.0, '2014-11-19 0': 1416326400.0, '2014-11-20 0': 1416412800.0, '2014-11-21 0': 1416499200.0, '2014-11-22 0': 1416585600.0, '2014-11-23 0': 1416672000.0, '2014-11-24 0': 1416758400.0, '2014-11-25 0': 1416844800.0, '2014-11-26 0': 1416931200.0, '2014-11-27 0': 1417017600.0, '2014-11-28 0': 141714000.0, '2014-11-29 0': 1417190400.0, '2014-11-30 0': 1417276800.0, '2014-12-01 0': 1417363200.0, '2014-12-02 0': 1417449600.0, '2014-12-03 0': 1417536000.0, '2014-12-04 0': 1417622400.0, '2014-12-05 0': 1417708800.0, '2014-12-06 0': 1417795200.0, '2014-12-07 0': 1417881600.0, '2014-12-08 0': 1417968000.0, '2014-12-09 0': 1418054400.0, '2014-12-1 0': 1418140800.0, '2014-12-11 0': 1418227200.0, '2014-12-12 0': 1418313600.0, '2014-12-13 0': 1418400000.0, '2014-12-14 0': 1418486400.0, '2014-12-15 0': 1418572800.0, '2014-12-16 0': 1418659200.0, '2014-12-17 0': 1418745600.0, '2014-12-18 0': 1418832000.0, '2014-12-19 0': 1418918400.0}
one_day = 86400

# label_day: start of the label day
label_day = "2014-12-%02d 0" % int(sys.argv[1])
label_date_s = date_table[label_day]
label_date_e = label_date_s + one_day
day_before_2 = label_date_s - one_day * 2
day_before_5 = label_date_s - one_day * 5
day_before_1 = label_date_s - one_day * 1

# read items that are in the set
item_set = Set()
item_set_file = open("tianchi_mobile_recommend_train_item.csv", 'r')
item_set_file.readline()
for line in item_set_file:
    (ii, geo, ci) = line.split(',')
    item_set.add(ii)

fp = open("tianchi_mobile_recommend_train_user.csv", 'r')
wf = open(label_day+"_feat.csv", 'wb')
wp = csv.writer(wf)
wf1 = open(label_day+"_feat_user_item.csv", 'wb')
wp1 = csv.writer(wf1)

ui_cart = {}
fp.readline()
count = 0
for line in fp:
    count += 1
    if count % 10000 == 0:
        print count
    (ui, ii, bt, ug, ca, ti) = line.split(',')
    if ii not in item_set:
        continue
    # init feature set.
    if (ui, ii) not in ui_cart:
        ui_cart[(ui, ii)] = [0, 0, 0, 0, 0]
    i_time = s_time.mktime(s_time.strptime(ti.strip(), '%Y-%m-%d %H'))
    # bought on label_day, used as label
    if bt == '4' and label_date_s <= i_time < label_date_e:
        ui_cart[(ui, ii)][0] += 1
    if i_time < label_date_s:
        # viewed within 1 days
        if bt == '1' and day_before_1 <= i_time:
            ui_cart[(ui, ii)][1] += 1
        if bt == '2' and day_before_1 <= i_time:
            ui_cart[(ui, ii)][2] += 1
        if bt == '3' and day_before_1 <= i_time:
            ui_cart[(ui, ii)][3] += 1
        if bt == '4' and day_before_1 <= i_time:
            ui_cart[(ui, ii)][4] += 1
        # viewed within 2 days
        if bt == '1' and day_before_2 <= i_time:
            ui_cart[(ui, ii)][5] += 1
        if bt == '2' and day_before_2 <= i_time:
            ui_cart[(ui, ii)][6] += 1
        if bt == '3' and day_before_2 <= i_time:
            ui_cart[(ui, ii)][7] += 1
        if bt == '4' and day_before_2 <= i_time:
            ui_cart[(ui, ii)][8] += 1
        # viewed within 5 days
        if bt == '1' and day_before_5 <= i_time:
            ui_cart[(ui, ii)][9] += 1
        if bt == '2' and day_before_5 <= i_time:
            ui_cart[(ui, ii)][10] += 1
        if bt == '3' and day_before_5 <= i_time:
            ui_cart[(ui, ii)][11] += 1
        if bt == '4' and day_before_5 <= i_time:
            ui_cart[(ui, ii)][12] += 1

for (k, v) in ui_cart.iteritems():
    if sum(v) > 0:
        wp1.writerow((k[0], k[1]))
        wp.writerow((k[0], k[1]) + tuple(v))

wf.close()