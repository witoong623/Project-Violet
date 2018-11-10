import * as React from 'react';
import { observable, action } from 'mobx';
import { observer } from 'mobx-react';
import axios, { AxiosResponse } from 'axios';
import { Match } from '../models';

@observer
export class MatchEntry extends React.Component<{match: Match, isAuthenticate: boolean}> {
    @action.bound
    handleInputChange(event: any) {
      this.props.match.isWatch = event.target.checked;
  
      if (this.props.match.isWatch) {
        axios.post('/userwatchhistory/', { match: this.props.match.matchId })
          .then(action((res: AxiosResponse<any>) => {
            this.props.match.watchId = res.data.id;
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

      const watchBadge = match.isWatch ? (
        <div className="match-card-badge">
          <span className="badge badge-success">Watched</span>
        </div>
      ) : (
        <div className="match-card-badge" style={{visibility: "hidden"}}>
          <span className="badge badge-success">Watched</span>
        </div>
      );

      const matchLogo = match.homeScore !== null ? (
        <div className="match-card-logo">
          <div className="match-card-logo-box">
            <img src={match.homeLogo} height="90" />
            <div className="match-score">{match.homeScore.toString()}</div>
          </div>
          <h6>VS</h6>
          <div className="match-card-logo-box">
            <img src={match.awayLogo} height="90" />
            <div className="match-score">{match.awayScore.toString()}</div>
          </div>
        </div>
      ) : (
        <div className="match-card-logo">
          <img src={match.homeLogo} height="90" />
          <h6>VS</h6>
          <img src={match.awayLogo} height="90" />
        </div>
      );
  
      return (
        <div className="col-3">
          <div className="match-card">
            {watchBadge}
            {matchLogo}
            <div className="match-card-body">
              <h5>{match.home}</h5>
              <p>VS</p>
              <h5>{match.away}</h5>
              <h6>{match.date}</h6>
            </div>
            {isAuthenticate &&
              <div className="match-card-control">
                <div className="form-check">
                  <input id={match.matchId.toString()} className="form-check-input" type="checkbox" checked={match.isWatch} onChange={this.handleInputChange} />
                  <label className="form-check-label" htmlFor={match.matchId.toString()}>
                    Watch this match
                </label>
                </div>
              </div>
            }
          </div>
        </div>
      )
    }
  }