$(document).ready(function () {
    $('.ui.search')
        .search({
            // change search endpoint to a custom endpoint by manipulating apiSettings
            apiSettings: {
                url: 'search/?q={query}'
            },
            type: 'category'
        })
    ;
});