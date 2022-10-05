from typing import List
from bs4 import BeautifulSoup
import requests
import re
import pandas as pd


# gives list of all team squad links when given a league
def parseleague(league):
    teams = []
    leaguetext = requests.get(league).text
    leaguesoup = BeautifulSoup(leaguetext, 'html.parser')
    for i in leaguesoup.find_all("a",string=re.compile("Squad")):
        teams.append(i['href'])
    return teams

#gives list of player link, player teams when given a team
def parseteam(team):
    players = []
    teamtext = requests.get("https://www.worldfootball.net" + team).text
    teamsoup = BeautifulSoup(teamtext, 'html.parser')
    teamstring = teamsoup.find("div", class_ = "head").get_text().lstrip().rstrip()
    for i in teamsoup.find_all("a"):
        if "player_summary" in str(i):
            players.append((i['href'],teamstring))
    return players

# gives dictionary of player info when given a player link
def parseplayer(player, team):
    info = {"Name" : None, "Team": team, "Birthdate" : None, "Nation": None, "Height": None, "Weight": None, "Foot" : None, "Position" : None}
    playertext = requests.get("https://www.worldfootball.net" + player).text
    playersoup = BeautifulSoup(playertext, 'html.parser')
    try:
        info["Name"] = playersoup.find("h2", itemprop = "name").get_text().lstrip().rstrip()
    except:
        return None
    try:
        info["Birthdate"] = playersoup.find("b", string="Born:").parent.next_sibling.next_sibling.get_text().lstrip().rstrip()
    except:
        info["Birthdate"] = None
    try:
        info["Nation"] = playersoup.find("span", itemprop = "nationality").get_text().lstrip().rstrip()
    except:
        info["Nation"] = None
    try:
        info["Height"] = playersoup.find("b", string="Height:").parent.next_sibling.next_sibling.get_text().lstrip().rstrip()
    except:
        info["Height"] = None
    try:
        info["Foot"] = playersoup.find("b", string="Foot:").parent.next_sibling.next_sibling.get_text().lstrip().rstrip()
    except:
        info["Foot"] = None
    try:
        info["Weight"] = playersoup.find("b", string="Weight:").parent.next_sibling.next_sibling.get_text().lstrip().rstrip()
    except:
        info["Weight"] = None
    try:
        info["Position"] = playersoup.find("b", string="Position(s):").parent.next_sibling.next_sibling.get_text().lstrip().rstrip()
    except:
        info["Position"] = None
    return info

def playerDataFromLeagues(leagues: List[str]):
    players = []
    for league in leagues:
        for team in parseleague(league):
            for player in parseteam(team):
                players.append(parseplayer(player))
    return players

def playerDataFromTeam(team: List[str]):
    players = []
    for player in team:
        players.append(parseplayer(player[0], player[1]))
    return players


if __name__ == "__main__":
    prem = "https://www.worldfootball.net/players/eng-premier-league-2022-2023/"
    bundes = "https://www.worldfootball.net/players/bundesliga-2022-2023/"
    la_liga = "https://www.worldfootball.net/players/esp-primera-division-2022-2023/"
    ligue_1 = "https://www.worldfootball.net/players/fra-ligue-1-2022-2023/"
    serie_a = "https://www.worldfootball.net/players/ita-serie-a-2022-2023/"
    leagues = [prem,bundes,la_liga,ligue_1,serie_a]

    # just doing one example with la liga
    teams = parseleague(la_liga)
    players = parseteam(teams[0])
    pl = playerDataFromTeam(players)
    pl.extend(playerDataFromTeam(parseteam(teams[1])))
    playerdata = pd.DataFrame.from_records(pl)
    playerdata.drop_duplicates(inplace=True)
    playerdata.to_csv('players.csv')

    


