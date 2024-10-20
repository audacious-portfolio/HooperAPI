from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles
import requests


app = FastAPI()

app.mount("/logos", StaticFiles(directory="static"), name="static")


@app.get("/")
async def root():
    return {"message": "Hello World"}


class Team:
    def __init__(self, team_id, team_name, team_city, team_tricode, team_slug, wins, losses, score, seed):
        self.teamId = team_id
        self.teamName = team_name
        self.teamCity = team_city
        self.teamTricode = team_tricode
        self.teamSlug = team_slug
        self.wins = wins
        self.losses = losses
        self.score = score
        self.seed = seed
        self.lightLogo = f"https://hooperapi.onrender.com/logos/light/{team_id}"
        self.darkLogo = f"https://hooperapi.onrender.com/logos/dark/{team_id}"


class Player:
    def __init__(self, player_id, first_name, last_name, team_id, team_name, team_city, team_tricode, team_slug, points):
        self.playerId = player_id
        self.firstName = first_name
        self.lastName = last_name
        self.teamId = team_id
        self.teamName = team_name
        self.teamCity = team_city
        self.teamTricode = team_tricode
        self.teamSlug = team_slug
        self.points = points
        self.headshot = f"https://cdn.nba.com/headshots/nba/latest/1040x760/{player_id}.png"


class Game:
  def __init__(self, game_id, game_status, game_date_time, home_team, away_team, points_leader):
    self.gameId = game_id
    self.gameStatus = game_status
    self.gameDateTime = game_date_time
    self.gameStatus = game_status
    self.homeTeam = home_team
    self.awayTeam = away_team
    self.pointsLeader = points_leader


@app.get("/games/{date}")
async def get_games_by_date(date: str):
    formatted_date = f"{date[:2]}/{date[2:4]}/{date[4:]} 00:00:00"

    url = "https://cdn.nba.com/static/json/staticData/scheduleLeagueV2_1.json"
    response = requests.get(url).json()

    raw_schedule = response["leagueSchedule"]["gameDates"]
    raw_games = []
    for day in raw_schedule:
        if day["gameDate"] == formatted_date:
            raw_games = day["games"]

    games = []
    for game in raw_games:
        home_team = Team(game["homeTeam"]["teamId"], game["homeTeam"]["teamName"], game["homeTeam"]["teamCity"], game["homeTeam"]["teamTricode"], game["homeTeam"]["teamSlug"], game["homeTeam"]["wins"], game["homeTeam"]["losses"], game["homeTeam"]["score"], game["homeTeam"]["seed"])
        away_team = Team(game["awayTeam"]["teamId"], game["awayTeam"]["teamName"], game["awayTeam"]["teamCity"], game["awayTeam"]["teamTricode"], game["awayTeam"]["teamSlug"], game["awayTeam"]["wins"], game["awayTeam"]["losses"], game["awayTeam"]["score"], game["awayTeam"]["seed"])
        points_leader = Player(game["pointsLeaders"][0]["personId"], game["pointsLeaders"][0]["firstName"], game["pointsLeaders"][0]["lastName"], game["pointsLeaders"][0]["teamId"], game["pointsLeaders"][0]["teamName"], game["pointsLeaders"][0]["teamCity"], game["pointsLeaders"][0]["teamTricode"], game["pointsLeaders"][0]["teamSlug"], game["pointsLeaders"][0]["points"],)
        games.append(Game(game["gameId"], game["gameStatusText"], game["gameDateTimeEst"], home_team , away_team, points_leader))

    return {"data": games}
