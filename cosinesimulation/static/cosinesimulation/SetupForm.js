var _jsxFileName = 'react\\SetupForm.js';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

function _toConsumableArray(arr) { if (Array.isArray(arr)) { for (var i = 0, arr2 = Array(arr.length); i < arr.length; i++) { arr2[i] = arr[i]; } return arr2; } else { return Array.from(arr); } }

import React, { Component } from 'react';
import CheckBox from './CheckBox';

function range(size) {
  var startAt = arguments.length > 1 && arguments[1] !== undefined ? arguments[1] : 0;

  return [].concat(_toConsumableArray(Array(size).keys())).map(function (i) {
    return i + startAt;
  });
}

var SetupForm = function (_Component) {
  _inherits(SetupForm, _Component);

  function SetupForm(props) {
    _classCallCheck(this, SetupForm);

    var _this = _possibleConstructorReturn(this, (SetupForm.__proto__ || Object.getPrototypeOf(SetupForm)).call(this, props));

    _this.state = {
      case: ['u1', 'u11'],
      selectedCase: ''
    };
    return _this;
  }

  _createClass(SetupForm, [{
    key: 'render',
    value: function render() {
      var _this2 = this;

      var u1MatchCount = range(39, 2).map(function (num, index) {
        return React.createElement(CheckBox, { key: index, number: num, __source: {
            fileName: _jsxFileName,
            lineNumber: 19
          },
          __self: _this2
        });
      });

      return React.createElement(
        'form',
        {
          __source: {
            fileName: _jsxFileName,
            lineNumber: 22
          },
          __self: this
        },
        React.createElement(
          'div',
          { className: 'form-row', __source: {
              fileName: _jsxFileName,
              lineNumber: 23
            },
            __self: this
          },
          React.createElement(
            'div',
            { className: 'form-group', __source: {
                fileName: _jsxFileName,
                lineNumber: 24
              },
              __self: this
            },
            React.createElement(
              'label',
              { htmlFor: 'user-select', __source: {
                  fileName: _jsxFileName,
                  lineNumber: 25
                },
                __self: this
              },
              '\u0E40\u0E25\u0E37\u0E2D\u0E01\u0E1C\u0E39\u0E49\u0E43\u0E0A\u0E49'
            ),
            React.createElement(
              'select',
              { className: 'form-control', id: 'user-select', __source: {
                  fileName: _jsxFileName,
                  lineNumber: 26
                },
                __self: this
              },
              this.state.case.map(function (user, index) {
                return React.createElement(
                  'option',
                  { key: index, value: user, __source: {
                      fileName: _jsxFileName,
                      lineNumber: 28
                    },
                    __self: _this2
                  },
                  user
                );
              })
            )
          )
        ),
        React.createElement(
          'div',
          { className: 'form-row', __source: {
              fileName: _jsxFileName,
              lineNumber: 33
            },
            __self: this
          },
          u1MatchCount
        )
      );
    }
  }]);

  return SetupForm;
}(Component);

export default SetupForm;