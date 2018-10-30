import * as React from 'react'
import * as ReactDOM from 'react-dom'
import { observable, action, configure } from 'mobx';
import { observer } from "mobx-react";
import axios from 'axios';
import { Match } from './models';
import { MatchEntry } from './components/match-entry';
import { IndexPageApi } from './transportlayers';

enum MatchType {
  TodayMatch = 'todayMatch',
  UpcommingMatch = 'upcommingMatch',
  RecentMatch = 'recentMatch',
  Recommended = 'recommended'
}

const matchTypeBaseKeys: {[key:string]: number} = {
  todayMatch: 1,
  upcommingMatch: 100,
  recentMatch: 1000,
  recommended: 10000
}

axios.defaults.xsrfHeaderName = 'X-CSRFToken';
axios.defaults.xsrfCookieName = 'csrftoken';

configure({
  enforceActions: 'observed'
});

class MatchesStore {
  @observable todayMatches: Array<Match> = new Array<Match>();
  @observable upcommingMatches: Array<Match> = new Array<Match>();
  @observable recentMatches: Array<Match> = new Array<Match>();
  @observable recommendedMatches: Array<Match> = new Array<Match>();

  // findingMatches is use to store every match regardless of their type
  // so that we can find duplicate match
  private findingMatches: Array<Match> = new Array<Match>();

  constructor(public indexPageApi: IndexPageApi) {
    this.fetchMatchLists()
      .then(() => this.fetchUserWatchHistory())
      .then(() => this.fetchRecommendedMatches());
  }

  private async fetchMatchLists() {
    let upcommingMatches = await this.indexPageApi.fetchUpcommingMatches();
    upcommingMatches.forEach((matchJson: any) => this.updateMatchFromServer(matchJson, this.upcommingMatches));

    let todayMatches = await this.indexPageApi.fetchTodayMatches();
    todayMatches.forEach(matchJosn => this.updateMatchFromServer(matchJosn, this.todayMatches));

    let recentMatches = await this.indexPageApi.fetchRecentMatches();
    recentMatches.forEach(matchJson => this.updateMatchFromServer(matchJson, this.recentMatches));
  }

  // This method is used to call from outside store to fetch next recent matches
  async fetchNextRecentMatches() {
    let recentMatches = await this.indexPageApi.fetchRecentMatches();
    recentMatches.forEach(matchJson => this.updateMatchFromServer(matchJson, this.recentMatches));
  }

  private fetchUserWatchHistory() {
    this.indexPageApi.fetchUserWatchHistory()
      .then(data => {
        data.forEach((userWatch: any) => this.updateMatchIsWatchFromServer(userWatch));
      });
  }

  private fetchRecommendedMatches() {
    this.indexPageApi.fetchRecommendedMatches()
      .then(data => {
        data.forEach(matchJson => this.updateMatchFromServer(matchJson, this.recommendedMatches))
      })
      .catch(err => console.log(err));
  }

  @action.bound
  updateMatchFromServer(matchJson: any, storeArray: Array<Match>) {
    let existMatch = this.findingMatches.find(match => match.matchId === matchJson.id)
    if (existMatch) {
      storeArray.push(existMatch);
      return;
    }

    let match = new Match(matchJson.id);
    match.updateFromJson(matchJson);
    storeArray.push(match);
    this.findingMatches.push(match);
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

    match = this.recommendedMatches.find(match => match.matchId === userWatch.match);
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

    const recommendedMatchesSection = matchesStore.recommendedMatches.length > 0 ? (
      <MatchesSection matchType={MatchType.Recommended} matches={matchesStore.recommendedMatches} />
    ) : (
      <div className="alert alert-info" role="alert">
        No recommended match.
      </div>
    );

    return (
      <div>
        <h2>Recommended matches</h2>
        {recommendedMatchesSection}
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

const api = new IndexPageApi();
const store = new MatchesStore(api);

const element = <IndexPage matchesStore={store} />;
ReactDOM.render(
  element,
  document.getElementById('react')
);

window.onscroll = () => {
  if (
    window.innerHeight + document.documentElement.scrollTop
    === document.documentElement.offsetHeight
  ) {
    store.fetchNextRecentMatches();
  }
}
