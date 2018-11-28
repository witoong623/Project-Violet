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

    private _jsDate: Date;
    get jsDate(): Date {
      return this._jsDate;
    }

    constructor(public matchId: number) {
    }

    updateFromJson(matchJson: any) {
      this._jsDate = new Date(matchJson.date);

      this.home = matchJson.home_team;
      this.away = matchJson.away_team;
      this.date = this.jsDate.toLocaleDateString('th-TH', dateFormatOption);
      this.homeLogo = matchJson.home_logo;
      this.awayLogo = matchJson.away_logo;
      this.homeScore = matchJson.home_score;
      this.awayScore = matchJson.away_score;
    }

    updateIsWatch(isWatch: boolean) {
      
    }
}
