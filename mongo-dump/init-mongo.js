db.createUser(
    {
       user: "user",
       pwd: "password",
       roles:[
          {
             role:"readWrite",
             db:"getdata"
          }
       ]
    }
 )
db.createCollection('getdata',{capped : true, size:4096, max : 20})