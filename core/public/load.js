/**
 * TODO:
 * 
 * Write code for loading_page.html, contact Flask API to get track IDs instead of client.js.
 * 
 * This is necessary because methods from 'client.js' are terminated if pages are changed mid-way through them, so 'player_page.html' will never be displayed
 */

$(function name() {
    mood = localStorage.getItem("mood")
    getTracks(mood.replace(/['"]+/g, ''));
  });

  function getTracks(mood) {
      list_id = localStorage.getItem("playlist");
      var tracks = []
      //console.log("Is mood still " + mood + "?");
      $.ajax({
        url : "/gettracks",
        type: "GET",
        data: { id: list_id, mood_data: mood },
        contentType: "application/json; charset=utf-8",
        dataType: "json",
        success: function(res){
          // log returned tracks
          console.log("Client result: " + res);
          window.location.href = '/player'
        }
      });
  }
  