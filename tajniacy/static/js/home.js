function marco() {

$.ajax({
    url : "", // the endpoint
    type : "POST", // http method
    data : {

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