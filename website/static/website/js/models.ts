import { observable } from 'mobx';

const dateFormatOption = {
  day: 'numeric',
  month: 'long',
  year: 'numeric',
  hour: 'numeric',
  minute: 'numeric'
}

export class Match {
    public home: string;
    public away: string;
    public date: string;
    public homeLogo: string;
    public awayLogo: string;
    public homeScore?: number = null;
    public awayScore?: number = null;

    @observable public isWatch: boolean = false;
    public watchId: number = 0;

    constructor(public matchId: number) {
    }

    updateFromJson(matchJson: any) {
      this.home = matchJson.home_team;
      this.away = matchJson.away_team;
      this.date = new Date(matchJson.date).toLocaleDateString('th-TH', dateFormatOption);
      this.homeLogo = matchJson.home_logo;
      this.awayLogo = matchJson.away_logo;
      this.homeScore = matchJson.home_score;
      this.awayScore = matchJson.away_score;
    }

    updateIsWatch(isWatch: boolean) {
      
    }
}
