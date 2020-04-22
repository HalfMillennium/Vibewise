// client-side js
// run by the browser each time your view template is loaded

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
      $.get({url: '/nextpage', headers: {"Authorization": `Bearer ${hash.access_token}`}}, function(data) {
        // "Data" is the array of track objects we get from the API. See server.js for the function that returns it.
        console.log(data)

        var title = $('<h3 class="display-4">Your public Spotify playlists:</h3>');
        title.prependTo('#data-container');
  
        var tracks = new Array(data.items.length);
        // For each of the playlists, create an element
        data.items.forEach(function(playlist) {
          var playlistDiv = $('<button class="btn btn-dark button-pad " id="new"></button>');
          playlistDiv.text(playlist.name);
          playlistDiv.appendTo('#data-container ul');
          document.getElementById("new").id = playlist.name;

          var button = document.getElementById(playlist.name);
          button.setAttribute("onclick","getData(this.id)");
          button.title = button.id;
        });
  
      });
    }
  
  });
  