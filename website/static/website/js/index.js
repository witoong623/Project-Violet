import React from 'react'
import ReactDOM from 'react-dom'
import { observable } from 'mobx';
import { observer } from "mobx-react";
import DevTools from 'mobx-react-devtools';
import axios from 'axios';

const dateFormatOption = {
  day: 'numeric',
  month: 'long',
  year: 'numeric',
  hour: 'numeric',
  minute: 'numeric'
}

class ProjectVioletApi {
  fetchUpcommingMatches() {
    return axios.get('/upcomming-matches')
      .then(res => res.data);
  }

  fetchUserWatchHistory() {
    return axios.get('/userwatchhistory')
      .then(res => res.data);
  }
}

class MatchesStore {
  @observable matches = [];
  projectVioletApi;

  constructor(projectVioletApi) {
    this.projectVioletApi = projectVioletApi;
    this.fetchUpcommingMatches();
  }

  fetchUpcommingMatches() {
    this.projectVioletApi.fetchUpcommingMatches().then(matches => {
      matches.forEach(matchJson => this.updateMatchFromServer(matchJson))
    }).then(() => this.fetchUserWatchHistory());
  }

  fetchUserWatchHistory() {
    this.projectVioletApi.fetchUserWatchHistory()
      .then(data => {
        data.forEach(userWatch => this.updateMatchIsWatchFromServer(userWatch));
      })
      .catch(err => {
        if (err.request.status === 403) {
          // unauthenticate, anonymous user
          return;
        } else if (err.request) {
          // The request was made but no response was received, log then ignore
          console.log(err.request);
          return;
        } else {
          throw err;
        }
      });
  }

  updateMatchFromServer(matchJson) {
    let match = this.matches.find(match => match.id === matchJson.id);

    if (!match) {
      match = new Match(matchJson.id, matchJson.home_team, matchJson.away_team, new Date(matchJson.date).toLocaleDateString('th-TH', dateFormatOption),
        matchJson.home_logo, matchJson.away_logo, false);
      this.matches.push(match);
    }
  }

  updateMatchIsWatchFromServer(userWatch) {
    let match = this.matches.find(match => match.id === userWatch.match);

    if (match) {
      match.isWatch = true;
    }
  }
}

class Match {
  @observable isWatch = false;

  constructor(id, home, away, date, homeLogo, awayLogo, isWatch) {
    this.id = id;
    this.home = home;
    this.away = away;
    this.date = date;
    this.homeLogo = homeLogo;
    this.awayLogo = awayLogo;
    this.isWatch = isWatch;
  }
}

@observer class MatchEntry extends React.Component {
  constructor(props) {
    super(props);
    
    this.handleInputChange = this.handleInputChange.bind(this);
  }

  handleInputChange(event) {
    this.props.match.isWatch = event.target.checked;
  }

  render() {
    const watchBadge = this.props.match.isWatch ? (
      <div className="match-card-badge">
        <span className="badge badge-success">Watched</span>
      </div>
    ) : (
      <div className="match-card-badge" style={{visibility: "hidden"}}>
        <span className="badge badge-success">Watched</span>
      </div>
    );

    return (
      <div className="col-sm">
        <div className="match-card">
          {watchBadge}
          <div className="match-card-logo">
            <img src={this.props.match.homeLogo} height="90" />
            <h6>VS</h6>
            <img src={this.props.match.awayLogo} height="90" />
          </div>
          <div className="match-card-body">
            <h5>{this.props.match.home}</h5>
            <p>VS</p>
            <h5>{this.props.match.away}</h5>
            <h6>{this.props.match.date}</h6>
          </div>
          <div className="match-card-control">
            <div className="form-check">
              <input className="form-check-input" type="checkbox" checked={this.props.match.isWatch} id="iswatch" onChange={this.handleInputChange} />
              <label className="form-check-label" htmlFor="iswatch">
                Watch this match
              </label>
            </div>
          </div>
        </div>
      </div>
    )
  }
}


@observer class MatchesSection extends React.Component {
  render() {
    const entries = this.props.matchesStore.matches.map(match => <MatchEntry key={match.id} match={match} />);
    const rows = [];

    for (let i = 0; i < entries.length; i+=4) {
      let row = [];
      row.push(entries.slice(i, i + 4));
      rows.push(row);
    }

    return (
      <div>
        {rows.map((row, index) => <div key={index} className="row">{row}</div>)}
        <DevTools />
      </div>
    )
  }
}

const api = new ProjectVioletApi();
const store = new MatchesStore(api);

const element = <MatchesSection matchesStore={store} />;
ReactDOM.render(
  element,
  document.getElementById('react')
);