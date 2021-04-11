var express = require('express');
var router = express.Router();
var path = require('path');
router.use(express.static('public'));

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
  response.sendFile(path.resolve('views/player_page.html'));
});

module.exports = router;