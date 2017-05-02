# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
# import json
# import pprint
# from pymongo import MongoClient


# client = MongoClient("mongodb://localhost:27017")
# db = client.sydney
infile = 'sydney.osm'
street_types_re = re.compile(r'\b\S+\.?$',re.IGNORECASE)
street_types = defaultdict(int)

def auditStreetTypes(street_types,street_name):
    r = street_types_re.search(street_name)
    if r:
        streetType = r.group()
        street_types[streetType] += 1

def printSortedDict(d):
    keys = d.keys()
    keys = sorted(keys,key = lambda s:s.lower())
    for k in keys:
        print '%s:%d'%(k,d[k])

def isStreet(elem):
    if elem.tag == 'tag' and elem.attrib['k'] == 'addr:street':
        return True

def audit():
    for _,element in ET.iterparse(infile):
        if isStreet(element):
            auditStreetTypes(street_types,element.attrib['v'])
    printSortedDict(street_types)


# def audit_mongodb():
#     results = db.sydney.aggregate([
#         {'$match':{'address.street':{'$exists':1}}},
#         {'$group':{'_id':'$address.street',
#                     'count':{'$sum':1}}},
#         {'$sort':{'count':-1}}
#     ])
#     for result in results:
#         print result
#         print 1


if __name__ == '__main__':
    audit()


