# -*- coding: utf-8 -*-
import xml.etree.cElementTree as ET
import pprint
import re
import codecs
import json

"""
Your task is to wrangle the data and transform the shape of the data
into the model we mentioned earlier. The output should be a list of dictionaries
that look like this:

{
"id": "2406124091",
"type: "node",
"visible":"true",
"created": {
          "version":"2",
          "changeset":"17206049",
          "timestamp":"2013-08-03T16:43:42Z",
          "user":"linuxUser16",
          "uid":"1219059"
        },
"pos": [41.9757030, -87.6921867],
"address": {
          "housenumber": "5157",
          "postcode": "60625",
          "street": "North Lincoln Ave"
        },
"amenity": "restaurant",
"cuisine": "mexican",
"name": "La Cabana De Don Luis",
"phone": "1 (773)-271-5176"
}

You have to complete the function 'shape_element'.
We have provided a function that will parse the map file, and call the function with the element
as an argument. You should return a dictionary, containing the shaped data for that element.
We have also provided a way to save the data in a file, so that you could use
mongoimport later on to import the shaped data into MongoDB. 

Note that in this exercise we do not use the 'update street name' procedures
you worked on in the previous exercise. If you are using this code in your final
project, you are strongly encouraged to use the code from previous exercise to 
update the street names before you save them to JSON. 

In particular the following things should be done:
- you should process only 2 types of top level tags: "node" and "way"
- all attributes of "node" and "way" should be turned into regular key/value pairs, except:
    - attributes in the CREATED array should be added under a key "created"
    - attributes for latitude and longitude should be added to a "pos" array,
      for use in geospacial indexing. Make sure the values inside "pos" array are floats
      and not strings. 
- if the second level tag "k" value contains problematic characters, it should be ignored
- if the second level tag "k" value starts with "addr:", it should be added to a dictionary "address"
- if the second level tag "k" value does not start with "addr:", but contains ":", you can
  process it in a way that you feel is best. For example, you might split it into a two-level
  dictionary like with "addr:", or otherwise convert the ":" to create a valid key.
- if there is a second ":" that separates the type/direction of a street,
  the tag should be ignored, for example:

<tag k="addr:housenumber" v="5158"/>
<tag k="addr:street" v="North Lincoln Avenue"/>
<tag k="addr:street:name" v="Lincoln"/>
<tag k="addr:street:prefix" v="North"/>
<tag k="addr:street:type" v="Avenue"/>
<tag k="amenity" v="pharmacy"/>

  should be turned into:

{...
"address": {
    "housenumber": 5158,
    "street": "North Lincoln Avenue"
}
"amenity": "pharmacy",
...
}

- for "way" specifically:

  <nd ref="305896090"/>
  <nd ref="1719825889"/>

should be turned into
"node_refs": ["305896090", "1719825889"]
"""

lower = re.compile(r'^([a-z]|_)*$')
lower_colon = re.compile(r'^([a-z]|_)*:([a-z]|_)*$')
problemchars = re.compile(r'[=\+/&<>;\'"\?%#$@\,\. \t\r\n]')
postcode_re = re.compile(r'\b\d{4}')
street_types_re = re.compile(r'\b\S+\.?$',re.IGNORECASE)

CREATED = ["version", "changeset", "timestamp", "user", "uid"]
fix_mapping = {
    'St':'Street',
    'st':'Street',
    'street':'Street',
    'Street)':'Street',
    'Rd':'Road',
    'Boulevarde':'Boulevard',
    'Wollit':'Wolli'
}

# if the street type in the street name is wrong, then fix it according to the fix mapping.
def fix_street_name(street_name, fix_mapping):
    street_type = street_types_re.search(street_name).group()
    if street_type in fix_mapping:
        street_name = street_name.replace(street_type,fix_mapping[street_type])
    return street_name

# shape the element in a more logical way. put the attributes of same kind together.
def shape_element(element):
    node = {}
    created_dict = {}
    address = {}
    node_refs = []
    if element.tag == "node" or element.tag == "way": # gather the creation information together.
        for attribute in element.attrib:
            if attribute in CREATED:
                created_dict[attribute] = element.attrib[attribute]
            elif attribute not in ['lat', 'lon']:
                node[attribute] = element.attrib[attribute]
        if set(['lat', 'lon']).issubset(element.attrib): # put the latitude and longitude together.
            pos = [float(element.attrib['lat']), float(element.attrib['lon'])]
            node['pos'] = pos
        node['created'] = created_dict
        node['type'] = element.tag

        for tag in element.iter('tag'):
            # ignore the attributes with more than 1 colon.
            if tag.attrib['k'].count(':') > 1 or problemchars.search(tag.attrib['k']):
                continue
            elif tag.attrib['k'].find('addr:') == 0:
                if 'city' in tag.attrib['k']:
                    address['city'] = tag.attrib['v']
                elif 'housenumber' in tag.attrib['k']:
                    address['housenumber'] = tag.attrib['v']
                # audit the postcode to ensure it has 4 digits.
                elif 'postcode' in tag.attrib['k'] and postcode_re.search(tag.attrib['v']):
                    address['postcode'] = postcode_re.search(tag.attrib['v']).group()
                # fix the street type if it is wrong.
                elif 'street' in tag.attrib['k'] and street_types_re.search(tag.attrib['v']):
                    address['street'] = fix_street_name(tag.attrib['v'],fix_mapping)
                node['address'] = address
            else:
                node[tag.attrib['k'].replace(':', '_')] = tag.attrib['v']
        for nd in element.iter('nd'):
            node_refs.append(nd.attrib['ref'])
        if node_refs != []:
            node['node_refs'] = node_refs
        return node
    else:
        return None


def process_map(file_in, pretty=False):
    file_out = "{0}.json".format(file_in)
    data = []
    with codecs.open(file_out, "w") as fo:
        for _, element in ET.iterparse(file_in):
            el = shape_element(element)
            if el:
                data.append(el)
                if pretty:
                    fo.write(json.dumps(el, indent=2) + "\n")
                else:
                    fo.write(json.dumps(el) + "\n")
    return data


def test():
    # NOTE: if you are running this code on your computer, with a larger dataset,
    # call the process_map procedure with pretty=False. The pretty=True option adds
    # additional spaces to the output, making it significantly larger.
    data = process_map('sydney.osm', False)
    pprint.pprint(data)



if __name__ == "__main__":
    test()