// server.js
// where your node app starts

// init project
var express = require('express');
var app = express();
var bodyParser = require('body-parser');
var Promise = require('promise');

app.use(bodyParser.urlencoded({
  extended: true
}));

// http://expressjs.com/en/starter/static-files.html
app.use(express.static('public'));

// http://expressjs.com/en/starter/basic-routing.html

/**  when home page is requested, respond with this file **/
app.get("/", function (request, response) {
  response.sendFile(__dirname + '/views/player_page.html');
});

app.get("/desiredvibe", function (request, response) {
  response.sendFile(__dirname + '/views/moodprompt.html');
});


//-------------------------------------------------------------//


// init Spotify API wrapper
var SpotifyWebApi = require('spotify-web-api-node');

// Replace with your redirect URI, required scopes, and show_dialog preference
var redirectUri = 'https://github.com/HalfMillennium',
    clID = '9013dc5d86b84ffca62df2f22e00968e',
    clSEC = 'b9484118ab374707925b1b15100cc58b';

var scopes = ['user-top-read','streaming','user-read-private'];
var showDialog = true;

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
    response.redirect(`/#access_token=${data.body['access_token']}&refresh_token=${data.body['refresh_token']}`)
  }, function(err) {
    console.log('Something went wrong when retrieving the access token!', err.message);
  });
});

app.get("/logout", function (request, response) {
  response.redirect('/');
});

app.get('/getplaylists', function (request, response) {
  /* I want to serve his html file after the user is authenticated */
  //response.sendFile(__dirname + '/views/nextpage.html');
  
  var loggedInSpotifyApi = new SpotifyWebApi();
  console.log(request.headers['authorization'].split(' ')[1]);
  loggedInSpotifyApi.setAccessToken(request.headers['authorization'].split(' ')[1]);
  
  // Get user playlists
  loggedInSpotifyApi.getUserPlaylists()
    .then(function(data) {
      console.log(data.body);
      response.send(data.body);
    }, function(err) {
      console.error(err);
    });
});

function getAverage(vals) {
  var sum = 0;

  vals.forEach(function(data) {
      sum += data;
  });

  return sum / vals.length;
}

app.post('/getdata', function (request, response) {
  var loggedInSpotifyApi = new SpotifyWebApi();

  loggedInSpotifyApi.setAccessToken(request.headers['authorization'].split(' ')[1]);

  var playlistID = request.body.listID;
    
  // Get tracks in a playlist
  loggedInSpotifyApi.getPlaylist(playlistID)
    .then(function(data) {
      var track_data = [];

      console.log("// AUDIO ANALYSIS RESULTS //");
      data.body.tracks.items.forEach(function(data) {
          //console.log(data.track);
        
        loggedInSpotifyApi.getAudioAnalysisForTrack(data.track.id)
            .then(function(audiof) {
              track_data.push(audiof.body.segments[0].pitches);
              console.log(data.track.name + " : " + getAverage(audiof.body.segments[0].pitches));
            },function(err) {
              console.log('Something went wrong!', err);
            });
      });

      response.send(track_data);
    }, function(err) {
      console.log('Something went wrong!', err);
    });
});

//-------------------------------------------------------------//


// listen for requests :)
var listener = app.listen('8888', function () {
  console.log('Your app is listening on port ' + listener.address().port);
});
