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
/******/ 	return __webpack_require__(__webpack_require__.s = "./src/js/blockadblock.js");
/******/ })
/************************************************************************/
/******/ ({

/***/ "./src/js/blockadblock.js":
/*!********************************!*\
  !*** ./src/js/blockadblock.js ***!
  \********************************/
/*! no static exports found */
/***/ (function(module, exports) {

/*
 * BlockAdBlock 3.2.1
 * Copyright (c) 2015 Valentin Allaire <valentin.allaire@sitexw.fr>
 * Released under the MIT license
 * https://github.com/sitexw/BlockAdBlock
 */
(function (window) {
  var BlockAdBlock = function BlockAdBlock(options) {
    this._options = {
      checkOnLoad: false,
      resetOnEnd: false,
      loopCheckTime: 50,
      loopMaxNumber: 5,
      baitClass: 'pub_300x250 pub_300x250m pub_728x90 text-ad textAd text_ad text_ads text-ads text-ad-links',
      baitStyle: 'width: 1px !important; height: 1px !important; position: absolute !important; left: -10000px !important; top: -1000px !important;',
      debug: false
    };
    this._var = {
      version: '3.2.1',
      bait: null,
      checking: false,
      loop: null,
      loopNumber: 0,
      event: {
        detected: [],
        notDetected: []
      }
    };

    if (options !== undefined) {
      this.setOption(options);
    }

    var self = this;

    var eventCallback = function eventCallback() {
      setTimeout(function () {
        if (self._options.checkOnLoad === true) {
          if (self._options.debug === true) {
            self._log('onload->eventCallback', 'A check loading is launched');
          }

          if (self._var.bait === null) {
            self._creatBait();
          }

          setTimeout(function () {
            self.check();
          }, 1);
        }
      }, 1);
    };

    if (window.addEventListener !== undefined) {
      window.addEventListener('load', eventCallback, false);
    } else {
      window.attachEvent('onload', eventCallback);
    }
  };

  BlockAdBlock.prototype._options = null;
  BlockAdBlock.prototype._var = null;
  BlockAdBlock.prototype._bait = null;

  BlockAdBlock.prototype._log = function (method, message) {
    console.log('[BlockAdBlock][' + method + '] ' + message);
  };

  BlockAdBlock.prototype.setOption = function (options, value) {
    if (value !== undefined) {
      var key = options;
      options = {};
      options[key] = value;
    }

    for (var option in options) {
      this._options[option] = options[option];

      if (this._options.debug === true) {
        this._log('setOption', 'The option "' + option + '" he was assigned to "' + options[option] + '"');
      }
    }

    return this;
  };

  BlockAdBlock.prototype._creatBait = function () {
    var bait = document.createElement('div');
    bait.setAttribute('class', this._options.baitClass);
    bait.setAttribute('style', this._options.baitStyle);
    this._var.bait = window.document.body.appendChild(bait);
    this._var.bait.offsetParent;
    this._var.bait.offsetHeight;
    this._var.bait.offsetLeft;
    this._var.bait.offsetTop;
    this._var.bait.offsetWidth;
    this._var.bait.clientHeight;
    this._var.bait.clientWidth;

    if (this._options.debug === true) {
      this._log('_creatBait', 'Bait has been created');
    }
  };

  BlockAdBlock.prototype._destroyBait = function () {
    window.document.body.removeChild(this._var.bait);
    this._var.bait = null;

    if (this._options.debug === true) {
      this._log('_destroyBait', 'Bait has been removed');
    }
  };

  BlockAdBlock.prototype.check = function (loop) {
    if (loop === undefined) {
      loop = true;
    }

    if (this._options.debug === true) {
      this._log('check', 'An audit was requested ' + (loop === true ? 'with a' : 'without') + ' loop');
    }

    if (this._var.checking === true) {
      if (this._options.debug === true) {
        this._log('check', 'A check was canceled because there is already an ongoing');
      }

      return false;
    }

    this._var.checking = true;

    if (this._var.bait === null) {
      this._creatBait();
    }

    var self = this;
    this._var.loopNumber = 0;

    if (loop === true) {
      this._var.loop = setInterval(function () {
        self._checkBait(loop);
      }, this._options.loopCheckTime);
    }

    setTimeout(function () {
      self._checkBait(loop);
    }, 1);

    if (this._options.debug === true) {
      this._log('check', 'A check is in progress ...');
    }

    return true;
  };

  BlockAdBlock.prototype._checkBait = function (loop) {
    var detected = false;

    if (this._var.bait === null) {
      this._creatBait();
    }

    if (window.document.body.getAttribute('abp') !== null || this._var.bait.offsetParent === null || this._var.bait.offsetHeight == 0 || this._var.bait.offsetLeft == 0 || this._var.bait.offsetTop == 0 || this._var.bait.offsetWidth == 0 || this._var.bait.clientHeight == 0 || this._var.bait.clientWidth == 0) {
      detected = true;
    }

    if (window.getComputedStyle !== undefined) {
      var baitTemp = window.getComputedStyle(this._var.bait, null);

      if (baitTemp && (baitTemp.getPropertyValue('display') == 'none' || baitTemp.getPropertyValue('visibility') == 'hidden')) {
        detected = true;
      }
    }

    if (this._options.debug === true) {
      this._log('_checkBait', 'A check (' + (this._var.loopNumber + 1) + '/' + this._options.loopMaxNumber + ' ~' + (1 + this._var.loopNumber * this._options.loopCheckTime) + 'ms) was conducted and detection is ' + (detected === true ? 'positive' : 'negative'));
    }

    if (loop === true) {
      this._var.loopNumber++;

      if (this._var.loopNumber >= this._options.loopMaxNumber) {
        this._stopLoop();
      }
    }

    if (detected === true) {
      this._stopLoop();

      this._destroyBait();

      this.emitEvent(true);

      if (loop === true) {
        this._var.checking = false;
      }
    } else if (this._var.loop === null || loop === false) {
      this._destroyBait();

      this.emitEvent(false);

      if (loop === true) {
        this._var.checking = false;
      }
    }
  };

  BlockAdBlock.prototype._stopLoop = function (detected) {
    clearInterval(this._var.loop);
    this._var.loop = null;
    this._var.loopNumber = 0;

    if (this._options.debug === true) {
      this._log('_stopLoop', 'A loop has been stopped');
    }
  };

  BlockAdBlock.prototype.emitEvent = function (detected) {
    if (this._options.debug === true) {
      this._log('emitEvent', 'An event with a ' + (detected === true ? 'positive' : 'negative') + ' detection was called');
    }

    var fns = this._var.event[detected === true ? 'detected' : 'notDetected'];

    for (var i in fns) {
      if (this._options.debug === true) {
        this._log('emitEvent', 'Call function ' + (parseInt(i) + 1) + '/' + fns.length);
      }

      if (fns.hasOwnProperty(i)) {
        fns[i]();
      }
    }

    if (this._options.resetOnEnd === true) {
      this.clearEvent();
    }

    return this;
  };

  BlockAdBlock.prototype.clearEvent = function () {
    this._var.event.detected = [];
    this._var.event.notDetected = [];

    if (this._options.debug === true) {
      this._log('clearEvent', 'The event list has been cleared');
    }
  };

  BlockAdBlock.prototype.on = function (detected, fn) {
    this._var.event[detected === true ? 'detected' : 'notDetected'].push(fn);

    if (this._options.debug === true) {
      this._log('on', 'A type of event "' + (detected === true ? 'detected' : 'notDetected') + '" was added');
    }

    return this;
  };

  BlockAdBlock.prototype.onDetected = function (fn) {
    return this.on(true, fn);
  };

  BlockAdBlock.prototype.onNotDetected = function (fn) {
    return this.on(false, fn);
  };

  window.BlockAdBlock = BlockAdBlock;

  if (window.blockAdBlock === undefined) {
    window.blockAdBlock = new BlockAdBlock({
      checkOnLoad: true,
      resetOnEnd: true
    });
  }
})(window);

/***/ })

/******/ });
//# sourceMappingURL=blockadblock-1.10.0.js.map