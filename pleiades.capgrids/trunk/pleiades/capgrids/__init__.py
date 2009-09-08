import csv
import os

from zope.dublincore.interfaces import ICMFDublinCore
from zope.interface import implements
from zgeo.geographer.interfaces import IGeoreferenced


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
        