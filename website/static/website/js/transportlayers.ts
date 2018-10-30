import axios from 'axios';

export class IndexPageApi {
  private isRecenMatchesFirstFetch: boolean = true;
  private recentMatchesNextUrl: string;

  fetchUpcommingMatches(): Promise<any[]> {
    return axios.get('/upcomming-matches/')
      .then(res => res.data)
      .catch(err => {
        console.log(err);
        return new Array<any>();
      });
  }

  async fetchRecentMatches(): Promise<any[]> {
    let fetchLink: string = null;

    if (this.isRecenMatchesFirstFetch) {
      this.isRecenMatchesFirstFetch = false;
      fetchLink = '/recent-matches/'
    } else if (this.recentMatchesNextUrl !== null) {
      fetchLink = this.recentMatchesNextUrl
    } else {
      // No next page
      return new Array();
    }


    return axios.get(fetchLink)
      .then(res => {
        this.recentMatchesNextUrl = res.data.next;
        return res.data.results;
      })
      .catch(err => {
        console.log(err);
        return new Array();
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

  fetchRecommendedMatches(): Promise<any[]> {
    return axios.get('/recommended-matches/')
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
      })
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

export class CompetitionPageApi {
  private nextPortionLink: string = null;
  private isFirstFetch: boolean = true;

  constructor(public competitionId: string) {

  }

  async fetchMatchList(): Promise<any[]> {
    let fetchLink: string = null;

    if (this.isFirstFetch) {
      this.isFirstFetch = false;
      fetchLink = `/api/competition/${this.competitionId}/`;
    } else if (this.nextPortionLink !== null) {
      fetchLink = this.nextPortionLink;
    } else {
      // no more match
      return new Array();
    }

    return axios.get(fetchLink)
      .then(res => {
        this.nextPortionLink = res.data.next;
        return res.data.results;
      })
      .catch(err => {
        console.log(err);
        return new Array();
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
