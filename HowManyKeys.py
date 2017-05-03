# -*- coding=utf-8 -*-
import xml.etree.cElementTree as ET


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
    return keys

keys = findKeys(infile)
# sort the values in descend order.
sortedKeys = sorted(keys.items(),key = lambda item:item[1],reverse = True)
print sortedKeys

with open(outfile,'wb') as output:
    for keys in sortedKeys:
        output.write(str(keys))


