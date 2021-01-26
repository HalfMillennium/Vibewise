// client-side js
// run by the browser each time your view template is loaded

//const { get } = require("https");

// by default, you've got jQuery,
// add other scripts at the bottom of index.html

$(function name() {
  
    $('#login').click(function() {
      // Call the authorize endpoint, which will return an authorize URL, then redirect to that URL
      $.get('/authorize', function(data) {
        console.log(data)
        window.location = data;
      });
    });
    
    const hash = window.location.hash
      .substring(1)
      .split('&')
      .reduce(function (initial, item) {
        if (item) {
          var parts = item.split('=');
          initial[parts[0]] = decodeURIComponent(parts[1]);
        }
        return initial;
      }, {});
    window.location.hash = '';

    localStorage.setItem("accessToken", hash.access_token);
    
    if (hash.access_token) {
      $('#login_jumb').hide();
      $.get({url: '/getplaylists', headers: {"Authorization": `Bearer ${hash.access_token}`}}, function(data) {
        // "Data" is the array of track objects we get from the API. See server.js for the function that returns it.
        console.log(data)

        var title = $('<h3 class="display-4 text-white">Choose one of your (public) playlists.</h3>');
        title.prependTo('#data-container');
  
        var tracks = new Array(data.items.length);
        // For each of the playlists, create an element
        data.items.forEach(function(playlist) {
          var playlistDiv = $('<button class="btn btn-dark button-pad " id="new"></button>');
          playlistDiv.text(playlist.name);
          playlistDiv.appendTo('#data-container ul');
          document.getElementById("new").id = playlist.id;

          var button = document.getElementById(playlist.id);
          button.setAttribute("onclick","getPrompt(this.id);");
          
          //button.title = button.id;
        });
  
      });
    }

    $('#submit-mood').click(function() {
      var txt = document.getElementById("moodInput").value;
      txt = txt.replaceAll(" ","_");
      console.log(txt)
      var mood = ''
      $.ajax({
        url : "/gettone",
        type: "GET",
        data: { text: txt },
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(res){
          // log returned tones
          mood = JSON.stringify(res);
          console.log("Resultant mood: " + mood);
          // TEST: Get access token
          getTracks(mood.replace(/['"]+/g, ''));
        }
      });
    });
  
  });

  function getTracks(mood) {
      list_id = localStorage.getItem("playlist");
      var tracks = []
      console.log("Is mood still " + mood + "?");
      $.ajax({
        url : "/gettracks",
        type: "GET",
        data: { id: list_id, mood_data: mood },
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(res){
          // log returned tracks
          //tracks = JSON.parse(res);
          console.log("Client result: " + res);
          //updateQueue(res);
        }
      });
  }
  
  function getPrompt(playlist_id) {
    console.log(playlist_id);
    localStorage.setItem('playlist',playlist_id);
    // switch to mood prompt
    window.location.href = '/mood'
  }

  function updateQueue(track_ids) {
    $.ajax({
      url : "http://127.0.0.1:5000/q?ids=123&ids=124",
      type: "GET",
      //sdata: JSON.stringify(track_ids),
      contentType: "application/json; charset=utf-8",
      dataType: "json",
      success: function(res){
        console.log("Song info: " + res);
      }
    });
  }