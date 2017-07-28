var AUTOPLAY_SPEED = 5000; //ms

function registerWidget() {
  $('.js-carousel').each(function() {
    var carousel = $(this);
    carousel.currentSlide = 0;
    carousel.slides = [];

    carousel.find('.js-carousel__item').each(function(i) {
      var item = $(this);
      item.slideIndex = i;
      carousel.slides.push(item);
    });

    var numSlides = carousel.slides.length;

    if (numSlides > 1) {
      carousel.setSlide = function(n) {
        carousel.currentSlide = n;

        if (carousel.currentSlide >= numSlides) {
          carousel.currentSlide = 0;
        } else if (carousel.currentSlide < 0) {
          carousel.currentSlide = numSlides - 1;
        }

        var slideToActivate = carousel.slides[carousel.currentSlide];
        $.each(carousel.slides, function(i, slide) {
          if (slide.css('display') != 'none') {
            slide.animate({ opacity: 0 }, 100, 'linear', function() {
              slide.css('display', 'none')

              slideToActivate.css('opacity', 0);
              slideToActivate.css('display', 'block');
              slideToActivate.animate({ opacity: 1 }, 600, 'linear');
            });
          }
        });

        $.each(carouselButtons, function(i, button) {
          button.removeClass('carousel-button--active');
          if (carousel.currentSlide == i) {
            button.addClass('carousel-button--active');
          }
        })
      };

      var startAutoplay = function() {
        carousel.interval = setInterval(function() {
          carousel.setSlide(carousel.currentSlide + 1);
        }, AUTOPLAY_SPEED);
      };

      var carouselButtons = [];
      var buttonRow = $('<div>', { class: 'carousel-button-row' });
      carousel.append(buttonRow);
      for (var j = 0; j < carousel.slides.length; j++) {
        var button = $('<div>', {
          class: 'carousel-button' + (!j ? ' carousel-button--active' : ''),
          'data-index': j
        });

        button.click(function() {
          var i = $(this).data('index')
          carousel.setSlide(i);
          clearInterval(carousel.interval);

          // restart autoplay after some time
          carousel.interval = setTimeout(startAutoplay, AUTOPLAY_SPEED / 2);
        });

        buttonRow.append(button)
        carouselButtons.push(button);
      }

      startAutoplay();
    }
  });
}

module.exports = registerWidget
