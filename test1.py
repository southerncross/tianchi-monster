import csv

fp = open("2014-12-19 0_feat.csv", 'r')
wf = open("_predict.csv", 'wb')
wp = csv.writer(wf)


wp.writerow(('user_id', 'item_id'))
for line in fp:
    res = line.split(',')
    if res[5] != 0:
        wp.writerow((res[0], res[1]))