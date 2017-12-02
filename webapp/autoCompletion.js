var natural_request_input = new autoComplete({
    selector: '#natural_request',
    source: function(term, suggest) {
        term = term.toLowerCase();
        terms = term.split(' ');

        currentTerm = terms[findCarpetIndex($("#natural_request")["0"], terms)-1];
        var choices = data;
        var suggestions = [];
        for (j=0;j<choices.length;j++)
            if (~choices[j].toLowerCase().indexOf(currentTerm)) suggestions.push(choices[j]);
        suggest(suggestions);
    },
    onSelect(event, term, item) {
        var request = $("#natural_request").val();
        var request_words = request.split(' ');
        request_words[findCarpetIndex($("#natural_request")["0"], request_words)-1] = term;
        var newVal = request_words.join(' ');
        var s = document.getElementById("natural_request");
        s.value = newVal;
    }
});

function findCarpetIndex(field, values) {
    var charSum = 0, i = 0;
    var carpetPosition = field.selectionStart;
    for (value of values) {
        if (charSum >= carpetPosition - values.length) { return i; }
        else {
            charSum += value.length;
            i++;  
        }
    }
    return i;
}