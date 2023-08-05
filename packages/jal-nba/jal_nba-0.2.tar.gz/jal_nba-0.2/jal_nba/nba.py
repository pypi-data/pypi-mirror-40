import datetime
import json
import logging
import requests

from collections import namedtuple
from datetime import timedelta
from pytz import timezone
from requests.packages.urllib3.exceptions import InsecureRequestWarning
from .exceptions import NBAException

requests.packages.urllib3.disable_warnings(InsecureRequestWarning)


def _config():
    """
    Get configuration for command
    :return:
    """
    with open('config.json'.format(config_file), 'r') as f:
        config = json.load(f)
    if 'env' not in config.keys():
        config['env'] = None
    if config['env']:
        for env_var in config['env']:
            config[env_var] = os.environ[env_var]
        del config['env']
    return config

BASE_URL = 'https://stats.nba.com/stats/'


CONFIG = _config()
COUNT = 0


def fetch_data(session, url, params):
    """
    Fetch data from stats.nba.com API
    """
    global COUNT
    COUNT += 1
    logging.info(COUNT)
    user_agent = [
        'Mozilla/5.0 (Windows NT 6.2; WOW64)',
        'AppleWebKit/537.36 (KHTML, like Gecko)',
        'Chrome/57.0.2987.133 Safari/537.36'
    ]

    headers = {
        'user-agent': (" ".join(user_agent)),
        'Dnt': ('1'),
        'Accept-Encoding': ('gzip, deflate, sdch'),
        'Accept-Language': ('en'),
        'origin': ('http://stats.nba.com'),
        'Cache-Control': ('max-age=0'),
        'Connection': ('keep-alive'),
        'Host': ('stats.nba.com')
    }

    try:
        request = session.get(url, headers=headers, params=params, verify=False, timeout=10)
        if request.status_code == 200:
            data = request.json()
            request.connection.close()
            return data['resultSets']
    except requests.exceptions.Timeout as err:
        logging.error(f"NBA API Timeout\n{url}\n{params}")
        err_message = [
            'Unable to connect to stats.nba.com API.',
            'Connection timed out'
        ]
        try:
            # session = requests.session()
            request = session.get(url, headers=headers, params=params, verify=False)
        except requests.exceptions.Timeout:
            raise NBAException("\n".join(err_message))
    except requests.exceptions.ConnectionError:
        session = requests.session()
        request = session.get(url, headers=headers, params=params, verify=False)
    if request.status_code == 200:
        data = request.json()
        # logging.info(json.dumps(data, indent=2))
        # for i in data['resultSets']:
        #    logging.info(i['name'])
        return data['resultSets']
    else:
        print(request.status_code)


class NBA:
    """
    Create NBA team object
    """
    teams = get_config('nba_teams.json')

    def __init__(self):
        self._session = requests.session()
        self._date = datetime.datetime.now(timezone('US/Eastern'))


class NBALeague(NBA):
    """
    NBA League
    """
    def __init__(self):
        super().__init__()
        self._team_ids = CONFIG['ids']
        self.games_data = self._get_games_data()
        self.eastern_conference = self._conference_record_data('east')
        self.western_conference = self._conference_record_data('west')
        self.team_records = self.nba_records()
        self.overall_standings = self.team_win_percentages()
        self.eastern_conference_standings = self.east_win_percentages()
        self.western_conference_standings = self.west_win_percentages()

    def recent_games(self):
        date = (self._date - timedelta(1)).strftime("%m/%d/%Y")
        return self._get_games_data(date)

    def recent_scores(self):
        games = []
        if self.todays_games.live or self.todays_games.final:
            return self.todays_games.live + self.todays_games.final
        games_data = self.recent_games()
        game_headers = games_data[0]['headers']
        game_sets = games_data[0]['rowSet']
        for game in game_sets:
            header_list = ['HOME_TEAM_ID', 'VISITOR_TEAM_ID', 'GAME_ID']
            game_info = list(zip(game_headers, game))
            game_data = {x.lower(): self._get_data(game_info, x) for x in header_list}
            game_data['home_team'] = self._team_ids.get(game_data['home_team_id'])
            game_data['away_team'] = self._team_ids.get(game_data['visitor_team_id'])
            score_headers = games_data[1]['headers']
            score_sets = games_data[1]['rowSet']
            game_scores = []
            for score in score_sets:
                game_scores.append(list(zip(score_headers, score)))
            for score in game_scores:
                game_id = self._get_data(score, 'GAME_ID')
                team_id = self._get_data(score, 'TEAM_ID')
                points = self._get_data(score, 'PTS')
                if game_id == game_data['game_id']:
                    if team_id == game_data['home_team_id']:
                        game_data['home_team_score'] = points
                    elif team_id == game_data['visitor_team_id']:
                        game_data['away_team_score'] = points
            games.append(game_data)
        return games

    def nba_records(self):
        """
        Return a dict containing individual record of each NBA team. Each team
        in dict is identified with a string of their NBA API id
        """
        nba_data = {}
        for i in self.eastern_conference.keys():
            wins = self.eastern_conference[i]['W']
            losses = self.eastern_conference[i]['L']
            record = f"{wins}-{losses}"
            # name = self._team_ids.get(i)
            # nba_data[name] = record
            nba_data[i] = record
        for i in self.western_conference.keys():
            wins = self.western_conference[i]['W']
            losses = self.western_conference[i]['L']
            record = f"{wins}-{losses}"
            nba_data[i] = record
        return nba_data

    def team_win_percentages(self):
        """
        Return a dict containing the win percentage of each individual NBA team
        this can be used to display standings for the entire league
        """
        win_percentages = {}
        for k, v in self.eastern_conference.items():
            win_percentages[k] = v['W_PCT']
        for k, v in self.western_conference.items():
            win_percentages[k] = v['W_PCT']
        return win_percentages

    def east_win_percentages(self):
        """
        Return a dict containing the win percentage for each team in the NBA
        Eastern Conference. This can be used to display the current standings
        for the conference
        """
        win_percentages = {}
        for k, v in self.eastern_conference.items():
            win_percentages[k] = v['W_PCT']
        return win_percentages

    def west_win_percentages(self):
        """
        Return a dict containing the win percentage for each team in the NBA
        Western Conference. This can be used to display the current standings
        for the conference
        """
        win_percentages = {}
        for k, v in self.western_conference.items():
            win_percentages[k] = v['W_PCT']
        return win_percentages

    @staticmethod
    def _get_team_id(team):
        """
        Provided a team name this function will return its NBA API team ID
        number as a string
        """
        team_ids = CONFIG['names_to_id']
        team_id = team_ids.get(team)
        if not team_id:
            raise NBAException(f"Team {team} not found")
        return team_id

    @property
    def todays_games(self):
        """
        Fetch data from stats.nba.com and create list containing an object
        for each game being played today
        """
        unplayed_games = []
        live_games = []
        finished_games = []
        games_data = self.games_data
        game_headers = games_data[0]['headers']
        game_sets = games_data[0]['rowSet']
        header_list = [
            'GAME_STATUS_ID', 'HOME_TEAM_ID', 'VISITOR_TEAM_ID', 'GAME_ID', 'GAME_DATE_EST', 'GAME_STATUS_TEXT'
        ]
        for game in game_sets:
            # game_info = list(zip(game_headers, game))
            game_info = dict(zip(game_headers, game))
            game_data = {x.lower(): game_info.get(x) for x in header_list}
            # game_data = {x.lower(): self._get_data(game_info, x) for x in header_list}
            logging.info(json.dumps(game_data, indent=2))
            game_data['home_record'] = self.get_team_record(game_data['home_team_id'])
            game_data['away_record'] = self.get_team_record(game_data['visitor_team_id'])
            game_data['home_team'] = self._team_ids.get(game_data['home_team_id'])
            game_data['away_team'] = self._team_ids.get(game_data['visitor_team_id'])
            status = game_data['game_status_id']
            if status == '1':
                unplayed_games.append(game_data)
            elif status == '2' or status == '3':
                score_headers = games_data[1]['headers']
                score_sets = games_data[1]['rowSet']
                game_scores = []
                for score in score_sets:
                    game_scores.append(list(zip(score_headers, score)))
                for score in game_scores:
                    game_id = self._get_data(score, 'GAME_ID')
                    team_id = self._get_data(score, 'TEAM_ID')
                    points = self._get_data(score, 'PTS')
                    if game_id == game_data['game_id']:
                        if team_id == game_data['home_team_id']:
                            game_data['home_team_score'] = points
                        elif team_id == game_data['visitor_team_id']:
                            game_data['away_team_score'] = points
                if status == '2':
                    live_games.append(game_data)
                elif status == '3':
                    finished_games.append(game_data)
        Games = namedtuple('Status', ['unplayed', 'live', 'final'])
        games_info = Games(unplayed=unplayed_games, live=live_games, final=finished_games)
        # CACHE.set(game_data['id'], game_data)
        return games_info

    def get_team_record(self, team_id):
        """
        Get an NBA teams record with a team name or ID
        """
        team = str(team_id)
        if team not in self._team_ids.keys():
            team = self._get_team_id(team)
        record = self.team_records.get(team)
        return record

    def _get_games_data(self, date=None):
        """
        Fetch data from stats.nba.com for the days games
        The API returns all games for the calendar day along with their state
        (1 for unplayed, 2 for ongoing live, 3 for completed).
        """
        url = f"{BASE_URL}scoreboard/"
        # if no date is provided get data for the current days games
        if not date:
            date = datetime.datetime.strftime(self._date, "%m/%d/%Y")
        params = {
            'GameDate': date,
            'LeagueID': '00',
            'DayOffset': '0'
        }
        data = fetch_data(self._session, url, params)
        return data

    def _get_data(self, game_info, data_title):
        """
        Get the data value from the zipped list of row headers (data titles)
        and data points
        """
        for game in game_info:
            header, data = game
            if header == data_title:
                data = str(data)
                return data

    def _conference_record_data(self, conference):
        """
        Return a dict containing team info for each team in a provideded NBA
        conference. Data is gathered from the NBA API and then parsed using the
        from the API. Reurned data keys are each team's NBA API ID number and
        values consist of key, values for a teams games played (G), wins (W),
        losses (L), winning percentage (W_PCT), conference (CONFERENCE), home
        record (HOME_RECORD), road record (ROAD_RECORD), and team name (TEAM)
        Example of the Boston Celtic's item in the returned dict:
        "1610612738": {
          "TEAM_ID": "1610612738",
          "TEAM": "Boston",
          "G": "26",
          "W": "16",
          "L": "10",
          "W_PCT": "0.615",
          "CONFERENCE": "East",
          "HOME_RECORD": "8-3",
          "ROAD_RECORD": "8-7"
        }
        """
        if conference == 'east':
            conference = 'EastConfStandingsByDay'
        else:
            conference = 'WestConfStandingsByDay'
        conference_data = {}
        header_list = [
            'TEAM_ID', 'TEAM', 'G', 'W', 'L', 'W_PCT', 'CONFERENCE', 'HOME_RECORD', 'ROAD_RECORD'
        ]
        for i in self.games_data:
            if i['name'] == conference:
                headers = i['headers']
                game_sets = i['rowSet']
                for game in game_sets:
                    game_data = list(zip(headers, game))
                    team_data = {x: self._get_data(game_data, x) for x in header_list}
                    conference_data[team_data['TEAM_ID']] = team_data
        return conference_data

    def league_leaders(self):
        endpoint = 'leagueleaders'
        params = {
            'LeagueID': '00',
            'StatCategory': 'Scoring',
            'Season': '2018-19',
            'PerMode': 'PerGame',
            'Scope': 'RS',
            'SeasonType': 'Regular Season',
        }
        return endpoint, params


class NBATeam(NBALeague):
    def __init__(self, team):
        super().__init__()
        self.team = team
        self.record = self.get_team_record(self.team)
        self.win_percentage = self._get_win_percentage(self.team)
        self.wins = self._get_games_outcome_total(self.team, 'wins')
        self.losses = self._get_games_outcome_total(self.team, 'losses')
        self.games_played = self._get_games_played(self.team)
        self.roster = self._get_roster(self.team)
        self.offensive_stats = self._get_offense_stats(self.team)
        self.defensive_stats = self._get_defense_stats(self.team)
        self.city = self._get_city(self.team)
        self.mascot = self._get_mascot(self.team)
        self.name = f"{self.city} {self.mascot}"

    def __repr__(self):
        return f"{self.team} - record: {self.record}"

    def _get_win_percentage(self, team):
        """
        Get a team's current winning percentage
        """
        team_id = self._get_team_id(team)
        winning_percentage = self.overall_standings.get(team_id)
        return winning_percentage

    def _get_games_outcome_total(self, team, outcome):
        """
        Get the current number of wins or losses for a team
        """
        wins, losses = self.get_team_record(team).split('-')
        outcomes = {
            'wins': wins,
            'losses': losses
        }
        outcome_total = outcomes.get(outcome)
        return outcome_total

    def _get_games_played(self, team):
        """
        Get the number of games played by a team in current season
        """
        record = self.get_team_record(team).split('-')
        games = int(record[0]) + int(record[1])
        return games

    def _get_offense_stats(self, team):
        """
        Get a team's current offensive stats for the current season
        """
        pass

    def _get_defense_stats(self, team):
        """
        Get a team's current defensive stats for the current season
        """
        pass

    def _get_roster(self, team, season=None):
        """
        Get the current roster for a team
        """
        if not season:
            season = '2018-19'
        team_id = self._get_team_id(team)
        url = 'https://stats.nba.com/stats/commonteamroster/'
        params = {'Season': season, 'TeamID': team_id}
        roster_data = fetch_data(self._session, url, params)
        headers = roster_data[0]['headers']
        player_sets = roster_data[0]['rowSet']
        roster = []
        for player in player_sets:
            player_data = dict(zip(headers, player))
            roster.append(player_data)
        return roster

    def _get_game_logs(self, team, season=None, season_type='Regular Season'):
        """
        Get the game logs for a team
        """
        if not season:
            season = '2018-19'
        team_id = self._get_team_id(team)
        url = 'https://stats.nba.com/stats/teamgamelogs/'
        params = {'TeamID': team_id, 'Season': season, 'SeasonType': season_type}
        games_data = fetch_data(self.session, url, params)
        headers = games_data[0]['headers']
        game_sets = games_data[0]['rowSet']
        game_logs = []
        for game in game_sets:
            game_data = dict(zip(headers, game))
            game_logs.append(game_data)
        return game_logs

    def _get_city(self, team):
        pass

    def _get_mascot(self, team):
        pass


class NBAPlayer(NBA):
    def __init__(self, player):
        super().__init__()
        self.player = player
        pass


def main():
    nba = NBALeague()
    games = nba.todays_games
    print(json.dumps(games, indent=2))
    # print(json.dumps(games['resultSets'][0], indent=2))


if __name__ == '__main__':
    main()
