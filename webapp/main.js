function getSQLRequest(naturalRequest) {
    const data = {
        natural_request: naturalRequest
    };

    const ajaxRequest = $.ajax({
        method: "POST",
        url: "http://127.0.0.1:5000/natural",
        data: data
    });

    ajaxRequest.done((data) => {
        $("#sql").val(data);

        const dt = new Date();
        const time = dt.getHours() + ":" + dt.getMinutes() + ":" + dt.getSeconds();
        $("#sql_info").text("Heure de génération de la requête: " + time);

        $("#sql_info").show();
        $("#sql_form").show();
    });

    ajaxRequest.fail((jqXHR, textStatus, errorThrown) => {
        $("#error_natural_request_form").text(textStatus + ": " + errorThrown);
        $("#error_natural_request_form").show();
    })
}

function applySQLRequest(sqlRequest) {
    const data = {
        sql_request: sqlRequest
    };

    const ajaxRequest = $.ajax({
        method: "POST",
        url: "http://127.0.0.1:5000/sql",
        data: data
    });

    ajaxRequest.done((data) => {
        console.log(data);

        const dt = new Date();
        const time = dt.getHours() + ":" + dt.getMinutes() + ":" + dt.getSeconds();
        $("#results_info").text("Heure de génération de la requête: " + time);
        $("#results_info").show();

        const rows = JSON.parse(data);
        if (rows.length === 1 && rows[0].length === 1) {
            $("#results_count").html(rows[0])
        } else {
            $("#results_count").html(rows.length);
            for (row of rows) {
                $("#results_table").append(
                    '<tr>' +
                    '<td>' + row[0] + '</td>' +
                    '<td>' + row[1] + '</td>' +
                    '<td>' + row[3] + '</td>' +
                    '<td>' + row[4] + '/' + row[5] + '/' + row[6] + '</td>' +
                    '<td><a href="http://www4.utc.fr/~lo17/TELECHARGE/BULLETINS/' + row[2] + '"  target="_blank">' + row[2] + '</a></td>' +
                    '</tr>'
                );
            }
        }
    });

    ajaxRequest.fail((jqXHR, textStatus, errorThrown) => {
        $("#error_sql_form").show();
        $("#error_sql_form").text(textStatus + ":   " + errorThrown)
    });
}


$(document).ready(function () {
    $(window).keydown(function (event) {
        if (event.keyCode == 13) {
            event.preventDefault();
            return false;
        }
    });
});

$('#natural_request_form').submit((event) => {
    event.preventDefault();
    $("#sql").val("");
    $("#sql_info").text("");

    $("#sql_info").hide();
    $("#sql_form").hide();
    $("#error_natural_request_form").hide();

    getSQLRequest($('#natural_request').val());
});

$('#sql_form').submit((event) => {
    event.preventDefault();
    $("#error_sql_form").text();
    $("#error_sql_form").hide();
    $("#results_info").text();
    $("#results_info").hide();


    $("#results_count").html();
    $("#results_table").html();

    applySQLRequest($("#sql").val());
});

$("#error_natural_request_form").hide();
$("#error_sql_form").hide();
$("#sql_info").hide();
$("#results_info").hide();
