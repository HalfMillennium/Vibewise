function getData(id) {
    var token = localStorage.getItem("accessToken");

    $.ajaxSetup({
        headers: { "Authorization": `Bearer ${token}` }
    });

    $.ajax({
        type: 'post',
        url:'/getdata',
        dataType: 'json',
        async: false,
        data: {listID: id},
        success: function(data){
          console.log(data);
          //document.getElementById(id).style.visibility = "hidden";

          var mean_pitches = [];
          data.forEach(pitch_group => {
              var sum = 0;
              pitch_group.forEach(pitch => {
                  sum += pitch;
              })
              mean_pitches.push(sum / pitch_group.length);

              var pit = $('<p id="n" class="text-white">Mean Pitch</p>');
              pit.prependTo('#data-container');
              document.getElementById("n").setAttribute("id", sum / pitch_group.length);
              document.getElementById(sum / pitch_group.length).setAttribute("title", sum / pitch_group.length);
          });
         }
      })
}