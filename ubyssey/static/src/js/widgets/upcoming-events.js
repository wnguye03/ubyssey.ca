function registerWidget() {
  $('.carousel').each(function() {
    var carousel = $(this);
    carousel.currentSlide = 0;
    carousel.slides = [];

    carousel.find('.carousel-item').each(function(i) {
      var item = $(this);
      item.slideIndex = i;
      carousel.slides.push(item);
    });

    var numSlides = carousel.slides.length;

    if (numSlides > 1) {
      carousel.moveSlide = function(n) {
        carousel.currentSlide += n;

        if (carousel.currentSlide >= numSlides) {
          carousel.currentSlide = 0;
        } else if (carousel.currentSlide < 0) {
          carousel.currentSlide = numSlides - 1;
        }

        $.each(carousel.slides, function(i, slide) {
          if (slide.slideIndex == carousel.currentSlide) {
              slide.css('display', 'block');
          } else {
            slide.css('display', 'none');
          }
        });
      };

      // "autoplay"
      carousel.interval = setInterval(function() {
        carousel.moveSlide(1);
      }, 5000);

      var left = $('<div>', { 'class': 'carousel-left fa fa-arrow-circle-left' });
      left.click(function() {
        carousel.moveSlide(-1);
        clearInterval(carousel.interval); // disable autoplay
      });

      var right = $('<div>', { 'class': 'carousel-right fa fa-arrow-circle-right' });
      right.click(function() {
        carousel.moveSlide(1);
        clearInterval(carousel.interval);
      });

      carousel.append(left);
      carousel.append(right);
    }
  });
}

module.exports = registerWidget
