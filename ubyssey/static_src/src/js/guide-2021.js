function dropDownHeader(dropDownParentName, dropDownName) {
    $(dropDownParentName).hover(function (e) {
        e.stopPropagation();
        $(dropDownName).finish();
        $(dropDownName).slideToggle(200);
    }, (function (e) {
        e.stopPropagation();
        $(dropDownName).finish();
        $(dropDownName).hide();
    })
    );
}


$(document).ready(function () {
    dropDownHeader('#c-nav-home-mobile', '.c-home-more');
    dropDownHeader('#c-nav-home-tablet', '.c-home-more');
    dropDownHeader('.c-nav-current', '#c-section-more--current');
    dropDownHeader('#c-nav-section--academic', '#c-section-more--academic');
    dropDownHeader('#c-nav-section--ubc', '#c-section-more--ubc');
    dropDownHeader('#c-nav-section--adulting', '#c-section-more--adulting');
    dropDownHeader('#c-nav-section--sdp', '#c-section-more--sdp');
    dropDownHeader('#c-nav-section--vancouver', '#c-section-more--vancouver');
});