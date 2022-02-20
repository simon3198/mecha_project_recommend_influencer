$(document).ready(function() {
    $.ajax({
        type: "GET",
        url: "datas/recommender_final_score.csv",
        dataType: "text",
        success: function(data) {processData(data);}
     });
     $(document).on("click",'.btn-outline-secondary',function () {
       console.log(this.id)
       var win = window.open("","popup","")
       win.document.write('<h2 style="text-align:center; font-size:50px;">'+this.id+'</h2><img style="width:500px; height:300px;" src="influencer image/'+this.id+'_1.png" alt=""><img style="width:500px; height:300px;"  src="influencer image/'+this.id+'_3.png" alt=""><img style="width:500px; height:300px;"  src="influencer image/'+this.id+'_5.png" alt=""><img style="width:750px; height:450px;"  src="influencer image/'+this.id+'_4.png" alt=""><img style="width:750px; height:450px;"  src="influencer image/'+this.id+'_2.png" alt=""><br><hr>')
       // $("body").append("click!!!<br/>");
     });
     $('.btn-view').click(function(){
       $.ajax({
           type: "GET",
           url: "datas/recommender_final_weekview.csv",
           dataType: "text",
           success: function(data) {processData_(data);}
        });
     })
     $('.btn-score').click(function(){
       $.ajax({
           type: "GET",
           url: "datas/recommender_final_score.csv",
           dataType: "text",
           success: function(data) {processData(data);}
        });
     })
});



function processData(allText) {
  var table = $('#tableBody')
  table.empty()
    var allTextLines = allText.split(/\r\n|\n/);
    var headers = allTextLines[0].split(',');
    var lines = [];

    for (var i=1; i<allTextLines.length; i++) {
        var data = allTextLines[i].split(',');
        if (data.length == headers.length) {

            var tarr = [];
            for (var j=0; j<headers.length; j++) {
                tarr.push(headers[j]+":"+data[j]);
            }
            lines.push(tarr);
        }
    }
    var item = lines[0][4].split(':')[0]

    var title = $('.title')
    if(title.children().length==1){
      title.append('<h3 style="text-align:center;">'+item+'</h3>')
    }

    var table = $('#tableBody')
    for(var i=1;i<lines.length;i++){
      var id = lines[i-1][0].split(':')[1]
      var score = Math.round((lines[i-1][4].split(':')[1])*1000)/1000;
      var weekView = Math.round(lines[i-1][1].split(':')[1])
      var threeYears = Math.round(lines[i-1][3].split(':')[1])

      if(i<11){
        table.append('<tr><th scope="row">'+i+'</th><td><a href="https://blog.naver.com/'+id+'">'+id+'</a></td><td style="color:red;">'+score+'</td><td>'+weekView+'</td><td>'+threeYears+'</td><td><button id='+id+' type="button" type="button" class="btn btn-outline-secondary" name="button">Graph</button></td></tr>')
      }
      else{
        table.append('<tr><th scope="row">'+i+'</th><td><a href="https://blog.naver.com/'+id+'">'+id+'</a></td><td>'+score+'</td><td>'+weekView+'</td><td>'+threeYears+'</td><td><button id='+id+' type="button" type="button" class="btn btn-outline-secondary" name="button">Graph</button></td></tr>')

      }
    }
}

function processData_(allText) {
    var table = $('#tableBody')
    table.empty()


    var allTextLines = allText.split(/\r\n|\n/);
    var headers = allTextLines[0].split(',');
    var lines = [];

    for (var i=1; i<allTextLines.length; i++) {
        var data = allTextLines[i].split(',');
        if (data.length == headers.length) {

            var tarr = [];
            for (var j=0; j<headers.length; j++) {
                tarr.push(headers[j]+":"+data[j]);
            }
            lines.push(tarr);
        }
    }
    console.log(lines)
    for(var i=1;i<lines.length;i++){
      var id = lines[i-1][0].split(':')[1]
      var score = Math.round((lines[i-1][4].split(':')[1])*1000)/1000;
      var weekView = Math.round(lines[i-1][1].split(':')[1])
      var threeYears = Math.round(lines[i-1][3].split(':')[1])
      if(i<11){
        table.append('<tr><th scope="row">'+i+'</th><td><a href="https://blog.naver.com/'+id+'">'+id+'</a></td><td >'+score+'</td><td style="color:red;">'+weekView+'</td><td>'+threeYears+'</td><td><button id='+id+' type="button" type="button" class="btn btn-outline-secondary" name="button">Graph</button></td></tr>')
      }
      else{
        table.append('<tr><th scope="row">'+i+'</th><td><a href="https://blog.naver.com/'+id+'">'+id+'</a></td><td>'+score+'</td><td>'+weekView+'</td><td>'+threeYears+'</td><td><button id='+id+' type="button" type="button" class="btn btn-outline-secondary" name="button">Graph</button></td></tr>')

      }
    }
}
