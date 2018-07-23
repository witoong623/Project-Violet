var _jsxFileName = "react\\CheckBox.js";

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

import React, { Component } from 'react';

var CheckBox = function (_Component) {
  _inherits(CheckBox, _Component);

  function CheckBox(props) {
    _classCallCheck(this, CheckBox);

    return _possibleConstructorReturn(this, (CheckBox.__proto__ || Object.getPrototypeOf(CheckBox)).call(this, props));
  }

  _createClass(CheckBox, [{
    key: "render",
    value: function render() {
      var inputId = "matchNo" + this.props.number;

      return React.createElement(
        "div",
        { className: "form-check", __source: {
            fileName: _jsxFileName,
            lineNumber: 12
          },
          __self: this
        },
        React.createElement("input", { className: "form-check-input", type: "checkbox", value: "", id: inputId, __source: {
            fileName: _jsxFileName,
            lineNumber: 13
          },
          __self: this
        }),
        React.createElement(
          "label",
          { className: "form-check-label", htmlFor: inputId, __source: {
              fileName: _jsxFileName,
              lineNumber: 14
            },
            __self: this
          },
          this.props.number
        )
      );
    }
  }]);

  return CheckBox;
}(Component);

export default CheckBox;