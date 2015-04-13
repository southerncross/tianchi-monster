import csv

wf = open("merge_feat.csv", 'wb')
wp = csv.writer(wf)
wf1 = open("merge_feat_user_item.csv", 'wb')
wp1 = csv.writer(wf1)

date = 15
feats = ("feature%d_1.csv"%date, "feature%d_2.csv"%date, "feature%d_5.csv"%date)

ui_cart = {}

for i in range(0, len(feats)):
    print i
    fp = open(feats[i], 'r')
    for line in fp:
        (ui, ii, f1, f2, f3, f4) = line.split(',')
        if (ui, ii) not in ui_cart:
            ui_cart[(ui, ii)] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        ui_cart[(ui, ii)][i*4 + 1] = f1
        ui_cart[(ui, ii)][i*4 + 2] = f2
        ui_cart[(ui, ii)][i*4 + 3] = f3
        ui_cart[(ui, ii)][i*4 + 4] = f4
fp = open("feature%d_tag.csv"%date, 'r')
for line in fp:
    (ui, ii, tag) = line.split(',')
    if (ui, ii) not in ui_cart:
        ui_cart[(ui, ii)] = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    ui_cart[(ui, ii)][0] = tag
        
for (k, v) in ui_cart.iteritems():
    wp1.writerow((k[0], k[1]))
    wp.writerow(tuple(v))