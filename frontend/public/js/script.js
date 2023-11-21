/*
 * ATTENTION: The "eval" devtool has been used (maybe by default in mode: "development").
 * This devtool is neither made for production nor for readable output files.
 * It uses "eval()" calls to create a separate source file in the browser devtools.
 * If you are trying to read the output file, select a different devtool (https://webpack.js.org/configuration/devtool/)
 * or disable the default devtool with "devtool: false".
 * If you are looking for production-ready output files, see mode: "production" (https://webpack.js.org/configuration/mode/).
 */
/******/ (() => { // webpackBootstrap
/******/ 	"use strict";
/******/ 	var __webpack_modules__ = ({

/***/ "./src/js/script.js":
/*!**************************!*\
  !*** ./src/js/script.js ***!
  \**************************/
/***/ ((__unused_webpack___webpack_module__, __webpack_exports__, __webpack_require__) => {

eval("__webpack_require__.r(__webpack_exports__);\n// Для зміни вигляду товарів при відкриванні/закриванні фільтрації\r\n\r\nconst filterDetails = document.getElementById(\"filter-details\");\r\nconst goodsList = document.getElementById(\"goods-list\");\r\n\r\nfilterDetails.addEventListener(\"toggle\", function () {\r\n   if (filterDetails.open) {\r\n      goodsList.classList.remove(\"filter-closed\");\r\n   } else {\r\n      goodsList.classList.add(\"filter-closed\");\r\n   }\r\n});\r\n\r\n\r\n// Реалізація інпута з ціною\r\nconst range = document.getElementById(\"input-left\");\r\nconst range2 = document.getElementById(\"input-right\");\r\n\r\nrange.addEventListener(\"input\", function () {\r\n   const value = this.value;\r\n   const min = this.min;\r\n   const max = this.max;\r\n   const percent = ((value - min) / (max - min)) * 100;\r\n   const percent2 =\r\n      ((range2.value - range2.min) / (range2.max - range2.min)) * 100;\r\n   document.querySelector(\".range\").style.left = percent + \"%\";\r\n   document.querySelector(\".thumb.left\").style.left = percent + \"%\";\r\n   document.querySelector(\".price__value-min\").innerText = this.value;\r\n});\r\n\r\nrange2.addEventListener(\"input\", function () {\r\n   const value = this.value;\r\n   const min = this.min;\r\n   const max = this.max;\r\n   const percent = ((value - min) / (max - min)) * 100;\r\n   const percent2 = ((range.value - range.min) / (range.max - range.min)) * 100;\r\n   document.querySelector(\".range\").style.right = 100 - percent + \"%\";\r\n   document.querySelector(\".thumb.right\").style.right = 100 - percent + \"%\";\r\n   document.querySelector(\".price__value-max\").innerText = this.value;\r\n});\r\n\n\n//# sourceURL=webpack://project/./src/js/script.js?");

/***/ })

/******/ 	});
/************************************************************************/
/******/ 	// The require scope
/******/ 	var __webpack_require__ = {};
/******/ 	
/************************************************************************/
/******/ 	/* webpack/runtime/make namespace object */
/******/ 	(() => {
/******/ 		// define __esModule on exports
/******/ 		__webpack_require__.r = (exports) => {
/******/ 			if(typeof Symbol !== 'undefined' && Symbol.toStringTag) {
/******/ 				Object.defineProperty(exports, Symbol.toStringTag, { value: 'Module' });
/******/ 			}
/******/ 			Object.defineProperty(exports, '__esModule', { value: true });
/******/ 		};
/******/ 	})();
/******/ 	
/************************************************************************/
/******/ 	
/******/ 	// startup
/******/ 	// Load entry module and return exports
/******/ 	// This entry module can't be inlined because the eval devtool is used.
/******/ 	var __webpack_exports__ = {};
/******/ 	__webpack_modules__["./src/js/script.js"](0, __webpack_exports__, __webpack_require__);
/******/ 	
/******/ })()
;