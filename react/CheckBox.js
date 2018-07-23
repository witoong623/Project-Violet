import React, { Component } from 'react';

class CheckBox extends Component {
  constructor(props) {
    super(props);
  }

  render() {
    let inputId = `matchNo${this.props.number}`;

    return (
      <div className="form-check">
        <input className="form-check-input" type="checkbox" value="" id={inputId} />
        <label className="form-check-label" htmlFor={inputId}>
          {this.props.number}
        </label>
      </div>
    )
  }
}

export default CheckBox;