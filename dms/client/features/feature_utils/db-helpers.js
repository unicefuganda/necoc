module.exports = function () {
    var MongoClient = require('mongodb').MongoClient;

    return {
        dropDB: function (callback) {
            MongoClient.connect('mongodb://127.0.0.1:27017/dms_test', function (err, db) {
                if (err) { console.log(err); return; }
                db.dropDatabase(function(err, done) {
                    if (err) { console.log(err); return; }
                    db.close();
                    callback();
                });
            });
        }
    }
}