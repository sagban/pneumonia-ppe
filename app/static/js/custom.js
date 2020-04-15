$(function () {
    $("#results").hide();

});
// var images;
// var image_r;
// var prediction_r;
// var name_r;

function submitForm(){
    event.preventDefault();
    var form_data = new FormData($('#formid')[0]);
    const no_error = validateForm();
    uploadData(form_data, no_error );
}

function submitDemo(val) {
    event.preventDefault();
    $("#results").hide();
    $('.message').text('Please wait...');
    $("#results .row").html("");
    $("#results .user").text("");
    var data = new FormData();
    data.append('name', "Demo");
    data.append('email', "demo@pnemoscan.ai");
    data.append('filename', val);

    // console.log(data);
    $.ajaxSetup({
        headers: { "X-CSRFToken": getCookie("csrftoken") }
    });
    $.ajax({
            type: 'POST',
            url: '/demoajax/',
            data: data,
            contentType: false,
            cache: false,
            beforeSend: function(){
                $("#results").show();
                $("#results h1").text("Please Wait...");
                $('html, body').animate({scrollTop: $("#results").offset().top - 200 }, 500);
            },
            complete: function () {
                $("#results h1").text("Results");
            },
            processData: false,
            success: function(data) {
                $('.message').text("");
                if(data.status === 0){
                    $('html, body').animate({scrollTop: $("#results").offset().top - 50}, 500);
                    $("#results .user").text(data.message);
                }
                else if(data.status === 1){
                    $('html, body').animate({scrollTop: $("#results").offset().top - 50}, 500);
                    var user = data.username;
                    var email = data.email;
                    $("#results .user").text(user + " - " +email);
                    var images = data.images;
                    var len = images.length;
                    // var str = '';
                    for(var i=0; i<len; i++){

                        // console.log(images[i]);
                        var image = images[i].image;
                        var prediction = images[i].pred;
                        var name = images[i].name;
                        var str = '<div class=\'col-md-4 g-margin-b-30--xs\'>\n' +
                            '                    <article>\n' +
                            '                        <img class="img-responsive" src="data:image/png;base64,'+image+'" alt="Image">\n' +
                            '                        <div class="g-bg-color--white g-box-shadow__dark-lightest-v2 g-text-center--xs g-padding-x-40--xs g-padding-y-30--xs">\n' +
                            '                            <p class="text-uppercase g-font-size-14--xs g-font-weight--700 g-color--primary g-letter-spacing--2">'+'image ' +(i + 1).toString()  +' - '+name+'</p>\n' +
                            '                            <h2 class="g-font-size-26--xs g-letter-spacing--1">'+prediction+' case</h2>\n' +
                            '                        </div>\n' +
                            '                    </article>\n' +
                            '                </div>';

                        $("#results .row").append(str);
                    }

                }
            }
        });
}

function uploadData(form_data, no_error) {
    event.preventDefault();
    $("#results").hide();
    $('.message').text('Please wait...');
    $("#results .row").html("");
    $("#results .user").text("");


    if(no_error === true){
        $.ajaxSetup({
            headers: { "X-CSRFToken": getCookie("csrftoken") }
        });
        console.log(form_data);
        $.ajax({
            type: 'POST',
            url: '/uploadajax/',
            data: form_data,
            contentType: false,
            cache: false,
            beforeSend: function(){
                $("#results").show();
                $("#results h1").text("Please Wait...");
                $('html, body').animate({scrollTop: $("#results").offset().top - 200 }, 500);
            },
            complete: function () {
                $("#results h1").text("Results");
            },
            processData: false,
            success: function(data) {
                $('.message').text("");
                if(data.status === 1){
                    $('html, body').animate({scrollTop: $("#results").offset().top - 50}, 500);
                    var user = data.username;
                    var email = data.email;
                    $("#results .user").text(user + " - " +email);
                    var images = data.images;
                    var len = images.length;
                    // var str = '';
                    for(var i=0; i<len; i++){

                        // console.log(images[i]);
                        var image = images[i].image;
                        var prediction = images[i].pred;
                        var name = images[i].name;
                        var str = '<div class=\'col-md-4 g-margin-b-30--xs\'>\n' +
                            '                    <article>\n' +
                            '                        <img class="img-responsive" src="data:image/png;base64,'+image+'" alt="Image">\n' +
                            '                        <div class="g-bg-color--white g-box-shadow__dark-lightest-v2 g-text-center--xs g-padding-x-40--xs g-padding-y-30--xs">\n' +
                            '                            <p class="text-uppercase g-font-size-14--xs g-font-weight--700 g-color--primary g-letter-spacing--2">'+'image ' +(i + 1).toString()  +' - '+name+'</p>\n' +
                            '                            <h2 class="g-font-size-26--xs g-letter-spacing--1">'+prediction+' case</h2>\n' +
                            '                        </div>\n' +
                            '                    </article>\n' +
                            '                </div>';

                        $("#results .row").append(str);
                    }

                }
            }
        });

    }
    return false;

}

function validateForm(){
    const name = $('#formid input[name="name"]').val();
    const email = $('#formid input[name="email"]').val();

    if(!name || !email){
        $('.message').text("Please provide all the details");
        return false;
    }
    else if(!validateFiles()){
        return false;
    }
    else return true;
}

$('#formid input[name="files"]').change(function () {
    validateFiles();
});

function validateFiles(){
    $('.message').text("");
    const files = $('#formid input[name="files"]').get(0);
    const l = files.files.length;
    if(l < 1){
        $('.message').text("Please upload at least 1 image to continue");
        return false;
    }
    else if(l > 15){
       $('.message').text("Maximum 15 images are allowed");
        return false;
    }
    const image_extensions = ['ras', 'xwd', 'bmp', 'jpe', 'jpg', 'jpeg', 'xpm', 'ief', 'pbm', 'tif', 'gif', 'ppm', 'xbm',
                            'tiff', 'rgb', 'pgm', 'png', 'pnm'];
    for (var i = 0; i < l; i++) {
       var f = files.files[i];
       // console.log(f);
       const ext = f.name.split('.').pop().toLowerCase();
       const size = f.size;
        if ($.inArray(ext, image_extensions) == -1){
            $('.message').text("Please upload an appropriate image file");
            return false;
        }
        else if(size > 1000000){
            $('.message').text("Image " + f.name +" should be less that 1 MB");
            return false;
        }
    }
    return true;
}

function getCookie(c_name) {
    if (document.cookie.length > 0)
    {
        c_start = document.cookie.indexOf(c_name + "=");
        if (c_start != -1)
        {
            c_start = c_start + c_name.length + 1;
            c_end = document.cookie.indexOf(";", c_start);
            if (c_end == -1) c_end = document.cookie.length;
            return unescape(document.cookie.substring(c_start,c_end));
        }
    }
    return "";
}

