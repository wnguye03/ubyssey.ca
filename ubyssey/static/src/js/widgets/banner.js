var MOBILE_BREAKPOINT = 960;
var DEFAULT_HOMEPAGE_PADDING = 55;

function registerBanner() {
  var banner = $('.c-banner');
  if (banner && banner[0]) {
    var mainOriginalHeight = parseInt($('main').css('padding-top'), 10);

    function bannerResize() {
      var height = $('.c-banner')[0].offsetHeight;
      var headerCount = 0;
      $('header').each(function() {
        if ($(this).hasClass('header-site') || $(this).hasClass('mobile')) {
          $(this).css('top', height);
          headerCount++;
        }
      });
      if (headerCount == 1 && $(window).width() < MOBILE_BREAKPOINT) {
        banner.css('position', 'fixed');
        var padding = DEFAULT_HOMEPAGE_PADDING + mainOriginalHeight + height;
        $('#search-form').css('top', height)
        $('main').css('padding-top', padding);
      } else if (headerCount == 2 || $(window).width() < MOBILE_BREAKPOINT) {
        banner.css('position', 'fixed');
        $('#search-form').css('top', height)
        $('main').css('padding-top', mainOriginalHeight + height);
      } else {
        banner.css('position', 'static');
        $('#search-form').css('top', 0)
        $('main').css('padding-top', mainOriginalHeight);
      }
    }
    bannerResize();

    $(window).resize(bannerResize);
  }
}

module.exports = registerBanner;
