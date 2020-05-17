$(document).ready(function () {
    $("#search-button").click(function () {
        let data = {
            "q": $(this).parent().children().val(),
            "filters": $('#search-field-filters').val(),
            "age": $('#search-field-age').val(),
            "start": $('#search-field-start').val(),
            "end": $('#search-field-end').val(),
            "json": "extend"
        };
        $('#search-button').addClass('loading');
        $.get({
            url: "/search/",
            data: data,
            dataType: "json",
            success: function (data) { // Удачи
                delete data['results']['additions'];
                $('#search-result').html('');

                let isEmpty = true;

                for (let result in data['results']) {
                    let groupData = data['results'][result];
                    if (groupData['results'].length === 0) continue;
                    isEmpty = false;
                    $('#search-result').append($('#search-template-group').html());
                    $($('#search-result').children('.ui.segment')[$('#search-result').children('.ui.segment').length - 1]).children().html(groupData['name']);

                    let group = $($('#search-result').children('.ui.segments')[$('#search-result').children('.ui.segment').length - 1]);
                    for (let result in groupData['results']) {
                        group.append($('#search-template-item').html());
                        group.children().last().children().children().first().html(groupData['results'][result]['title']);
                        group.children().last().attr('href', groupData['results'][result]['url']);

                        if (groupData['results'][result]['extend'] !== undefined) {
                            for (let extend in groupData['results'][result]['extend']) {
                                let extendData = groupData['results'][result]['extend'][extend];
                                group.children().last().children().children().last().append($('#search-template-list-item').html());
                                group.children().last().children().children().last().children().last().children('.content').children('.header').text(extendData['name']);
                                group.children().last().children().children().last().children().last().attr('href', extendData['url'])
                            }
                        }
                    }
                }

                if (isEmpty) $('#search-result').html("<h3 style='margin: 20px'>Нет результатов</h3>");

                $('#search-button').removeClass('loading');
            }
        })
    })
});
