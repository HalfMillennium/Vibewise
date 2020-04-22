function getData(id) {
    var token = localStorage.getItem("accessToken");

    //$('#Georgie').hide();

    $.get({url: '/getdata', headers: {"Authorization": `Bearer ${token}`}}, function(data) {
        // "Data" is the array of track objects we get from the API. See server.js for the function that returns it.
        console.log("id");

        //var login_info = document.getElementById("login_jumb");
        //login_info.style.display = "none";
        //$('#'+id).hide();
        document.getElementById(id).hide();
        /*
        var title = $('<h3>Your public Spotify playlists:</h3>');
        title.prependTo('#data-container');
  
        var tracks = new Array(data.items.length);
        // For each of the playlists, create an element
        data.items.forEach(function(playlist) {
          var playlistDiv = $('<button class="btn btn-dark button-pad" id="p_list" onclick="downloadInfo"></button>');
          playlistDiv.text(playlist.name);
          playlistDiv.appendTo('#data-container ul');
        });*/
  
      });
}