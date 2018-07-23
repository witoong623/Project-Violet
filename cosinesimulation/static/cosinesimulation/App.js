var _jsxFileName = 'react\\App.js';

var _createClass = function () { function defineProperties(target, props) { for (var i = 0; i < props.length; i++) { var descriptor = props[i]; descriptor.enumerable = descriptor.enumerable || false; descriptor.configurable = true; if ("value" in descriptor) descriptor.writable = true; Object.defineProperty(target, descriptor.key, descriptor); } } return function (Constructor, protoProps, staticProps) { if (protoProps) defineProperties(Constructor.prototype, protoProps); if (staticProps) defineProperties(Constructor, staticProps); return Constructor; }; }();

function _classCallCheck(instance, Constructor) { if (!(instance instanceof Constructor)) { throw new TypeError("Cannot call a class as a function"); } }

function _possibleConstructorReturn(self, call) { if (!self) { throw new ReferenceError("this hasn't been initialised - super() hasn't been called"); } return call && (typeof call === "object" || typeof call === "function") ? call : self; }

function _inherits(subClass, superClass) { if (typeof superClass !== "function" && superClass !== null) { throw new TypeError("Super expression must either be null or a function, not " + typeof superClass); } subClass.prototype = Object.create(superClass && superClass.prototype, { constructor: { value: subClass, enumerable: false, writable: true, configurable: true } }); if (superClass) Object.setPrototypeOf ? Object.setPrototypeOf(subClass, superClass) : subClass.__proto__ = superClass; }

import React, { Component } from 'react';
import SetupForm from './SetupForm';

var App = function (_Component) {
  _inherits(App, _Component);

  function App() {
    _classCallCheck(this, App);

    return _possibleConstructorReturn(this, (App.__proto__ || Object.getPrototypeOf(App)).apply(this, arguments));
  }

  _createClass(App, [{
    key: 'render',
    value: function render() {
      return React.createElement(
        'div',
        {
          __source: {
            fileName: _jsxFileName,
            lineNumber: 7
          },
          __self: this
        },
        React.createElement(
          'h3',
          {
            __source: {
              fileName: _jsxFileName,
              lineNumber: 8
            },
            __self: this
          },
          'Cosine similarity simulation'
        ),
        React.createElement(
          'div',
          { className: 'row', __source: {
              fileName: _jsxFileName,
              lineNumber: 9
            },
            __self: this
          },
          React.createElement(
            'div',
            { className: 'col-md-12', __source: {
                fileName: _jsxFileName,
                lineNumber: 10
              },
              __self: this
            },
            React.createElement(SetupForm, {
              __source: {
                fileName: _jsxFileName,
                lineNumber: 11
              },
              __self: this
            })
          )
        )
      );
    }
  }]);

  return App;
}(Component);

var formContainer = document.querySelector('#formContainer');
ReactDOM.render(App, formContainer);