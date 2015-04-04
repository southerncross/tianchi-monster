import time

dates = []
for i in range(18, 31):
    dates.append("2014-11-%02d 0" % i)
for i in range(1, 20):
    dates.append("2014-12-%02d 0" % i)
d2t = {}
for d in dates:
    d2t[d] = time.mktime(time.strptime(d, '%Y-%m-%d %H'))

print dates
for d in dates:
    print "'"+d+"':", str(d2t[d])+",",