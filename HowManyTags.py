# -*- coding=utf-8 -*-
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import json

infile = 'sample.osm'
outfile = 'HowManyTags.txt'
# 找到所有tag的数量
def findTags(infile):
    tags = {}
    root = ET.iterparse(infile,events = ('start',))
    for _,item in root:
        if item.tag in tags:
            tags[item.tag] += 1
        else:
            tags[item.tag] = 1
    return tags

tags = findTags(infile)
pprint.pprint(tags)
jsonDict = json.dumps(tags)

with open(outfile,'wb') as output:
    output.write(jsonDict)


