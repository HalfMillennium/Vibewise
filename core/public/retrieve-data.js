function getData(id) {
    var token = localStorage.getItem("accessToken");

    /*
    ~TODO~
      - download csv of values
    
    $.post({url: '/getdata', headers: {"Authorization": `Bearer ${token}`}}, { listID: "3Qm86XLflmIXVm1wcwkgDK"},
         function(data) {
        // "Data" is the array of track objects we get from the API. See server.js for the function that returns it.
        console.log(data);

        document.getElementById(id).style.visibility = "hidden";
        
        // example of csv creation with array values
        const rows = [
          ["name1", "city1", "some other info"],
          ["name2", "city2", "more info"]
        ];
      
        let csvContent = "data:text/csv;charset=utf-8," 
            + rows.map(e => e.join(",")).join("\n");
      });*/
      
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