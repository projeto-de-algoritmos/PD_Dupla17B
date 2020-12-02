$(function () {

    var numberOfMovies = 0;

    $.showError = function(failure) { 
        $(failure).hide().appendTo('#iterative').fadeIn();
        setTimeout(function () {
            $('#failure').fadeOut();
            $('#failure').remove();
        }, 2600);
    }

    $('#names').on('click', ".title" , function() {
        if (!$(this).val()){

            numberOfMovies +=1;

            var nameInput = '<input type="text" class="form-control mb-2 title" name="title"  placeholder="Movie name" />'
            var timesInput = '<input id="time-'+numberOfMovies+'" class="mb-2" data-role="timepicker" data-seconds="false" />'
    
            $(nameInput).appendTo('#names');
            $(timesInput).appendTo('#times');          

        }   
    });


    $("#schedule").click(function () {


        var movieNames = $('.title').map((i, e) => e.value).get();
        movieNames = movieNames.filter((e) => e != '' && e != ' ')

        var movieStartTimes = $('[id^="time-"]').map((i, e) => e.value).get();
        movieStartTimes.slice(0,movieNames.length)
        
        if (!movieNames.join("")) {
            var failure = '<div id="failure" class="ml4 alert alert-danger"><p>You must include at least one movie !</p></div>'
            $.showError(failure)
            return
        }

        $.ajax({
            url: "/schedule",
            type: "POST",
            contentType: 'application/json',
            data: JSON.stringify({
                "movie_names": movieNames,
                "movie_start_times": movieStartTimes
            }),
            success: function (response) {
                $("#result").hide().html(response).fadeIn();
            },
            error: function () {
                var failure = '<div id="failure" class="ml4 alert alert-danger"><p>Movie not found</p></div>'
                $.showError(failure)         
            }
        });


    });



});