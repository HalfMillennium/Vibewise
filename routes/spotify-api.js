require('dotenv').config()
var express = require('express');
var router = express.Router();
var path = require('path');
var SpotifyWebApi = require('spotify-web-api-node');
require('dotenv').config()

// if testing locally: use localhost:888
var redirectUri = 'https://vibewise.herokuapp.com/callback';
var scopes = ['user-top-read','streaming','user-read-private', 'user-modify-playback-state', 'user-read-currently-playing'];
var showDialog = true;
var acc_token;

clID = process.env.CLIENT_ID,
clSEC = process.env.CLIENT_SECRET;
// The API object we'll use to interact with the API
var spotifyApi = new SpotifyWebApi({
  clientId : clID,
  clientSecret : clSEC,
  redirectUri : redirectUri
});
const http = require('http')
const querystring = require('querystring')
var track_ids;

router.use(express.static('public'));

router.get("/", function (request, response) {
  // starts vibe engine
  /*
  if(!request.session.v) {
    var engine = require('child_process').exec('python vibe_engine.py', {
      cwd: '/Users/percival/Documents/GitHub/Vibewise/core/flask'
    }, function(error, stdout, stderr) {
      if(error) {
        console.log("Error:",error,"\n")
      }
      if(stderr) {
        console.log("Stderr:",stderr,"\n")
      }
      //console.log("Vibe engine initiated:\n",stdout)
    });
    engine.stdout.pipe(process.stdout)
    engine.on('exit', function() {
      console.log("Vibe engine initiated.")
    })
    request.session.v = 1
  }*/

  response.sendFile(path.resolve(__dirname + './../views/index.html'));
});
  

router.get("/authorize", function (request, response) {
  var authorizeURL = spotifyApi.createAuthorizeURL(scopes, null, showDialog);
  console.log(authorizeURL)
  response.send(authorizeURL);
});

// Exchange Authorization Code for an Access Token
router.get("/callback", function (request, response) {
  var authorizationCode = request.query.code;
  console.log(authorizationCode)
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

router.get("/logout", function (request, response) {
  response.redirect('/');
});

router.get('/getplaylists', function (request, response) {
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

router.get("/gettone", function (request, response) {
  str = request.query.text
  console.log(str)
  const options = {
    hostname: 'https://aqueous-bastion-86228.herokuapp.com',
    //port: 5000,
    path: '/gettone/'+str,
    method: 'GET'
  }
  mood = ''
  const req = http.request(options, res => {
    console.log(`statusCode: ${res.statusCode}`)
    res.on('data', (d) => {
      console.log(`BODY: ${d.toString()}`);
      if(d.toString() == 'no_tone') {
        response.status(400).send("No tone detected! Try another phrase/sentence.")
        response.end()
      }
      response.send(d.toString());
    });
  })

  req.on('error', error => {
    console.error(error)
  })

  req.end()
});

router.get("/gettracks", function(request, response) {
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
    hostname: 'https://aqueous-bastion-86228.herokuapp.com',
    //port: 5000,
    path: '/getfilter/?'+get_request_args,
    method: 'GET'
  }

  const req = http.request(options, res => {
    console.log(`statusCode: ${res.statusCode}`)
    res.on('data', (d) => {
      // d = list of tracks
      if(d == "INACTIVE") {
        response.send(path.resolve("views/no_active.html"))
      }
      track_ids = d
      response.send(track_ids)
    })
  })

  req.on('error', error => {
    console.error(error.message)
  })

  req.end()
  
});


module.exports = router;