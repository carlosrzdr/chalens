$(document).ready(function() {

    $('#statusForm').click(function(event) {

        $.ajax({
            url : '/update_control',
            type : 'POST',
        });

        event.preventDefault();

    });

});

$(document).ready(function() {

    $('#eraseForm').click(function(event) {

        $.ajax({
            url : '/erase_data',
            type : 'POST',
        });

        event.preventDefault();

    });

});

$(document).ready(function() {

    $('#refreshNetwork').click(function(event) {

        $.ajax({
            url : '/refresh_network',
            type : 'POST',
        });

        event.preventDefault();

    });

});


$(document).ready(function() {

    $('#refreshArea').click(function(event) {

        $.ajax({
            url : '/refresh_area',
            type : 'POST',
        });

        event.preventDefault();

    });

});