from pymongo import MongoClient

client = MongoClient('mongodb://localhost:27017')
db = client.sydney

def most_enthusiastic_user():
    result = db.sydney.aggregate([{"$match":{'created.user':{'$exists':1}}},
                                {'$group':{'_id':'$created.user',
                                            'count':{'$sum':1}}},
                                 {'$sort':{'count':-1}},
                                 {'$limit':10}])
    return result

def most_popular_amenities():
    result = db.sydney.aggregate([
        {'$match':{'amenity':{'$exists':1}}},
        {'$group':{'_id':'$amenity',
                   'count':{'$sum':1}}},
        {'$sort':{'count':-1}},
        {'$limit':10}
    ])
    return result


def most_popular_cuisine():
    result = db.sydney.aggregate([
        {'$match':{'cuisine':{'$exists':1}}},
        {'$group':{'_id':'$cuisine',
                   'count':{'$sum':1}}},
        {'$sort':{'count':-1}},
        {'$limit':10}
    ])
    return result


def most_popular_religion():
    result = db.sydney.aggregate([
        {'$match':{'religion':{'$exists':1}}},
        {'$group':{'_id':'$religion',
                   'count':{'$sum':1}}},
        {'$sort':{'count':-1}},
        {'$limit':10}
    ])
    return result


results = most_popular_religion()
for item in results:
    print item