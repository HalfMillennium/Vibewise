var express = require('express');
var app = express();
var router = express.Router();
var path = require('path');
//var exphbs = require('express-handlebars');
app.use(express.static('public'));
app.use(express.urlencoded({ extended: true }));
/*
app.engine('handlebars', exphbs({ defaultLayout: 'main' }));
app.set('view engine', 'handlebars');*/

//router.use(express.static('public'));
router.use(express.json());

router.get("/mood", function(request, response) {
  console.log("Mood prompt requested.");
  response.sendFile(path.resolve('views/moodprompt.html')); 
});

router.get("/load", function(request, response) {
  console.log("Loading...");
  response.sendFile(path.resolve('views/loading_page.html')); 
});

router.get("/player", function(request, response) {
  console.log("Player page requested.");
  //response.sendFile(path.resolve('views/player_page.html'));
  t = []
  for(track of request.body.track_info) {
    t.push({
      image: track[0],
      artist: track[1],
      song: track[2]
    })
  }
  console.log("track_info (objects):",t)
  response.sendFile(path.resolve('views/static_page.html'))
  //response.render("player_body", { t })
});

module.exports = router;