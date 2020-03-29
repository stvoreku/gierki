



$(function() {
    // This function gets cookie with a given name
    function getCookie(name) {
        var cookieValue = null;
        if (document.cookie && document.cookie != '') {
            var cookies = document.cookie.split(';');
            for (var i = 0; i < cookies.length; i++) {
                var cookie = jQuery.trim(cookies[i]);
                // Does this cookie string begin with the name we want?
                if (cookie.substring(0, name.length + 1) == (name + '=')) {
                    cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                    break;
                }
            }
        }
        return cookieValue;
    }
    var csrftoken = getCookie('csrftoken');

    /*
    The functions below will create a header with csrftoken
    */

    function csrfSafeMethod(method) {
        // these HTTP methods do not require CSRF protection
        return (/^(GET|HEAD|OPTIONS|TRACE)$/.test(method));
    }
    function sameOrigin(url) {
        // test that a given url is a same-origin URL
        // url could be relative or scheme relative or absolute
        var host = document.location.host; // host + port
        var protocol = document.location.protocol;
        var sr_origin = '//' + host;
        var origin = protocol + sr_origin;
        // Allow absolute or scheme relative URLs to same origin
        return (url == origin || url.slice(0, origin.length + 1) == origin + '/') ||
            (url == sr_origin || url.slice(0, sr_origin.length + 1) == sr_origin + '/') ||
            // or any other URL that isn't scheme relative or absolute i.e relative.
            !(/^(\/\/|http:|https:).*/.test(url));
    }

    $.ajaxSetup({
        beforeSend: function(xhr, settings) {
            if (!csrfSafeMethod(settings.type) && sameOrigin(settings.url)) {
                // Send the token to same-origin, relative URLs only.
                // Send the token only if the method warrants CSRF protection
                // Using the CSRFToken value acquired earlier
                xhr.setRequestHeader("X-CSRFToken", csrftoken);
            }
        }
    });

});

function tap(card){
        $.ajax({
    url : "", // the endpoint
    type : "POST", // http method
    data : {
    'card_tap':card
    }, // data sent with the post request

    success : function(json) {
	    console.log(json)
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

function fillGame(cards) {

    $('.cardtable').empty();
    $('.cardtable').append("<tr>")
    var arrayLength = cards.length;
    for (var i = 0; i < arrayLength; i++) {
        if(i % 5 === 0) {$('.cardtable').append("</tr><tr>")}

        //console.log(i)
        //console.log(cards[i]);
        var inHTML = ""

        inHTML += ("<td>" + cards[i].word)
        if ('visible' in cards[i]) {
            if(cards[i].visible === false){inHTML += "<button onclick='tap(" + cards[i].id + ")'>TAP</button>"}
            if(cards[i].visible === true){inHTML += cards[i].status}
        }
        $('.cardtable').append(inHTML)
}

}




function game_update(gamenum) {
    console.log('update')
        $.ajax({
    url : "/game/", // the endpoint
    type : "GET", // http method
    data : {
    'game_number': gamenum
    }, // data sent with the post request

    success : function(json) {
	    console.log(json)
        cards = json['cards']
        fillGame(cards);
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });
}

function add_player(selector, team) {
    console.log(team)
    $.ajax({
    url : "", // the endpoint
    type : "POST", // http method
    data : {
    'add_player':$(selector).val(), 'team':team,
    }, // data sent with the post request

    success : function(json) {
	    console.log(json)
        location.reload();
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });


}
function add_leader(selector, team){
    console.log(team)
        $.ajax({
    url : "", // the endpoint
    type : "POST", // http method
    data : {
    'add_leader':$(selector).val(), 'team':team,
    }, // data sent with the post request

    success : function(json) {
	    console.log(json)
        location.reload();
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });


}

function start_game(){
            $.ajax({
    url : "", // the endpoint
    type : "POST", // http method
    data : {
    'game_status':'active'
    }, // data sent with the post request

    success : function(json) {
	    console.log(json)

        location.reload();
        },

        // handle a non-successful response
        error : function(xhr,errmsg,err) {
            console.log(xhr.status + ": " + xhr.responseText); // provide a bit more info about the error to the console
        }
    });


}

