'use strict';

const {MongoClient} = require('mongodb');

const uri = "mongodb://root:password@mongodb:27017/";

// MongoClient.connect(uri, function(err, db) {
//   if (err) throw err;
//   var dbo = db.db("getdata");
//   dbo.collection("getdata").findOne({}, function(err, result) {
//     if (err) throw err;
//     console.log(result)
//     console.log(result['windows_percent'])
//     db.close();
//   });
// });

var express = require('express'),
    app = express();

app.set('views', 'views');

app.get('/', function(req, res) {
  MongoClient.connect(uri, function(err, db) {
    if (err) throw err;
    var dbo = db.db("getdata");
    var voteCollection = dbo.collection("getdata")
    const result = voteCollection.findOne({}, {sort:{$natural:-1}}, function(err, result) {
      if (err) throw err 
      console.log(result)
      db.close();

      res.render('home.pug', {
        windows: result['windows_percent'],
        mac: result['mac_percent']
      });
    })
  });
});

app.listen(8090);
module.exports.getApp = app;