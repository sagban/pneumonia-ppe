
'use strict';

$(function () {
    $("#results").hide();
});
//initiate the time
var date1 = new Date();
var videoElement = document.querySelector('video');
// var audioSelect = document.querySelector('select#audioSource');
var videoSelect = document.querySelector('select#videoSource');
var canvas = document.querySelector('#canvas');
var video= document.querySelector('#video');
var Result = $("#result_strip");
var width = 400;
var height = 400*9/16;

navigator.mediaDevices.enumerateDevices()
  .then(gotDevices).then(getStream).catch(handleError);

// audioSelect.onchange = getStream;
videoSelect.onchange = getStream;

function gotDevices(deviceInfos) {

  for (var i = 0; i !== deviceInfos.length; ++i) {
      var deviceInfo = deviceInfos[i];
      var option = document.createElement('option');
      option.value = deviceInfo.deviceId;
      if (deviceInfo.kind === 'videoinput') {
          option.text = deviceInfo.label || 'camera ' + (videoSelect.length + 1);
          videoSelect.appendChild(option);
      } else {
          console.log('Found one other kind of source/device: ', deviceInfo);
      }
    // if (deviceInfo.kind === 'audioinput') {
    //   option.text = deviceInfo.label ||
    //     'microphone ' + (audioSelect.length + 1);
    //   audioSelect.appendChild(option);
    // } else

  }
}

function getStream() {
  if (window.stream) {
    window.stream.getTracks().forEach(function(track) {
      track.stop();
    });
  }
  var widthVideo = function(){
      return width;
      // return window.innerWidth;
    // if (window.innerWidth < 600){
    //   return window.innerWidth;
    // }
    // else{
    //   return 500;
    // }
  };
   var heightVideo = function(){

       return height;
       // return window.innerHeight;
       // if (window.innerHeight < 800 && window.innerWidth < 600){
       //
       //  }
       //  else{
       //    return 600;
       //  }
  };
  var constraints = {
    video: {
      deviceId: {exact: videoSelect.value},
        width:widthVideo(),
        height:heightVideo()
    }
  };

  navigator.mediaDevices.getUserMedia(constraints).
    then(gotStream).catch(handleError);
}

function gotStream(stream) {
  window.stream = stream; // make stream available to console
  videoElement.srcObject = stream;
}

function handleError(error) {
  $(".message").html(error);
}

function takepicture() {

  // $('html, body').animate({scrollTop: $("video").offset().top - 100 }, 500);
    $("#results").show();
    $("#startButton span").html("Stop");
    var widthVideo = function(){
    return width;
  };
   var heightVideo = function(){
    return height;
  };
   var width = widthVideo();
   var height = heightVideo();
    canvas.width = width;
    canvas.height = height;
    canvas.getContext('2d').drawImage(video, 0, 0, width, height);
    var dataUrl = canvas.toDataURL('image/jpg');
    Result.html("Trying..");
    console.log(dataUrl);
    $.ajax({
    type: "POST",
    headers: {
        'Content-Type': 'application/x-www-form-urlencoded'
    },
    crossDomain: true,
    url: "https://v91bnrsr4k.execute-api.us-west-2.amazonaws.com/prod",
    data: {
        data: dataUrl
    }
    }).done(function(data) {

        $("#results").show();
        $('html, body').animate({scrollTop: $("#results").offset().top }, 500);
        if(data.status === 0){
            Result.html(data.message);
        }

        else if(data.code =='NO BarCode Found'){
            console.log("Trying..")
            var interval = setTimeout(function(){

                var date2 = new Date();
                var diff = date2 - date1;
                if(diff > 100000){

                    Result.html('Try Again : Time Out');
                    $("#startButton span").html("Start");
                    clearTimeout(interval);

                }
                $('#startbutton').click();


            },2000);

        }
        else{
            // console.log(data.code);
            var obj = JSON.parse(data);
            var i;
            Result.html('<b>Detected</b> :)<ol>');
            for(i=0; i<obj.length;i++){
                Result.append("<li><ul><li>Code: <b>"+obj[i].code+"</b></li><li>Type: <b>"+obj[i].type+"</b></li></ul></li>");
            }
            Result.append("</ol>")
            window.navigator.vibrate(200);
            clearTimeout(interval);
        }

        // Do Any thing you want
    })
        .fail(function(){
            console.log('Failed')
        });
}


startButton.addEventListener('click', function(ev){
    takepicture();
    Result.html("Searching..");
    ev.preventDefault();
    }, false
);

function start() {
    $("#startButton span").html("Stop");
    $('html, body').animate({scrollTop: $("#results").offset().top }, 500);

}
