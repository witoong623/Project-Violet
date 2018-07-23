import React, { Component } from 'react';
import CheckBox from './CheckBox';

function range(size, startAt = 0) {
  return [...Array(size).keys()].map(i => i + startAt);
}

class SetupForm extends Component {
  constructor(props) {
    super(props);

    this.state = {
      case: ['u1', 'u11'],
      selectedCase: ''
    }
  }

  render() {
    let u1MatchCount = range(39, 2).map((num, index) => <CheckBox key={index} number={num} />);

    return (
      <form>
        <div className="form-row">
          <div className="form-group">
            <label htmlFor="user-select">เลือกผู้ใช้</label>
            <select className="form-control" id="user-select">
              {this.state.case.map((user, index) =>
                <option key={index} value={user}>{user}</option>
              )}
            </select>
          </div>
        </div>
        <div className="form-row">
          {u1MatchCount}
        </div>
      </form>
    )
  }
}

export default SetupForm;