module.exports = function () {
    var MongoClient = require('mongodb').MongoClient;
    var _ = require('lodash');
    var persistentCollections = [
        'system.indexes',
        'user',
        'django_session',
        'token'
    ];

    function connectToMongo(callback) {
        MongoClient.connect('mongodb://127.0.0.1:27017/dms_test', function (err, db) {
            if (err) {
                console.log(err);
                return;
            }
            callback(db);
        });
    }

    return {
        dropDB: function (callback) {
            connectToMongo(function (db) {
                db.dropDatabase(function (err) {
                    if (err) {
                        console.log(err);
                        return;
                    }
                    db.close();
                    callback();
                });
            });
        },
        dropCollections: function (callback) {
            connectToMongo(function (db) {
                db.collectionNames(function (err, collectionNames) {
                    if (err) {
                        console.log(err);
                        return;
                    }

                    var names = collectionNames.map(function (collection) {
                        return collection.name.split('dms_test.')[1];
                    });

                    var uniqueCollections = _.difference(names, persistentCollections);
                    if (!uniqueCollections.length) {
                        db.close();
                        callback();
                    }

                    var count = 0;
                    uniqueCollections.forEach(function (collection_name) {
                        db.dropCollection(collection_name, function (err) {
                            err && console.log(collection_name, err);
                            if (++count == uniqueCollections.length) {
                                db.close();
                                callback();
                            }
                        });
                    });

                });
            });
        }
    }
}