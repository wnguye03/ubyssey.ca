var section_count = 1;
//a GET request based on the 'section'
function load_sections(scrollHandler) {
    $.ajax({
        url: '/beta',
        type: 'get',
        data: {
            section_count: section_count,
        },
        beforeSend: function () {
            $('.loader').show();
        },
        complete: function () {
            $('.loader').hide();
        },
        success: function (response) {

            // if the response.length is < 141 it means that the user have loaded all of the sections on the homepage and we will remove the scrolling functionality 
            if (response.length > 141) {
                document.getElementById('section_container').innerHTML = document.getElementById('section_container').innerHTML + `${response}`

                $(window).scroll(scrollHandler);
                section_count = section_count + 1;
            } else {
                $(window).off("scroll", scrollHandler);
            }
        }
    })
}

$(window).scroll(function scrollHandler() {
    //An ajax call will be sent when the user reaches the bottom of the window
    if ($(window).scrollTop() + $(window).height() == $(document).height()) {
        $(window).off("scroll", scrollHandler);
        load_sections(scrollHandler);
    }
})
