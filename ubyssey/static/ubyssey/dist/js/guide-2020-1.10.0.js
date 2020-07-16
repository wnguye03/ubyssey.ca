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
/******/ 	return __webpack_require__(__webpack_require__.s = "./src/js/guide-2020.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/js/guide-2020.js":
/*!******************************!*\
  !*** ./src/js/guide-2020.js ***!
  \******************************/
/*! no static exports found */
/***/ (function(module, exports) {

var colors = {
  colorHome: "#0073A9",
  colorAdulting: "#59A3AC",
  colorAcademics: "#FBCC80",
  colorSDP: "#E2BEB0",
  colorVancouver: "#EA8392",
  colorUBC: "#002145"
};
$(document).ready(function () {
  checkFooter();
  $('#c-nav-home').hover(function (e) {
    e.stopPropagation();
    $('.c-home-more').finish();
    $('.c-home-more').slideToggle(300);
  }, function (e) {
    e.stopPropagation();
    $('.c-home-more').finish();
    $('.c-home-more').fadeOut(300);
  });
});
$(window).resize(function () {
  checkFooter();
});

function checkFooter() {
  if (window.screen.width < 500) {
    if (window.location.href.indexOf("academics") > -1) {
      if (document.getElementById("footer-academics") != null) {
        document.getElementById("footer-academics").style.display = 'block';
      }
    } else if (window.location.href.indexOf("adulting") > -1) {
      if (document.getElementById("footer-adulting") != null) {
        document.getElementById("footer-adulting").style.display = 'block';
      }
    } else if (window.location.href.indexOf("sdp") > -1) {
      if (document.getElementById("footer-sdp") != null) {
        document.getElementById("footer-sdp").style.display = 'block';
      }
    } else if (window.location.href.indexOf("vancouver") > -1) {
      if (document.getElementById("footer-vancouver") != null) {
        document.getElementById("footer-vancouver").style.display = 'block';
      }
    } else if (window.location.href.indexOf("ubc") > -1) {
      if (document.getElementById("footer-ubc") != null) {
        document.getElementById("footer-ubc").style.display = 'block';
      }
    } else {
      if (document.getElementById("footer-academics") != null) {
        document.getElementById("footer-academics").style.display = 'block';
      }

      if (document.getElementById("footer-adulting") != null) {
        document.getElementById("footer-adulting").style.display = 'block';
      }

      if (document.getElementById("footer-ubc") != null) {
        document.getElementById("footer-ubc").style.display = 'block';
      }

      if (document.getElementById("footer-vancouver") != null) {
        document.getElementById("footer-vancouver").style.display = 'block';
      }

      if (document.getElementById("footer-sdp") != null) {
        document.getElementById("footer-sdp").style.display = 'block';
      }
    }
  }
}

/***/ })

/******/ });
//# sourceMappingURL=guide-2020-1.10.0.js.map