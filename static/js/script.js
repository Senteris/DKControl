$(document).ready(function () {
    $('.ui.dropdown').dropdown();

    $("#age-slider").slider({
        max: 18,
        min: 1,
        range: true,
        values: [1, 18],
        slide: function (event, ui) {
            $("#result-age-slider").text("от " + ui.values[0] + " до " + ui.values[1]);
            $('#search-field-age').val(ui.values[0] + "-" + ui.values[1])
        },
    });

    $('.ui.search').search({
        // change search endpoint to a custom endpoint by manipulating apiSettings
        apiSettings: {
            url: '/search/?q={query}&json=true'
        },
        type: 'category',
        minCharacters: 0
    });

    $('#theme_switch').click(function () {
        $('body').toggleClass('theme_light');
        $('body').toggleClass('theme_dark');
        $.get('/theme/?theme=' + $('body').attr('class'))
    })

    const queryString = window.location.search;
    const urlParams = new URLSearchParams(queryString);
    const filters = urlParams.get('filters');
    if (filters) {
        $('.ui.dropdown')
            .dropdown("set selected", filters.split(','));
        $('#search-button').trigger("click")
    }
    if (urlParams.get('edit')) $('.edit.button').trigger("click")
    if (urlParams.get('operation') == "success") swal("Выполнено!", "Операция успешно выполнена!.", "success");

    $('.select').click(function () {
        $('.select').removeClass('selected');
        $('#select-result').val($(this).attr('value'));
        $(this).addClass('selected')
    });

    $('.attending-checkbox').click(function () {
        let status = "";
        if ($(this).is(":checked")) status = "True";
        $.get(`/attendings/${$(this).attr('name')}/`, {"status": status})
    })

    $('.edit.button').click(function () {
        $('.edit.button').replaceWith($('#edit-buttons').html())
        let items = $('.basic_info_block .item')
        for (let i = 0; i < items.length; i++) {
            let content = $(items[i]).children('.content.edit')
            let description = content.children('.description')
            if (content.hasClass('string')) {
                let value = description.text()
                if (value === "Не указано") value = "";
                description.html($('#string-edit-input').html());
                description.children().children('input').val(value)
                description.children().children('input').attr('name', content.attr('data-name'))
            } else if (content.hasClass('fio')) {
                let value = description.text()
                description.html($('#fio-edit-input').html());
                description.children().children('input').val(value)
                description.children().children('input').attr('name', 'fio')
            } else if (content.hasClass('date')) {
                let value = description.attr('data-date')
                description.html($('#date-edit-input').html());
                description.children().children('input').val(value)
                description.children().children('input').attr('name', content.attr('data-name'))
            } else if (content.hasClass('select')) {
                let value = description.attr('data-options').split(',')
                let selected = description.text()
                description.html($('#select-edit-input').html());
                for (let i2 in value) {
                    let option = $('<option></option>').val(value[i2]).text(value[i2]);
                    if (value[i2] === selected) option.attr('selected', '')
                    description.children().children('select').append(option)
                }
                description.children().children('select').attr('name', content.attr('data-name'))
            }
        }

        $('#bremove').click(function () {
            const createdAt = new Date($('#inCreatedAt').val());
            let date7DAgo = new Date();
            date7DAgo.setDate(date7DAgo.getDate() - 7);
            let is_archived = false;
            if ($('#inis_archived').val() == "True") is_archived = true;

            if (createdAt > date7DAgo || is_archived) // You can delete a person within 7 days.
                swal({
                    title: "Вы уверены?",
                    text: "Данные удаляться!",
                    type: "warning",
                    dangerMode: true,
                    buttons: {
                        cancel: {
                            text: "Отмена",
                            value: null,
                            visible: true,
                            className: "",
                            closeModal: true,
                        },
                        confirm: {
                            text: "Да, удалить это!",
                            value: true,
                            visible: true,
                            className: "",
                            closeModal: false
                        }
                    },
                }).then((value => {
                    if (value)
                        document.location.href = document.location.href + "remove/";
                }))
            else
                swal({
                    title: "Вы уверены?",
                    text: "Данные отправятся в архив!",
                    type: "warning",
                    dangerMode: true,
                    buttons: {
                        cancel: {
                            text: "Отмена",
                            value: null,
                            visible: true,
                            className: "",
                            closeModal: true,
                        },
                        confirm: {
                            text: "Да, архивировать это!",
                            value: true,
                            visible: true,
                            className: "",
                            closeModal: false
                        }
                    },
                }).then((value => {
                    if (value)
                        document.location.href = document.location.href + "archive/";
                }))
        })
    })
});