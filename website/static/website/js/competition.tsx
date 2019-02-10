import * as React from 'react'
import * as ReactDOM from 'react-dom'
import { observable, action, configure, runInAction } from 'mobx';
import { observer } from "mobx-react";
import axios from 'axios';
import { Match } from './models';
import { CompetitionPageApi } from './transportlayers';

axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.xsrfCookieName = 'csrftoken';

configure({
  enforceActions: 'observed'
});

@observer
class RowTable extends React.Component<{match: Match, isAuthenticate: boolean}> {
  @action.bound
  handleInputChange(event: any) {
    this.props.match.isWatch = event.target.checked;

    if (this.props.match.isWatch) {
      axios.post('/userwatchhistory/', { match: this.props.match.matchId })
        .then(action(res => {
        }))
        .catch(action(err => {
          this.props.match.isWatch = false;
        }));
    } else {
      axios.delete(`/userwatchhistory/${this.props.match.watchId}/`)
        .then(action(res => {
        }))
        .catch(action(err => {
          this.props.match.isWatch = true;
        }));
    }
    
  }
  
  render() {
    const { match, isAuthenticate } = this.props;

    return (
      <tr>
        <td>{match.date}</td>
        <td>{match.home}</td>
        <td>{match.away}</td>
        <td>{match.homeScore !== null ? match.homeScore : '-'} {match.homeScore !== null && ' - '} {match.awayScore !== null && match.awayScore}</td>
        {isAuthenticate &&
          <td>
            <div className="form-check">
              <input id={match.matchId.toString()} className="form-check-input" type="checkbox" checked={match.isWatch} onChange={this.handleInputChange} />
              <label className="form-check-label" htmlFor={match.matchId.toString()}>
                Watch this match
              </label>
            </div>
          </td>
        }
      </tr>
    )
  }
}

@observer
class CompetitionPage extends React.Component<{store: CompetitionMatchStore}> {
  render() {
    const { matches } = this.props.store;
    let tableRows = matches.map(match => <RowTable key={match.matchId} match={match} isAuthenticate={store.isAuthenticate} />)

    return (
      <table className="table table-bordered">
        <thead>
          <tr className="thead-light">
            <th>Date</th>
            <th>Home team</th>
            <th>Away team</th>
            <th>Score</th>
            {this.props.store.isAuthenticate &&
              <th>Watch?</th>
            }
          </tr>
        </thead>
        <tbody>
          {tableRows}
        </tbody>
      </table>
    )
  }
}

class CompetitionMatchStore {
  @observable matches: Array<Match> = new Array<Match>();
  @observable isAuthenticate: boolean;
  private userWatchHistory: Array<any> = new Array<any>();

  constructor(public competitionPageApi: CompetitionPageApi) {
    this.fetchUserWatchHistory()
      .then(() => this.fetchMatchList());
  }

  private async fetchMatchList(): Promise<void> {
    let matchList = await this.competitionPageApi.fetchMatchList();
    matchList.forEach(matchJson => this.updateMatchFromServer(matchJson));
  }

  async fetchNextMatchList(): Promise<void> {
    await this.fetchMatchList();
  }

  private fetchUserWatchHistory(): Promise<void> {
    return this.competitionPageApi.fetchUserWatchHistory()
      .then(data => {
        if (data === null) {
          runInAction(() => this.isAuthenticate = false);
          return;
        } else {
          runInAction(() => this.isAuthenticate = true);
        }
        this.userWatchHistory = data;
      });
  }

  @action.bound
  updateMatchFromServer(matchJson: any) {
    let match = new Match(matchJson.id);
    match.updateFromJson(matchJson);

    if (this.userWatchHistory.length > 0) {
      let found = this.userWatchHistory.find(uw => uw.match === match.matchId);
      if (found) {
        match.isWatch = true;
        match.watchId = found.id;
      }
    }

    this.matches.push(match);
  }
}

// to surpress error on window global object
declare global {
  interface Window { competitionId: string }
}

let api = new CompetitionPageApi(window.competitionId);
let store = new CompetitionMatchStore(api);

let element = <CompetitionPage store={store} />
ReactDOM.render(
  element,
  document.getElementById('react')
);

window.onscroll = () => {
  if (
    window.innerHeight + document.documentElement.scrollTop
    === document.documentElement.offsetHeight
  ) {
    store.fetchNextMatchList();
  }
}
