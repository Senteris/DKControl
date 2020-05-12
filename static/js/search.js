$(document).ready(function () {
    let input = $("#search");
    input.keyup(function () {
        let result = $('#search-result');
        if (this.value.length !== 0) {
            search(this.value).then(function (data) {
                let out = "";
                for (let elem in data['students']) out+= "<br>" + data['students'][elem];
                for (let elem in data['teachers']) out+= "<br>" + data['teachers'][elem];
                for (let elem in data['parents']) out+= "<br>" + data['parents'][elem];
                for (let elem in data['groups']) out+= "<br>" + data['groups'][elem];
                result.html(out);
            });
        } else {
            result.html('');
        }
    });
});

async function search(query) {
    let ret = undefined;
    await $.get("/search/?q=" + query, function (data) {
        ret = data;
    });
    return ret;
}