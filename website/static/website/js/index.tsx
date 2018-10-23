// @flow
import * as React from 'react'
import * as ReactDOM from 'react-dom'
import { observable, action, configure } from 'mobx';
import { observer } from "mobx-react";
import axios from 'axios';
import { Match } from './models';
import { MatchEntry } from './components/match-entry';

enum MatchType {
  TodayMatch = 'todayMatch',
  UpcommingMatch = 'upcommingMatch',
  RecentMatch = 'recentMatch'
}

const matchTypeBaseKeys: {[key:string]: number} = {
  todayMatch: 1,
  upcommingMatch: 100,
  recentMatch: 1000
}

axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.xsrfCookieName = 'csrftoken';

configure({
  enforceActions: 'observed'
});

class ProjectVioletApi {
  fetchUpcommingMatches(): Promise<any[]> {
    return axios.get('/upcomming-matches/')
      .then(res => res.data)
      .catch(err => {
        console.log(err);
        return new Array<any>();
      });
  }

  fetchRecentMatches(): Promise<any[]> {
    return axios.get('/recent-matches/')
      .then(res => res.data)
      .catch(err => {
        console.log(err);
        return new Array<any>();
      });
  }

  fetchTodayMatches(): Promise<any[]> {
    return axios.get('/today-matches/')
      .then(res => res.data)
      .catch(err => {
        console.log(err);
        return new Array<any>();
      });
  }

  fetchUserWatchHistory(): Promise<any[]> {
    return axios.get('/userwatchhistory/')
      .then(res => res.data)
      .catch(err => {
        if (err.request.status === 403) {
          // unauthenticate, anonymous user
          return new Array<any>();
        } else if (err.request) {
          // the request was made but no response was received, log then ignore
          console.log(err.request);
          return;
        } else {
          // unknown error, throw it
          throw err;
        }
      });
  }
}

class MatchesStore {
  @observable matches: Array<Match> = new Array<Match>();
  @observable todayMatches: Array<Match> = new Array<Match>();
  @observable upcommingMatches: Array<Match> = new Array<Match>();
  @observable recentMatches: Array<Match> = new Array<Match>();

  constructor(public projectVioletApi: ProjectVioletApi) {
    this.projectVioletApi = projectVioletApi;
    this.fetchUpcommingMatches()
      .then(() =>this.fetchUserWatchHistory());
  }

  async fetchUpcommingMatches() {
    let upcommingMatches = await this.projectVioletApi.fetchUpcommingMatches();
    upcommingMatches.forEach((matchJson: any) => this.updateMatchFromServer(matchJson, this.upcommingMatches));
    let todayMatches = await this.projectVioletApi.fetchTodayMatches();
    todayMatches.forEach(matchJosn => this.updateMatchFromServer(matchJosn, this.todayMatches));
    let recentMatches = await this.projectVioletApi.fetchRecentMatches();
    recentMatches.forEach(matchJson => this.updateMatchFromServer(matchJson, this.recentMatches));
  }

  fetchUserWatchHistory() {
    this.projectVioletApi.fetchUserWatchHistory()
      .then(data => {
        data.forEach((userWatch: any) => this.updateMatchIsWatchFromServer(userWatch));
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

  @action.bound
  updateMatchFromServer(matchJson: any, storeArray: Array<Match>) {
    let match = new Match(matchJson.id);
    match.updateFromJson(matchJson);
    storeArray.push(match);
  }

  updateMatchIsWatchFromServer(userWatch: any) {
    // find in every stores since every matches can be watched
    let match = this.recentMatches.find(match => match.matchId === userWatch.match);
    if (match) {
      this.performUpdateMatchIsWatch(match, userWatch);
      return;
    }

    match = this.upcommingMatches.find(match => match.matchId === userWatch.match);
    if (match) {
      this.performUpdateMatchIsWatch(match, userWatch);
      return;
    }

    match = this.todayMatches.find(match => match.matchId === userWatch.match);
    if (match) {
      this.performUpdateMatchIsWatch(match, userWatch);
      return;
    }
  }

  @action.bound
  performUpdateMatchIsWatch(match: Match, userWatch: any) {
    match.isWatch = true;
    match.watchId = userWatch.id;
  }
}


@observer class MatchesSection extends React.Component<{matches: Array<Match>, matchType: MatchType}> {
  render() {
    const { matches, matchType } = this.props;
    const baseKey = matchTypeBaseKeys[matchType];

    const entries = matches.map(match => <MatchEntry key={match.matchId} match={match} />);
    const rows = [];

    for (let i = 0; i < entries.length; i+=4) {
      let row = [];
      row.push(entries.slice(i, i + 4));
      rows.push(row);
    }

    return (
      <div>
        {rows.map((row, index) => <div key={index + baseKey} className="row">{row}</div>)}
      </div>
    );
  }
}

@observer
class IndexPage extends React.Component<{matchesStore: MatchesStore}> {
  render() {
    const { matchesStore } = this.props;

    const todayMatchesSection = matchesStore.todayMatches.length > 0 ? (
      <MatchesSection matchType={MatchType.TodayMatch} matches={matchesStore.todayMatches} />
    ) : (
      <div className="alert alert-info" role="alert">
        No match today.
      </div>
    );

    const upcommingMatchesSection = matchesStore.upcommingMatches.length > 0 ? (
      <MatchesSection matchType={MatchType.UpcommingMatch} matches={matchesStore.upcommingMatches} />
    ) : (
      <div className="alert alert-info" role="alert">
        No upcomming match.
      </div>
    );

    const recentMatchesSection = matchesStore.recentMatches.length > 0 ? (
      <MatchesSection matchType={MatchType.RecentMatch} matches={matchesStore.recentMatches} />
    ) : (
      <div className="alert alert-info" role="alert">
        No recent match.
      </div>
    );

    return (
      <div>
        <h2>Today matches</h2>
        {todayMatchesSection}
        <h2>Upcomming matches</h2>
        {upcommingMatchesSection}
        <h2>Recent matches</h2>
        {recentMatchesSection}
      </div>
    );
  }
}

const api = new ProjectVioletApi();
const store = new MatchesStore(api);

const element = <IndexPage matchesStore={store} />;
ReactDOM.render(
  element,
  document.getElementById('react')
);