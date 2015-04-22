import sys
import csv

dates = range(22, 33)
for idate in dates:
	filename = "E:/tianchi_feature_filtered/hotness/hotness_user_%d.csv" % idate
	offset = 1

	feat_store = []
	with open(filename, 'r') as f:
		line = f.readline()
		items = map(lambda x:float(x), line.strip().split(','))
		feat_store.append(items)
		feat_sum = items[offset:]
			
		for line in f:
			items = map(lambda x:float(x), line.strip().split(','))
			feat_store.append(items)
			feat_sum = [max(x,y) for x,y in zip(feat_sum, items[offset:])]
	print feat_sum

	wf = open(filename[:-4]+"_01.csv", 'wb')
	csvwf = csv.writer(wf)

	for items in feat_store:
		witems = items[:offset] + [("%.6f" % (float(x) / y)) if y != 0 else 0 for x,y in zip(items[offset:], feat_sum)]
		csvwf.writerow(tuple(witems))