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
/******/ 	return __webpack_require__(__webpack_require__.s = "./src/js/one-year-later.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/js/one-year-later.js":
/*!**********************************!*\
  !*** ./src/js/one-year-later.js ***!
  \**********************************/
/*! no static exports found */
/***/ (function(module, exports) {

function updateHeader() {
  var scrollTop = $(window).scrollTop();
  var element = $('.js-sticky');
  var elementHeight = element.height(),
      elementOffset = $(window).height() - elementHeight,
      parentOffset = element.parent().offset().top,
      parentHeight = element.parent().height();

  if (parentHeight <= elementHeight) {
    return;
  }

  var hasClass = element.hasClass('js-sticky--fixed'),
      shouldStick = scrollTop > elementOffset,
      shouldFreeze = scrollTop + elementOffset + elementHeight >= parentOffset + parentHeight;

  if (shouldStick) {
    if (!hasClass) {
      element.removeClass('js-sticky--frozen');
      element.addClass('js-sticky--fixed');
      element.css('top', element.data('offset') + 'px');
    }
  } else if (hasClass) {
    element.removeClass('js-sticky--fixed');
  }
}

function updateVideo() {
  var header = $('.oyl-header__container');

  if (header.width() / header.height() < 1.77) {
    $('#header-video').addClass('vertical');
  } else {
    $('#header-video').removeClass('vertical');
  }
}

$(function () {
  updateVideo();
  updateHeader();
  var vid = document.getElementById('header-video');

  vid.ontimeupdate = function () {
    var timeRemaining = vid.duration - vid.currentTime;

    if (timeRemaining < 5) {
      $('.oyl-header__shadow').addClass('is-visible');
    }

    if (timeRemaining < 3) {
      $('.oyl-article__header').addClass('is-visible');
    }
  };

  $(window).scroll(updateHeader);
  $(window).resize(updateVideo);
});

/***/ })

/******/ });
//# sourceMappingURL=one-year-later-1.10.0.js.map