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

eval("__webpack_require__.r(__webpack_exports__);\n// Для зміни вигляду товарів при відкриванні/закриванні фільтрації\n\nconst filterDetails = document.getElementById(\"filter-details\");\nconst goodsList = document.getElementById(\"goods-list\");\n\nfilterDetails.addEventListener(\"toggle\", function () {\n   if (filterDetails.open) {\n      goodsList.classList.remove(\"filter-closed\");\n   } else {\n      goodsList.classList.add(\"filter-closed\");\n   }\n});\n\n\n// Реалізація інпута з ціною\nconst range = document.getElementById(\"input-left\");\nconst range2 = document.getElementById(\"input-right\");\n\nrange.addEventListener(\"input\", function () {\n   const value = this.value;\n   const min = this.min;\n   const max = this.max;\n   const percent = ((value - min) / (max - min)) * 100;\n   const percent2 =\n      ((range2.value - range2.min) / (range2.max - range2.min)) * 100;\n   document.querySelector(\".range\").style.left = percent + \"%\";\n   document.querySelector(\".thumb.left\").style.left = percent + \"%\";\n   document.querySelector(\".price__value-min\").innerText = this.value;\n});\n\nrange2.addEventListener(\"input\", function () {\n   const value = this.value;\n   const min = this.min;\n   const max = this.max;\n   const percent = ((value - min) / (max - min)) * 100;\n   const percent2 = ((range.value - range.min) / (range.max - range.min)) * 100;\n   document.querySelector(\".range\").style.right = 100 - percent + \"%\";\n   document.querySelector(\".thumb.right\").style.right = 100 - percent + \"%\";\n   document.querySelector(\".price__value-max\").innerText = this.value;\n});\n\n\n//# sourceURL=webpack://project/./src/js/script.js?");

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