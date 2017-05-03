# Open Street Map Project

map area : Sydney Australia

https://mapzen.com/data/metro-extracts/your-extracts/b050d5b5a0c7

My initial idea was to analyse the map of Shanghai, but apprently there are not many OSM users here so the data were not big enough for this project. Syendy is a city I have lived for a period of time which made it interesting for me to explore the city again in a special way.

I firstly audited the osm file and converted it into .json file(see audit_street.py and cleaning_data.py). Then I imported the .json file into mongodb for further auditing and analysis. Importing command:

> mongoimport --db sydney --collection sydney --file sydney.osm.json

## Problems encontered in the Map
There were two main problems in the dataset. One is the overabbreviated or even wrong street type, another is the wrong postcode. These problems were caused by inevitable human error and need to be fixed before the data being loaded to the database.
### Overabbreviated/wrong street type
The first problem I found was the street types. Some street types are full names such as "Street" and "Road" while others are abbreviated like "St", "Rd". Sometimes it can also be wrong such as "Street)".

Boulevard - boulevarde

Road - Rd

St - St. - street - Street - Street)

Wolli - Wollit

Code used to audit:
please see audit_street.py

Code used to fix:
```python
fix_mapping = {
    'St':'Street',
    'st':'Street',
    'street':'Street',
    'Street)':'Street',
    'Rd':'Road',
    'Boulevarde':'Boulevard',
    'Wollit':'Wolli'
}

def fix_street_name(street_name, fix_mapping):
    street_type = street_types_re.search(street_name).group()
    if street_type in fix_mapping:
        street_name = street_name.replace(street_type,fix_mapping[street_type])
    return street_name
...
```

### Postcode - excessive part / wrong postcode
The post code should have only 4 digits, but some postcodes have excessive "NSW", or only have 3 digits.

should be:
2205

abnormal values:
NSW 2010,
NSW 2000,
200,
210

Code used to select:
```python
def audit_postcode():
    result = db.sydney.aggregate([
        {'$match':{'address.postcode':{'$exists':1}}},
        {'$group': {'_id': '$address.postcode',
                    'count': {'$sum': 1}}},
        {'$sort': {'count': -1}}
    ])
    return result
```
Code used to clean the data:
```python
import re
re_postcode = re.compile(r'\b\d{4}')
...
elif 'postcode' in tag.attrib['k'] and re_postcode.search(tag.attrib['v']):
     address['postcode'] = re_postcode.search(tag.attrib['v']).group()
...
```

## Data Overview:
This section provides some basic ideas of the dataset including the data sizes, unique users and so on. Maybe because of the lack of popularity, there were not many data points in Sydney so I had to extract data from a very large area to get enough data for this project and that is why the data files are not very large.
### Sizes of the data files
Sydney.osm --- 79.2M

Sydney.osm.json --- 86.9M
### Number of documents
> db.sydney.find().count()
389955
### Number of nodes
> db.sydney.find({'type':'node'}).count()
330856
### Number of ways
> db.sydney.find({'type':'way'}).count()
59066
### Number of unique users
> db.sydney.distinct("created.user").length
1264
### The most enthusiastic users
```
db.sydney.aggregate([{"$match":{'created.user':{'$exists':1}}},
                            {'$group':{'_id':'$created.user',
                                        'count':{'$sum':1}}},
                             {'$sort':{'count':-1}},
                             {'$limit':10}])


{u'count': 20808, u'_id': u'inas'}
{u'count': 20474, u'_id': u'aharvey'}
{u'count': 17897, u'_id': u'Ebenezer'}
{u'count': 17259, u'_id': u'samuelrussell'}
{u'count': 17085, u'_id': u'TheSwavu'}
{u'count': 16562, u'_id': u'dbaupp'}
{u'count': 13638, u'_id': u'Leon K'}
{u'count': 10845, u'_id': u'Warin61'}
{u'count': 10532, u'_id': u'JeLuF'}
{u'count': 9498, u'_id': u'bentrails'}
```

## Additional Ideas
I found that there are relatively less error in the Sydney area than that in cities of USA. The reason could be Australian are more cautious, but it is more likely that there are just fewer users of Open Street Map in Australia. A possible solution is to make the map contribution visible to activate users. For example, a "Contribution Ranking" could be published every week on the main page so that everyone knows there contribution would not be ignored.

Another idea I have for OpenStreetMap to improve its data quality is to automatically revise the data people updated. Errors are inevitable due to the nature of the product, but it may cause problems when people use it. I noticed that most of the errors are similar such as different abbreviations, wrong postcodes etc. so that this issue can be solved programmatically just like what I did to clean the data.

The benefit of auto correction is improving the data quality without requiring the user to put more efforts. A possible issue with the solution is that there may be some False Positive and False Negative when correcting the data by programs. For example a street may has a "St." in it's name, but the program may take it as a street type abbreviation and correct it. This issue can be solved by machine learning which take more features from correct data to audit the users' update.



## Additional Data Exploration
### What are the most popular cuisines in Sydney?
```python
db.sydney.aggregate([
        {'$match':{'cuisine':{'$exists':1}}},
        {'$group':{'_id':'$cuisine',
                   'count':{'$sum':1}}},
        {'$sort':{'count':-1}},
        {'$limit':10}

{u'count': 89, u'_id': u'coffee_shop'}
{u'count': 57, u'_id': u'burger'}
{u'count': 48, u'_id': u'thai'}
{u'count': 47, u'_id': u'pizza'}
{u'count': 39, u'_id': u'italian'}
{u'count': 37, u'_id': u'japanese'}
{u'count': 36, u'_id': u'chinese'}
{u'count': 22, u'_id': u'sandwich'}
{u'count': 21, u'_id': u'chicken'}
{u'count': 16, u'_id': u'indian'}
```

### What are the most popular amenties?
```python
db.sydney.aggregate([
        {'$match':{'amenity':{'$exists':1}}},
        {'$group':{'_id':'$amenity',
                   'count':{'$sum':1}}},
        {'$sort':{'count':-1}},
        {'$limit':10}

{u'count': 939, u'_id': u'parking'}
{u'count': 670, u'_id': u'restaurant'}
{u'count': 654, u'_id': u'bench'}
{u'count': 578, u'_id': u'cafe'}
{u'count': 450, u'_id': u'drinking_water'}
{u'count': 379, u'_id': u'toilets'}
{u'count': 373, u'_id': u'bicycle_parking'}
{u'count': 325, u'_id': u'pub'}
{u'count': 292, u'_id': u'school'}
{u'count': 253, u'_id': u'place_of_worship'}
```

### What are the most popular religion?
```python
db.sydney.aggregate([
        {'$match':{'religion':{'$exists':1}}},
        {'$group':{'_id':'$religion',
                   'count':{'$sum':1}}},
        {'$sort':{'count':-1}},
        {'$limit':10}
    ])

{u'count': 239, u'_id': u'christian'}
{u'count': 6, u'_id': u'muslim'}
{u'count': 4, u'_id': u'jewish'}
{u'count': 1, u'_id': u'unitarian_universalist'}
```

## Conclusion
During the research I have grasped the technique of wrangling, cleaning, and extracting data. It is a very good exercise for me to test my python skills and data analysing methodology. Apart from all those, I have had a more complete view of the city after the research. I have known the status quo of Open Street Map in Australia, the people in Sydney are mostly christian and they love coffee.