const { response } = require('express');
var express = require('express');
var router = express.Router();
var path = require('path');
express.use(express.static('public'));
express.use(express.urlencoded({ extended: true }));

express.engine('handlebars', exphbs({ defaultLayout: 'main' }));
express.set('view engine', 'handlebars');

router.get("/mood", function(request, response) {
  console.log("Mood prompt requested.");
  response.sendFile(path.resolve('views/moodprompt.html'));
});

router.get("/load", function(request, response) {
  console.log("Loading...");
  response.sendFile(path.resolve('views/loading_page.html'));
});

router.post("/player", function(req, res) {
  track_info = req.query.track_info;
  response.send("views/handles/player_body", { track_inf : track_info } )
});
/*
router.get("/player", function(request, response) {
  console.log("Player page requested.");
  response.sendFile(path.resolve('views/player_page.html'));
});*/

module.exports = router;