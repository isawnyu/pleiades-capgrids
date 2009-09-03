import csv
import os

alphanums = 'abcdefghijklmn'
scales = {'5000': 5.0, '1000': 1.0, '500': 0.5, '150': 0.25}
f = open(os.path.join(os.path.dirname(__file__), 'maps.csv'))
r = csv.reader(f)

data = dict([(rec[0], rec[:]) for rec in list(r)[1:]])

def box(mapid, gridsquare):
    rec = data[mapid]
    bbox = [float(rec[3]), float(rec[5]), float(rec[4]), float(rec[6])]
    cols = [alphanums[i] for i in range(alphanums.index(rec[7].lower()), alphanums.index(rec[8].lower())+1)] 
    rows = [k for k in range(int(rec[9]), int(rec[10])+1)]
    m, n = len(cols), len(rows)
    dx, dy = (bbox[2] - bbox[0])/m, (bbox[3] - bbox[1])/n
    col = gridsquare[0].lower()
    row = int(gridsquare[1:])
    i = cols.index(col)
    j = rows.index(row)
    minx = bbox[0] + i*dx
    maxy = bbox[3] - j*dy
    return (minx, maxy-dy, minx+dx, maxy)