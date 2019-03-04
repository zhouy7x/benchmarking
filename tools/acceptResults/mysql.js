var https = require('https');
var url = require('url');
var fs = require('fs');
var mysql = require('mysql');
var auth = require('basic-auth');
var listenIP = process.argv[2];

// read in the data required to connect to the database
var dbConfig = require('./dbconfig.json');

// read in the authentication info
var authConfig = require('./authconfig.json');

// read in the key and certificate for the server
ssl_options = {
  key: fs.readFileSync('key.pem'),
  cert: fs.readFileSync('cert.pem'),
};


// authenticate requests to the bridge
function authenticate(request, response) {
   var authInfo = auth(request);
   if (!authInfo || authInfo.name !== authConfig.name || authInfo.pass !== authConfig.pass ) {
       console.log('authenticate 1st.');
      if (response !== undefined) {
         console.log('authenticate 2nd.');
         response.writeHead(401, {'WWW-Authenticate': 'Basic realm="' + authConfig.realm + '"'});
         response.end()
      }
      return false
   }
   return true
}


var errorFunction = function(request, response, error) {
  response.writeHead(404, {'Content-Type': 'text/html'})
  response.end(error)
};

var table = "benchmark_IDs";

  function connect2db() {
    // get and validate we have appropriate data
    // var queryData = url.parse(request.url, true).query;
    // var queryData = {id: 3, name: "require new"}
      // 1 - start_stop_time
      // 2 - startup_footprint
      // 3 - require new
      // 4 - require cached
      // 5 - acme air throughput
      // 6 - acme air latency
      // 7 - acme air pre footprint
      // 8 - acme air post footprint
      // 9 - octane
      // 10 - dc eis latency
      // 11 - dc eis throughput
      // 12 - web tooling benchmark
      // 13 - dc eis pre footprint
      // 14 - dc eis post footprint
    var queryDatas = [
        {id: 1, name: "start_stop_time"},
        {id: 2, name: "startup_footprint"},
        {id: 3, name: "require new"},
        {id: 4, name: "require cached"},
        {id: 5, name: "acme air throughput"},
        {id: 6, name: "acme air latency"},
        {id: 7, name: "acme air pre footprint"},
        {id: 8, name: "acme air post footprint"},
        {id: 9, name: "octane"},
        {id: 10, name: "dc eis latency"},
        {id: 11, name: "dc eis throughput"},
        {id: 12, name: "web tooling benchmark"},
        {id: 13, name: "dc eis pre footprint"},
        {id: 14, name: "dc eis post footprint"},
    ];

    queryDatas = [
      [1, 'start_stop_time'],
      [2, 'startup_footprint'],
      [3, 'require new'],
      [4, 'require cached'],
      [5, 'acme air throughput'],
      [6, 'acme air latency'],
      [7, 'acme air pre footprint'],
      [8, 'acme air post footprint'],
      [9, 'octane'],
      [10, 'dc eis latency'],
      [11, 'dc eis throughput'],
      [12, 'web tooling benchmark'],
      [13, 'dc eis pre footprint'],
      [14, 'dc eis post footprint'],
    ];

    table = 'stream_IDs';
    queryDatas = [
        [1, 'master'],
        [2, '4.x'],
        [3, '0.12.x'],
        [4, '6.x'],
        [5, '7.x'],
        [6, '8.x'],
        [7, 'canary'],
        [8, '10.x'],
    ];

    table = 'benchresults';
    queryDatas = [
        [1, 9, 1550045434, 3333],
        [1, 9, 1550145434, 4444],
        [1, 9, 1550245434, 5555],
        [1, 9, 1550345434, 6666],
        [1, 9, 1550445434, 7777],
        [1, 9, 1550545434, 8888],
        [1, 9, 1550645434, 9999],
        [1, 9, 1550745434, 8888],
        [1, 9, 1550845434, 7777],
        [1, 9, 1550945434, 6666],
        [1, 9, 1551045434, 5555],
        [1, 9, 1551145434, 4444],
    ];
    // queryDatas = [
    //     [1, 1, 1550045434, 48000],
    //     [1, 1, 1550145434, 47000],
    //     [1, 1, 1550245434, 46000],
    //     [1, 1, 1550345434, 45000],
    //     [1, 1, 1550445434, 44000],
    //     [1, 1, 1550545434, 43000],
    //     [1, 1, 1550645434, 44000],
    //     [1, 1, 1550745434, 45000],
    //     [1, 1, 1550845434, 46000],
    //     [1, 1, 1550945434, 47000],
    //     [1, 1, 1551045434, 48000],
    //     [1, 1, 1551145434, 49000],
    // ];

    var con = mysql.createConnection(dbConfig);

    con.connect(function(err) {
      if (err) {
        // errorFunction(request, response, 'failed to connect to db:' + err);
          console.log('failed to connect to db:' + err);
            setTimeout(connect2db(), 10);
          return
      }

      // extract data and add to database
      //   for (index in queryDatas) {
      //       var queryData = queryDatas[index];
        console.log(queryDatas);
      // con.query('INSERT INTO ' + table + ' SET ?', queryData, function(err, res) {
      con.query('INSERT INTO ' + table + '(streamid, benchid, time, value) VALUES ?', [queryDatas], function(err, res) {
        if (err) {
          // errorFunction(request, response, 'failed to run query:' + err);
            console.log('failed to run query:' + err)
          return
        }
        con.end(function(err) {
          if (err) {
              // errorFunction(request, response, 'failed to cleanly close db connection:' + err)
              console.log('failed to cleanly close db connection:' + err);

              return
          }

          // response.writeHead(200, {'Content-Type': 'text/html'});
          // response.end('ok')
          console.log('ok')
        })
      })
        // }
    })
    con.on('error', function(err) {
      console.log('db error', err);
      if(err.code === 'PROTOCOL_CONNECTION_LOST') {
        connect2db();
      } else {
        throw err;
      }
    });
  }
  connect2db();

// console.log(5);
// // server.listen(3001, listenIP)
// server.listen(3000, () => console.log('Listening on port 3000!'));
//
// console.log("Server running!");
