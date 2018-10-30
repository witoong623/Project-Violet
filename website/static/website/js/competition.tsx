import * as React from 'react'
import * as ReactDOM from 'react-dom'
import { observable, action, configure } from 'mobx';
import { observer } from "mobx-react";
import axios from 'axios';
import { Match } from './models';
import { CompetitionPageApi } from './transportlayers';

@observer
class RowTable extends React.Component<{match: Match}> {
  render() {
    const { match } = this.props;

    return (
      <tr>
        <td>{match.date}</td>
        <td>{match.home}</td>
        <td>{match.away}</td>
        <td>{match.homeScore !== null ? match.homeScore : '-'} {match.homeScore !== null && ' - '} {match.awayScore !== null && match.awayScore}</td>
        <td>
          <div className="form-check">
            <input id={match.matchId.toString()} className="form-check-input" type="checkbox" />
            <label className="form-check-label" htmlFor={match.matchId.toString()}>
              Watch this match
            </label>
          </div>
        </td>
      </tr>
    )
  }
}

@observer
class CompetitionPage extends React.Component<{store: CompetitionMatchStore}> {
  render() {
    const { matches } = this.props.store;
    let tableRows = matches.map(match => <RowTable key={match.matchId} match={match} />)

    return (
      <table className="table table-bordered">
        <thead>
          <tr>
            <td>Date</td>
            <td>Home team</td>
            <td>Away team</td>
            <td>Score</td>
            <td>Watch?</td>
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

  constructor(public competitionPageApi: CompetitionPageApi) {
    this.fetchMatchList();
  }

  private async fetchMatchList(): Promise<void> {
    let matchList = await this.competitionPageApi.fetchMatchList();
    matchList.forEach(matchJson => this.updateMatchFromServer(matchJson));
  }

  private fetchUserWatchHistory() {
    this.competitionPageApi.fetchUserWatchHistory()
      .then(data => {
        data.forEach((userWatch: any) => this.updateMatchIsWatchFromServer(userWatch));
      });
  }

  async fetchNextMatchList(): Promise<void> {
    await this.fetchMatchList();
  }

  @action.bound
  updateMatchFromServer(matchJson: any) {
    let match = new Match(matchJson.id);
    match.updateFromJson(matchJson);
    this.matches.push(match);
  }

  updateMatchIsWatchFromServer(userWatch: any) {

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
