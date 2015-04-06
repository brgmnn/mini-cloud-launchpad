$(document).ready(function() {
    var launched = false;
    var running = false;

    $("#launch").click(function() {
        if (launched === false) {
            $("#launch").addClass("disabled");

            $.get("api/launch", function(data) {
                $("#launch").removeClass("disabled").html("Terminate Wordpress");
                launched = true;
            });
        } else {
            $("#launch").addClass("disabled");

            $.get("api/terminate", function(data) {
                $("#launch").removeClass("disabled").html("Launch Wordpress");
                launched = false;
            })
        }
    });

    function poll_status() {
        if (launched === true) {
            $.get("api/status", function(data) {
                $("#status").html(data);
                running = data === "running";
                setTimeout(poll_status, 5000);
            });
        } else {
            setTimeout(poll_status, 5000);
        }
    }

    function poll_url() {
        if (running === true) {
            $.get("api/url", function(data) {
                if (running) {
                    $("#url").attr("href", "http://"+data).text(data);
                }
                setTimeout(poll_url, 5000);
            });
        } else {
             setTimeout(poll_url, 5000);
        }
    }

    poll_url();
    poll_status();
});
