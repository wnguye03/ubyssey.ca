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
/******/ 	return __webpack_require__(__webpack_require__.s = "./src/js/dfp.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/js/dfp.js":
/*!***********************!*\
  !*** ./src/js/dfp.js ***!
  \***********************/
/*! no static exports found */
/***/ (function(module, exports) {

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } }

function _createClass(Constructor, protoProps, staticProps) { if (protoProps) _defineProperties(Constructor.prototype, protoProps); if (staticProps) _defineProperties(Constructor, staticProps); return Constructor; }

var SIZES = {
  'box': [300, 250],
  'skyscraper': [[300, 250], [300, 600]],
  'banner': [468, 60],
  'leaderboard': [[728, 90], [970, 90]],
  'mobile-leaderboard': [300, 50]
}; // Get reference to googletag from window object

var googletag = window.googletag;

var DFP = /*#__PURE__*/function () {
  function DFP() {
    _classCallCheck(this, DFP);

    this.adslots = [];
    this.element = document;
  }

  _createClass(DFP, [{
    key: "collectAds",
    value: function collectAds() {
      var _this = this;

      var dfpslots = $(this.element).find('.adslot').filter(':visible');
      $(dfpslots).each(function (_, dfpslot) {
        var slotName = $(dfpslot).attr('id'); // only reload the slot if its new

        var priorSlotNames = _this.adslots.reduce(function (acc, val) {
          return acc.concat(val);
        }, []);

        if (!priorSlotNames.includes(slotName)) {
          var slot = googletag.defineSlot("/61222807/".concat($(dfpslot).data('dfp')), SIZES[$(dfpslot).data('size')], slotName).setCollapseEmptyDiv(true).addService(googletag.pubads());

          _this.adslots.push([slotName, slot]);
        }
      });
    }
  }, {
    key: "refreshAds",
    value: function refreshAds() {
      this.adslots.forEach(function (slot) {
        googletag.display(slot[0]); // googletag.pubads().refresh([slot[1]]);

        googletag.pubads().refresh();
      });
    }
  }, {
    key: "load",
    value: function load(element) {
      this.element = element;
      googletag.cmd.push(DFP.setup);
      googletag.cmd.push(this.collectAds.bind(this));
      googletag.cmd.push(this.refreshAds.bind(this));
    }
  }, {
    key: "reset",
    value: function reset() {
      this.adslots = [];
      googletag.cmd.push(googletag.destroySlots);
    }
  }], [{
    key: "setup",
    value: function setup() {
      // Infinite scroll requires SRA
      // grapefruit
      // googletag.pubads().enableSingleRequest();
      // Disable initial load, we will use refresh() to fetch ads.
      // Calling this function means that display() calls just
      // register the slot as ready, but do not fetch ads for it.
      googletag.pubads().disableInitialLoad(); // Enable services

      googletag.enableServices();
    }
  }]);

  return DFP;
}();

var dfp = new DFP();
$(document).ready(function () {
  dfp.load(document);
});

window.resetAds = function (element) {
  dfp.reset();
  dfp.load(element);
};

/***/ })

/******/ });
//# sourceMappingURL=dfp-1.10.0.js.map