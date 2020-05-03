$(document).ready(function () {
    // Init
    $('.image-section').hide();
    $('.loader').hide();
    $('#result').hide();

    // Upload Preview
    function readURL(input) {
        if (input.files && input.files[0]) {
            //Read the file from the form and show it in the preview
            var reader = new FileReader();
            reader.onload = function (e) {
                console.log("loading preview")
                $('#imagePreview').attr('src', e.target.result);
                $('#imagePreview').hide();
                $('#imagePreview').fadeIn(650);
            }
            reader.readAsDataURL(input.files[0]);
        }
    }

    //On upload, show the image and the predict button
    $("#imageUpload").change(function () {
        $('.image-section').show();
        $('#btn-predict').show();
        console.log("changed");
        readURL(this);
    });

    // Make the request for the predictions with the form data and then show the results
    $('#btn-predict').click(function () {
        var form_data = new FormData($('#upload-file')[0]);

        // Show loading animation
        $(this).hide();
        $('.loader').show();

        // Make the request
        $.when($.ajax({
            type: 'POST',
            url: '/predict',
            data: form_data,
            contentType: false,
            cache: false,
            processData: false,
            async: true,
            success: function (response) {
                console.log("success !");
            },
        })).then( function(response) {
            //On successful response get and display the result  
            console.log('Success!');
            console.log(response);
            $('.loader').hide();
            $('#result').fadeIn(600);

            let labeled_img = "data:image/png;base64," + response['prediction']['labeled_img'];            
            let filled_img = "data:image/png;base64," + response['prediction']['filled_img'];
            id = Math.floor(Math.random() * 1e16);
            $('#imageLabeled').attr('src', labeled_img);
            $('#imageFilled').attr('src', filled_img);

            // Prepare the download buttons
            $("#btn-download-l").attr("download", "labeled_image_" + id + ".png").attr("href", labeled_img);            
            $("#btn-download-f").attr("download", "filled_image_" + id + ".png").attr("href", filled_img);
        }).fail( function(err) {
            //On failure, handle the error
            console.log("Error happened ! : \n" + err);
            alert("Unknown error happened, please try again");
            $('#result').hide();
            $('.loader').hide();
            $('#btn-predict').show();
        });
    });

});
