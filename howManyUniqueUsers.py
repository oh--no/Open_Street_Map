# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
"""
Your task is to explore the data a bit more.
The first task is a fun one - find out how many unique users
have contributed to the map in this particular area!

The function process_map should return a set of unique user IDs ("uid")
"""

def get_user(element):
    uid = ''
    if 'uid' in element.attrib.keys() and 'uid' != '':
        uid = element.attrib['uid']
    else:
        pass
    return uid


def process_map(filename):
    users = set()
    counter = 0
    for _, element in ET.iterparse(filename):
        #print(users)
        if 'uid' in element.attrib.keys():
            users.add(get_user(element))
            counter += 1
            print(users,counter)
            #pass
    return users


def test():

    users = process_map('example.osm')
    pprint.pprint(users)
    assert len(users) == 6



if __name__ == "__main__":
    test()