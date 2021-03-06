// server.js
// where your node app starts

// init project
var express = require('express');
var app = express();
var bodyParser = require('body-parser');
const http = require('http')
const querystring = require('querystring')
var track_ids;

app.use(bodyParser.urlencoded({
  extended: true
}));

// http://expressjs.com/en/starter/static-files.html
app.use(express.static('public'));

// http://expressjs.com/en/starter/basic-routing.html

/**  when home page is requested, respond with this file **/
app.get("/", function (request, response) {
  response.sendFile(__dirname + '/views/index.html');
});

app.get("/gettone", function (request, response) {
  str = request.query.text
  console.log(str)
  const options = {
    hostname: '127.0.0.1',
    port: 5000,
    path: '/gettone/'+str,
    method: 'GET'
  }
  mood = ''
  const req = http.request(options, res => {
    console.log(`statusCode: ${res.statusCode}`)
    res.on('data', (d) => {
      console.log(`BODY: ${d.toString()}`);
      response.send(d.toString());
    });
  })

  req.on('error', error => {
    console.error(error)
  })

  req.end()
});

app.get("/gettracks", function(request, response) {
  id = request.query.id
  m = request.query.mood_data

  for (const key in request.query) {
    console.log(key, request.query[key])
  }
  
  // GET parameters
  const parameters = {
    acc: acc_token,
    playlist_id: id,
    mood: m
  }

  // GET parameters as query string : "?id=123&type=post"
  const get_request_args = querystring.stringify(parameters);

  const options = {
    hostname: '127.0.0.1',
    port: 5000,
    path: '/getfilter/?'+get_request_args,
    method: 'GET'
  }

  const req = http.request(options, res => {
    console.log(`statusCode: ${res.statusCode}`)
    res.on('data', (d) => {
      // d = list of tracks
      track_ids = d
      response.send(track_ids)
    })
  })

  req.on('error', error => {
    console.error(error)
  })

  req.end()
  
});


//-------------------------------------------------------------//


// init Spotify API wrapper
var SpotifyWebApi = require('spotify-web-api-node');

var redirectUri = 'http://localhost:8888/callback',
    clID = '',
    clSEC = '';

var scopes = ['user-top-read','streaming','user-read-private', 'user-modify-playback-state'];
var showDialog = true;
var acc_token;
// The API object we'll use to interact with the API
var spotifyApi = new SpotifyWebApi({
  clientId : clID,
  clientSecret : clSEC,
  redirectUri : redirectUri
});

app.get("/authorize", function (request, response) {
  var authorizeURL = spotifyApi.createAuthorizeURL(scopes, null, showDialog);
  console.log(authorizeURL)
  response.send(authorizeURL);
});

// Exchange Authorization Code for an Access Token
app.get("/callback", function (request, response) {
  var authorizationCode = request.query.code;

  spotifyApi.authorizationCodeGrant(authorizationCode)
  .then(function(data) {
    console.log(data)
    acc_token = data.body['access_token']
    console.log("Access token here(auth): " + data.body['access_token'])
    response.redirect(`/#access_token=${data.body['access_token']}&refresh_token=${data.body['refresh_token']}`)
  }, function(err) {
    console.log('Something went wrong when retrieving the access token!', err.message);
  });
});

app.get("/logout", function (request, response) {
  response.redirect('/');
});

app.get('/getplaylists', function (request, response) {
  var loggedInSpotifyApi = new SpotifyWebApi();
  console.log(request.headers['authorization'].split(' ')[1]);
  loggedInSpotifyApi.setAccessToken(request.headers['authorization'].split(' ')[1]);

  // Get user playlists
  loggedInSpotifyApi.getUserPlaylists()
    .then(function(data) {
      //console.log(data.body);
      response.send(data.body);
    }, function(err) {
      console.error(err);
    });
});

//app.use(express.static('views'));
app.get("/mood", function(request, response) {
  console.log("Mood prompt requested.");
  response.sendFile(__dirname + '/views/moodprompt.html'); 
});

app.get("/load", function(request, response) {
  console.log("Loading...");
  response.sendFile(__dirname + '/views/loading_page.html'); 
});

app.get("/player", function(request, response) {
  console.log("Player page requested.");
  response.sendFile(__dirname + '/views/player_page.html'); 
});

//-------------------------------------------------------------//


// listen for requests
var listener = app.listen('8888', function () {
  console.log('Your app is listening on port ' + listener.address().port);
});
