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
        const parsedData = JSON.parse(data);
        $("#sql").val(parsedData["sql_request"]);

        const dt = new Date();
        const time = dt.getHours() + ":" + dt.getMinutes() + ":" + dt.getSeconds();
        // TODO: improve lemmas_choices (note Object.keys(parsedData["lemmas_choices"]).length)
        const info =
            "Heure de génération de la requête: " + time + "<br>" +
            "Requête préparsée: " + "<br>" +
            parsedData["preformatted_request"] + "<br>";
        $("#sql_info").html(info);

        let lemma_html = "";
        for (const initial_word of Object.keys(parsedData["lemmas_choices"])) {
            const lemmas = parsedData["lemmas_choices"][initial_word];
            lemma_html += initial_word + ": " + lemmas;
            lemma_html += "<br>";
        }
        if (lemma_html != "") {
            $("#lemmas_choices").html("<h3>Lemmes alternatifs</h3>" + lemma_html);
            $("#lemmas_choices").show()
        }

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

        const res = JSON.parse(data);
        const rows = res["rows"];

        if (!('colnames' in res)) {
            $("#results_count").html(rows[0])
        } else {
            $("#results_count").html(rows.length);

            const colnames = res["colnames"];

            let header = '<tr>';
            for (const colname of colnames) {
                header += '<th>';
                header += colname;
                header += '</th>';
            }
            header += '</tr>';

            let tbody = '';
            for (const row of rows) {
                tbody += '<tr>';
                for (const cell of row) {
                    tbody += '<td>';
                    if (cell.endsWith('.htm') || cell.endsWith('.html')) {
                        tbody += '<a href="http://www4.utc.fr/~lo17/TELECHARGE/BULLETINS/' + cell + '"  target="_blank">' + cell + '</a>'
                    } else {
                        tbody += cell;
                    }
                    tbody += '</td>';
                }
                tbody += '</tr>';
            }
            $("#results_table").html(header + tbody)
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
    $("#lemmas_choices").html("");

    $("#sql_info").hide();
    $("#sql_form").hide();
    $("#lemmas_choices").hide();
    $("#error_natural_request_form").hide();

    getSQLRequest($('#natural_request').val());
});

$('#sql_form').submit((event) => {
    event.preventDefault();
    $("#error_sql_form").text("");
    $("#error_sql_form").hide();
    $("#results_info").text("");
    $("#results_info").hide();


    $("#results_count").html("");
    $("#results_table").html("");

    applySQLRequest($("#sql").val());
});

$("#error_natural_request_form").hide();
$("#error_sql_form").hide();
$("#sql_info").hide();
$("#lemmas_choices").hide();
$("#results_info").hide();
