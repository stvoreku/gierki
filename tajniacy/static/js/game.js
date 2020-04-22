



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
    var arrayLength = cards.length;            // True == 1 #prawdziwe True === 1 #falszy
    for (var i = 0; i < arrayLength; i++) {
        if(i % 5 === 0) {$('.cardtable').append("</tr><tr>")}

        //console.log(i)
        //console.log(cards[i]);
        var inHTML = ""
        if('status' in cards[i])
            {
                inHTML += ("<td class=" + cards[i].status + ">" + cards[i].word)

            } else {
            inHTML += ("<td>" + cards[i].word)
        }
        if ('visible' in cards[i]) {
            if(cards[i].visible === false && !('status' in cards[i])){inHTML += "<br><button class='tapBtn' onclick='tap(" + cards[i].id + ")'>ODKRYJ</button>"}
            if(cards[i].visible === true){inHTML += " <br>ODKRYTA: " + cards[i].uncovered_by}
        }

            inHTML += "</td>"
        $('.cardtable').append(inHTML)
}

}

function fillPlayers(teams){


    team1 = Object.keys(teams)[0]
    team2 = Object.keys(teams)[1]

    $("#team1name").text(team1)
    $("#team2name").text(team2)

    $("#team1leader").text("Leader:" +  teams[team1].leader)
    $("#team2leader").text("Leader:" + teams[team2].leader)
    for (p in teams[team1].players) {
        $("team1").append('<li>' + p + '</li>')
    }
    for (p in teams[team2].players) {
        $("team2").append('<li>' + a + '</li>')
    }
    //$("#team1id").appendChild(teams[team1].players)
    //$("#team2id").appendChild(teams[team1].players)

}




function game_update(gamenum) {

        $.ajax({
    url : "/game/", // the endpoint
    type : "GET", // http method
    data : {
    'game_number': gamenum
    }, // data sent with the post request

    success : function(json) {

        cards = json['cards']
        teams = json['teams']
        fillPlayers(teams)
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
        //location.reload();
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
        //location.reload();
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

