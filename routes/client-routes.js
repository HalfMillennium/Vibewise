var express = require('express');
var app = express();
var router = express.Router();
var path = require('path');
var cors = require('cors');
app.use(cors())
app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));


/*
app.engine('handlebars', exphbs({ defaultLayout: 'main' }));
app.set('view engine', 'handlebars');*/

//router.use(express.static('public'));
router.use(express.json());
app.options('/mood', cors())
router.get("/mood", function(request, response) {
  console.log("Mood prompt requested.",path.resolve('views/moodprompt.html'));
  response.sendFile(path.resolve('views/moodprompt.html')); 
});

router.get("/load", function(request, response) {
  //console.log("Loading...",path.resolve('views/loading_page.html'));
  response.sendFile(path.resolve('views/loading_page.html')); 
  //response.sendFile(__dirname + "/views/loading_page.html")
});

router.post("/tracks", function(request, response) {
  //console.log("Player page requested.");
  //response.sendFile(path.resolve('views/player_page.html'));
  //console.log("start req",request.body.track_info,"end req")
  t = []
  try {
    for(track of request.body.track_info.responseJSON) {
      t.push({
        image: track[0],
        artist: track[1],
        song: track[2]
      })
    }
  } catch(e) {
    t = undefined
    response.end()
  }
  console.log("track_info (objects):",t)
  // add track info to session data, eventually this will be used for interactive player
  request.session.track_info = t
  //response.sendFile(path.resolve('views/static_page.html'))
  //response.render("player_body", { t })
  response.end()
});

router.get("/player", function(req, res) {
    if(req.session.track_info && req.session.track_info.length > 5) {
      res.sendFile(path.resolve('views/static_page_2.html'))
    } else if(req.session.track_info && req.session.track_info.length <= 5) {
      res.sendFile(path.resolve('views/not_many_recs.html'))
    } else {
      res.sendFile(path.resolve('views/no_recs_2.html'))
    }
});

module.exports = router;