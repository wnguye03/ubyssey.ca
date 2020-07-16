/******/ (function(modules) { // webpackBootstrap
/******/ 	// The module cache
/******/ 	var installedModules = {};
/******/
/******/ 	// The require function
/******/ 	function __webpack_require__(moduleId) {
/******/
/******/ 		// Check if module is in cache
/******/ 		if(installedModules[moduleId]) {
/******/ 			return installedModules[moduleId].exports;
/******/ 		}
/******/ 		// Create a new module (and put it into the cache)
/******/ 		var module = installedModules[moduleId] = {
/******/ 			i: moduleId,
/******/ 			l: false,
/******/ 			exports: {}
/******/ 		};
/******/
/******/ 		// Execute the module function
/******/ 		modules[moduleId].call(module.exports, module, module.exports, __webpack_require__);
/******/
/******/ 		// Flag the module as loaded
/******/ 		module.l = true;
/******/
/******/ 		// Return the exports of the module
/******/ 		return module.exports;
/******/ 	}
/******/
/******/
/******/ 	// expose the modules object (__webpack_modules__)
/******/ 	__webpack_require__.m = modules;
/******/
/******/ 	// expose the module cache
/******/ 	__webpack_require__.c = installedModules;
/******/
/******/ 	// define getter function for harmony exports
/******/ 	__webpack_require__.d = function(exports, name, getter) {
/******/ 		if(!__webpack_require__.o(exports, name)) {
/******/ 			Object.defineProperty(exports, name, { enumerable: true, get: getter });
/******/ 		}
/******/ 	};
/******/
/******/ 	// define __esModule on exports
/******/ 	__webpack_require__.r = function(exports) {
/******/ 		if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 			Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 		}
/******/ 		Object.defineProperty(exports, '__esModule', { value: true });
/******/ 	};
/******/
/******/ 	// create a fake namespace object
/******/ 	// mode & 1: value is a module id, require it
/******/ 	// mode & 2: merge all properties of value into the ns
/******/ 	// mode & 4: return value when already ns object
/******/ 	// mode & 8|1: behave like require
/******/ 	__webpack_require__.t = function(value, mode) {
/******/ 		if(mode & 1) value = __webpack_require__(value);
/******/ 		if(mode & 8) return value;
/******/ 		if((mode & 4) && typeof value === 'object' && value && value.__esModule) return value;
/******/ 		var ns = Object.create(null);
/******/ 		__webpack_require__.r(ns);
/******/ 		Object.defineProperty(ns, 'default', { enumerable: true, value: value });
/******/ 		if(mode & 2 && typeof value != 'string') for(var key in value) __webpack_require__.d(ns, key, function(key) { return value[key]; }.bind(null, key));
/******/ 		return ns;
/******/ 	};
/******/
/******/ 	// getDefaultExport function for compatibility with non-harmony modules
/******/ 	__webpack_require__.n = function(module) {
/******/ 		var getter = module && module.__esModule ?
/******/ 			function getDefault() { return module['default']; } :
/******/ 			function getModuleExports() { return module; };
/******/ 		__webpack_require__.d(getter, 'a', getter);
/******/ 		return getter;
/******/ 	};
/******/
/******/ 	// Object.prototype.hasOwnProperty.call
/******/ 	__webpack_require__.o = function(object, property) { return Object.prototype.hasOwnProperty.call(object, property); };
/******/
/******/ 	// __webpack_public_path__
/******/ 	__webpack_require__.p = "";
/******/
/******/
/******/ 	// Load entry module and return exports
/******/ 	return __webpack_require__(__webpack_require__.s = "./src/js/advertise_new.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/js/advertise_new.js":
/*!*********************************!*\
  !*** ./src/js/advertise_new.js ***!
  \*********************************/
/*! no static exports found */
/***/ (function(module, exports) {

// Scripts for the /advertise/ page
// Bundled as 'a.js' to prevent AdBlocker blocking.
$(function () {
  // Navigation links smooth scrolling
  $('a[href*=\\#]').on('click', function (e) {
    $('html,body').animate({
      scrollTop: $(this.hash).offset().top
    }, 500);
  });
  $('.o-placements--web .o-placements__placement').click(function () {
    $('.o-placements--web .o-placements__placement').removeClass('o-placements__placement--active');
    $(this).addClass('o-placements__placement--active');
    $('.o-placements--web .o-placements__demo__inner__right img').animate({
      left: $(this).data('horizontaloffset')
    }, 250, function () {//animation complete
    });
    $('.o-placements--web .o-placements__demo__inner__right img').css('top', $(this).data('offset'));
    $('.o-placements--web .o-placements__demo__inner__left img').css('top', $(this).data('offset'));
  });
  $('.o-placements--web .o-placements__platform--mode').click(function () {
    $('.o-placements--web .o-placements__platform--mode').removeClass('o-placements__platforms--active');
    $(this).addClass('o-placements__platforms--active');

    if ($(this).data('platform') == 'desktop') {
      $('.o-placements__demo__desktop').removeClass('o-hidden');
      $('.o-placements__demo__mobile').addClass('o-hidden');
      $('.o-placements__placement--demo--sidebar').removeClass('o-unavailable');
    } else {
      $('.o-placements__demo__desktop').addClass('o-hidden');
      $('.o-placements__demo__mobile').removeClass('o-hidden');
      $('.o-placements__placement--demo--sidebar').addClass('o-unavailable');
    }
  });
  $('.o-placements--print .o-placements__placement--demo').click(function () {
    $('.o-placements--print .o-placements__placement').removeClass('o-placements__placement--active');
    $(this).addClass('o-placements__placement--active');
    $('.o-placements--print .o-placements__demo').attr('data-demo', $(this).data('demo'));
  });
  $('.o-placements--guide .o-placements__placement--demo').click(function () {
    $('.o-placements--guide .o-placements__placement').removeClass('o-placements__placement--active');
    $(this).addClass('o-placements__placement--active');
    $('.o-placements--guide .o-placements__demo').attr('data-demo', $(this).data('demo'));
  }); // Open modal

  $('.c-production-schedule__view').click(function () {
    $('.c-production-schedule__modal').show();
  }); // Close modal

  $('.c-production-schedule__modal__close').click(function () {
    $('.c-production-schedule__modal').hide();
  });
  $('.c-production-schedule__modal').click(function () {
    $('.c-production-schedule__modal').hide();
  });
  $('.c-production-schedule__modal img').click(function (e) {
    e.stopPropagation();
  });
  $('.c-web-slider__point > div').click(function (e) {
    var offset = $(this).offset().left - $('.c-web-slider').offset().left;
    var content = $(this).data('content');
    var cost = $(this).data('cost');
    slideTo(offset, content, cost);
  });

  function slideTo(offset, content, cost) {
    var tooltipWidth = $('.c-web-slider__tooltip').outerWidth();
    var maxOffset = $('.c-web-slider').width() - tooltipWidth;
    offset = Math.max(0, offset - 25);
    $('.c-web-slider__tooltip').css('margin-left', Math.min(offset, maxOffset));
    var offsetPercent = 8;

    if (offset > maxOffset) {
      var offsetDif = offset - maxOffset + 35;
      offsetPercent = offsetDif / tooltipWidth * 100;
      offsetPercent = Math.min(92, offsetPercent);
    }

    $('.c-web-slider__tooltip__arrow').css('left', offsetPercent + '%');
    $('.c-web-slider__tooltip__content').html(content);
    $('.c-web-slider__tooltip__cost').text(cost);
  }
});

/***/ })

/******/ });
//# sourceMappingURL=a_new-1.10.0.js.map