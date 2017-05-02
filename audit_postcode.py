from pymongo import MongoClient
import pprint
import re

client = MongoClient('mongodb://localhost:27017')
db = client.sydney
re_postcode = re.compile(r'\b\d{4}')

def audit_postcode():
    result = db.sydney.aggregate([
        {'$match':{'address.postcode':{'$exists':1}}},
        {'$group': {'_id': '$address.postcode',
                    'count': {'$sum': 1}}},
        {'$sort': {'count': -1}}
    ])
    return result

# def clean_postcode():
#     postToFix = db.sydney.find_all('address.postcode':)


if __name__ == '__main__':
    results = audit_postcode()
    with open('audit_postcode.txt','w') as f:
        for result in results:
            #print result
            pprint.pprint(result)
            f.write(str(result))
            f.write('\n')
