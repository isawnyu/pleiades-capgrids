import csv
from itertools import islice
import os

from zope.dublincore.interfaces import ICMFDublinCore
from zope.interface import implements
from zgeo.geographer.interfaces import IGeoreferenced


alphanums = 'abcdefghijklmn'
scales = {'5000': 5.0, '1000': 1.0, '500': 0.5, '150': 0.25}
f = open(os.path.join(os.path.dirname(__file__), 'maps.csv'))
reader = csv.reader(f)

# data = dict([(rec[0], rec[:]) for rec in list(r)[1:]])

data = {}
for r in islice(reader, 1, None):
    key = r[0]
    value = data.get(key, [])
    value.append(r)
    data[key] = value

def box(mapid, gridsquare):
    row = int(gridsquare[1:])
    col = gridsquare[0].lower()
    for rec in data[mapid]:
        assert rec[0] == mapid
        try:
            cols = [alphanums[i] for i in range(alphanums.index(rec[7].lower()), alphanums.index(rec[8].lower())+1)]
            rows = [k for k in range(int(rec[9]), int(rec[10])+1)]
            assert row in rows
            assert col in cols
            bbox = float(rec[3]), float(rec[5]), float(rec[4]), float(rec[6])
            dx = (bbox[2] - bbox[0])/len(cols)
            dy = (bbox[3] - bbox[1])/len(rows)
            minx = bbox[0] + cols.index(col)*dx
            maxy = bbox[3] - rows.index(row)*dy
            return (minx, maxy-dy, minx+dx, maxy)
        except AssertionError:
            pass
        except:
            raise
    raise IndexError, "No gridsquare %s in map %s" % (gridsquare, mapid)


class Grid(object):
    
    """Context for surfacing grid squares in KML, Atom, JSON
    """
    implements(ICMFDublinCore, IGeoreferenced)
    
    def __init__(self, mapid, gridsquare):
        self.mapid = mapid
        self.gridsquare = gridsquare
    
    @property
    def id(self):
        return 'http://atlantides.org/capgrids/%s/%s' % (self.mapid, self.gridsquare)
    
    @property
    def bounds(self):
        return box(self.mapid, self.gridsquare)
    
    def Title(self):
        return 'Barrington Atlas map %s, grid square %s' % (self.mapid, self.gridsquare)
    
    def Description(self):
        return 'Bounding polygon of Barrington Atlas map %s, grid square %s' % (self.mapid, self.gridsquare)
    
    def Creator(self):
        return 'Classical Atlas Project, edited by R. Talbert'
    
    @property
    def type(self):
        return 'Polygon'
    
    @property
    def coordinates(self):
        l, b, r, t = self.bounds
        return (((l, b), (l, t), (r, t), (r, b), (l, b)),)
    
    @property
    def __geo_interface__(self):
        return dict(type=self.type, coordinates=self.coordinates)
        