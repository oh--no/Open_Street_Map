# -*- coding=utf-8 -*-
import xml.etree.cElementTree as ET
from collections import defaultdict
import re
import pprint
import json

infile = 'sydney.osm'
outfile = 'HowManyKeys.txt'
# 找到所有tag的数量
def findKeys(infile):
    keys = {}
    root = ET.iterparse(infile,events = ('start',))
    for _,item in root:
        if 'k' in item.attrib:
            if item.attrib['k'] in keys:
                keys[item.attrib['k']] += 1
            else:
                keys[item.attrib['k']] = 1
        # for tag in item:
        #     if tag.attrib['k'] in keys:
        #         keys[tag.attrib['k']] += 1
        #     else:
        #         keys[tag.attrib['k']] = 1
    return keys

keys = findKeys(infile)
sortedKeys = sorted(keys.items(),key = lambda item:item[1],reverse = True)
print sortedKeys
# pprint.pprint(keys)
# jsonDict = json.dumps(keys)
#
with open(outfile,'wb') as output:
    for keys in sortedKeys:
        output.write(str(keys))


