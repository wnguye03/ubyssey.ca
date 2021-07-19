var culture_fetched = false;
var opinion_fetched = false;
var features_fetched = false;
var sports_fetched = false;
var science_fetched = false;


//a GET request based on the 'section'
function load_sections(section, scrollHandler) {


    $.ajax({
        url: '/beta/ubyssey',
        type: 'get',
        data: {
            section: section,
        },
        beforeSend: function () {
            $('.loader').show();
        },
        complete: function () {
            $('.loader').hide();
        },
        success: function (response) {



            document.getElementById('section_container').innerHTML = document.getElementById('section_container').innerHTML + `${response}`

            setTrue(section)
            $(window).scroll(scrollHandler);
        }
    })



}

//setting the fetch to true after ajax call is successful 
function setTrue(section) {

    switch (section) {
        case 'culture':
            culture_fetched = true
            break;
        case 'opinion':
            opinion_fetched = true
            break;
        case 'features':
            features_fetched = true
            break;
        case 'sports':
            sports_fetched = true
            break;
        case 'science':
            science_fetched = true
            break;
    }

}


$(window).scroll(function scrollHandler() {
    //An ajax call will be sent when the user reaches the bottom of the window
    if ($(window).scrollTop() + $(window).height() == $(document).height()) {

        //fetch the culture first
        if (!culture_fetched) {
            $(window).off("scroll", scrollHandler);
            load_sections('culture', scrollHandler);
        }

        //if the culture section is fetched then fetch the sports section
        if (culture_fetched && !sports_fetched) {
            $(window).off("scroll", scrollHandler);
            load_sections('sports', scrollHandler)

        }

        //if the sports section is fetched then fetch the opinion section
        if (sports_fetched && !opinion_fetched) {
            $(window).off("scroll", scrollHandler);
            load_sections('opinion', scrollHandler)

        }

        //if the opinion section is fetched then fetch the features section 
        if (opinion_fetched && !features_fetched) {
            $(window).off("scroll", scrollHandler);
            load_sections('features', scrollHandler)
        }

        //if the features section is fetched then fetch the science section
        if (features_fetched && !science_fetched) {
            $(window).off("scroll", scrollHandler);
            load_sections('science', scrollHandler)
        }


    }
});