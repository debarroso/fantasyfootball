# @Author: Oliver DeBarros <debar>
# @Date:   2017-08-12T11:07:58-05:00
# @Email:  debarros.oliver@gmail.com
# @Filename: getPFR.py
# @Last modified by:   debar
# @Last modified time: 2018-04-15T12:21:20-05:00


#########################################################################################################
#
# This file is intended to scrape data from https://www.pro-football-reference.com to create a data
# set to which I will apply machine learning algorithms to win daily fantasy competitions
#
#########################################################################################################


#import libraries
from bs4 import BeautifulSoup, Comment
import requests
import re
import csv
import os

#store url in global for use throughout program
url = "https://www.pro-football-reference.com"
fantasy_pos = ["QB", "WR", "RB", "TE"]
team_dict = {"crd":["ARI"], "atl":["ATL"], "rav":["BAL"], "buf":["BUF"], "car":["CAR"],
             "chi":["CHI"], "cin":["CIN"], "cle":["CLE"], "dal":["DAL"], "den":["DEN"],
             "det":["DET"], "gnb":["GNB", "GB", "GBP"], "htx":["HOU"], "clt":["IND"],
             "jax":["JAX", "JAC"], "kan":["KAN", "KC"], "sdg":["SD", "LAC", "LACH"],
             "ram":["STL", "LAR", "LARM"], "mia":["MIA"], "min":["MIN"], "nwe":["NE", "NWE"],
             "nor":["NOR", "NO"], "nyg":["NYG"], "nyj":["NYJ"], "rai":["OAK"], "phi":["PHI"],
             "pit":["PIT"], "sfo":["SF"], "sea":["SEA"], "tam":["TAM", "TB"], "oti":["TEN"], "was":["WAS"]}

"""team_list = ["crd", "atl", "rav", "buf", "car", "chi", "cin", "cle", "dal", "den", "det", "gnb", "htx",
             "clt", "jax", "kan", "sdg", "ram", "mia", "min", "nwe", "nor", "nyg", "nyj", "rai", "phi",
             "pit", "sfo", "sea", "tam", "oti", "was"]
"""


#########################################################################################################
#                                      |\    /|    /\    |  |\  |
#                                      | \  / |   /__\   |  | \ |
#                                      |  \/  |  /    \  |  |  \|
#########################################################################################################
def main():
    #get team links outside of the loop since they do not change
    team_links = GetTeamLinks()

    for year in [2017]:
        print(year)
        #create team objects (team objs will store coaches, player objects, and links)
        teams = CreateTeamObjs(team_links, year)

        #get oline and dline team ranks
        LineRanks(teams, "ol", year)
        LineRanks(teams, "dl", year)
        print("LineRanks Done")

        #get overall team defense ranks
        TeamDefense(teams, year)
        print("Team Defense Done")

        #get overall passing and rushing offense ranks
        TeamOffense(teams, year)
        print("Team Offense Done")

        #pass in the team objects (since we want to get opponent team stats too) then iterate over
        #boxscores to get weekly stats
        WeeklyStats(teams, year)

        #fantasy points for every player on this team
        FantasyPoints(teams, year)

        #write all of the output to a file
        WriteToFile(teams, year)

    return


"""=====================================================================================================+
| This function will iterate over the 32 nfl teams and store links to each in a list                    |
+====================================================================================================="""
def GetTeamLinks():
    #request teams from pro-football-reference and get soup
    team_request = requests.get("{}/teams/".format(url))
    team_soup = BeautifulSoup(team_request.text, "lxml")

    #declare list to store links
    teams = []

    #iterate over soup to grab only relevant links and append to teams list
    for team in team_soup.find_all(href=re.compile("teams")):
        team_string = str(team)
        if "htm" in team_string or ">Teams<" in team_string:
            continue
        teams.append(team.get("href"))

    return teams


"""=====================================================================================================+
| This function will create a list of team objects                                                      |
+====================================================================================================="""
def CreateTeamObjs(teams, year):

  #declare list that we will be storing objects in
    team_obj = {}

    #iterate over teams and create team objects
    for team in teams:
        print(team)
        #request page and store info
        roster_req = requests.get("{}{}{}_roster.htm".format(url, team, year))
        soup = BeautifulSoup(roster_req.text, "lxml")

        #get team name from title segment
        name = str(soup.title).split(",")
        name = name[0].replace("<title>{} ".format(year), "").replace(" Starters", "")

        #get team abv fromlink
        abv = team.replace("teams", "").replace("/", "")

        #create player and coach dictionaries
        players = GetPlayers(soup, abv)
        coach_links = GetCoachLinks(soup)

        #create team objects
        team_obj[abv] = TeamObj(name, coach_links, players, team)

        #add list of boxscores to the team object
        (team_obj[abv].boxscores, team_obj[abv].after_bye, team_obj[abv].opp_score,
         team_obj[abv].opp_pass_yds, team_obj[abv].opp_rush_yds) = BoxScores(team, year)

        #we're gonna get the defensive alignment now
        team_info = BeautifulSoup(str(soup.find_all("div", {"id":"meta"})), "lxml")
        for p in team_info.find_all("p"):
            if "Defensive Alignment" in p.get_text():
                temp_align = p.get_text("^", strip=True).split("^")
                team_obj[abv].def_alignment = temp_align[1]

    return team_obj


"""=====================================================================================================+
| This function takes team webpage request text as an argument and returns the player links in a list   |
+====================================================================================================="""
def GetPlayers(player_soup, team):
    #declare list of player objects
    players = {}

    #since these are all stored in comments in the html get new soup object passing in comments
    comments = player_soup.find_all(text=lambda text: isinstance(text, Comment))
    comment_soup = BeautifulSoup(str(comments), "lxml")

    #loop over rows where we have a link that contains players in the string
    for comment in comment_soup.find_all(href=re.compile("players")):

        #to make getting the name and position easier join the text in a carrot delimited
        #string and then split based on that string
        row = comment.parent.parent.get_text("^", strip=True).split("^")

        #if the first element is numeric (jersey number) remove it
        if row[0].isnumeric():
            row.pop(0)

        #adding this for historical years if they went to pro bowl need to pop twice
        if "*" in row[1] or "+" in row[1]:
            row.pop(1)

        #if second element is now numeric (age) remove it
        if row[1].isnumeric():
            row.pop(1)

        #get rid of backslashes that were in the html file
        name = row[0].replace("\\", "")

        #name and position are now indexed at 0 and 1 so set them respectively
        if row[1].isalpha():
            position = row[1]
        else:
            position = ""

        #find index with hyphen for height
        index = None
        for i in range(2, len(row)):
            if "-" in row[i]:
                index = i
                break

        #if index is not set they're missing height and unimportant, move onto the next
        if index is None:
            continue

        #set height and weight based on index
        try:
            height = HeightToInches(row[index])
        except:
            continue
        weight = int(row[index - 1])

        #if Rook is in the row this player is a rookie
        if "Rook" in row[3:]:
            rook = True
        else:
            rook = False

        #get player link and their ID
        link = comment.get("href")
        ID = link.split("/")[-1].replace(".htm", "")

        #create our player objects
        players[ID] = PlayerObj(name, position, team, link, weight, height, rook)

        #deprecated, i don't really care about the course of the season for daily fantasy
        #get this seasons total fantasy output and last seasons fantasy output if we want this later the code is stored in misc
        #if position.upper() in fantasy_pos:
        #    (players[ID].prev_season, players[ID].season_stats) = GetSeason(link, position, year, rook)

    return players


"""=====================================================================================================+
| This function takes team webpage request text as an argument and returns the coach links in a list    |
+====================================================================================================="""
def GetCoachLinks(soup):
    #declare dictionary of teams current coaches
    coaches = {}

    #generate temp string so it is easier for us to create coaches soup object
    temp = soup.find_all("p")
    coach_soup = BeautifulSoup(str(temp), "lxml")

    #find all links that contain coaches
    for link in coach_soup.find_all(href=re.compile("coaches")):
        #type of coach is in parent strong tag so let's back out to grab it then remove the colon
        coach_type = link.parent.strong.get_text(strip=True).replace(":", "")

        #create dictionary of coaches with links to them
        coaches[coach_type] = {"link": link.get("href"), "name": link.get_text()}

    return coaches


"""=====================================================================================================+
| This call returns the links for boxscores in a week indexed dict for the team in the passed in year   |
|====================================================================================================="""
def BoxScores(team_link, year):
    #get initial soup for schedule page
    sched_req = requests.get("{}{}{}_games.htm".format(url, team_link, year))
    sched_soup = BeautifulSoup(sched_req.text, "lxml")

    last = 0

    #declare boxscore dict and get new soup
    boxscores = {}
    boxsoup = BeautifulSoup(str(sched_soup.find_all("tbody")), "lxml")

    #dict of opponent scores
    opp_scores = {}
    pass_yards = {}
    rush_yards = {}

    #iterate over boxscore links in the table
    for link in boxsoup.find_all(href=re.compile("boxscore")):
        #store link row in carrot delimited string to be easier to work with
        temp = link.parent.parent.get_text("^", strip=True).split("^")

        #if first part of string (week number) is not numeric continue to next iteration
        if not temp[0].isnumeric():
            continue

        if int(temp[0]) != last+1:
            after_bye = int(temp[0])

        #set boxscores dict index equal to week and link the boxscore
        boxscores[int(temp[0])] = link.get("href")

        last = int(temp[0])

        #get opponent scores
        opp_pts = int(link.parent.parent.find("td", {"data-stat":"pts_def"}).get_text())
        opp_scores[int(temp[0])] = opp_pts

        #get opponent pass yards
        try:
            pass_yds = int(link.parent.parent.find("td", {"data-stat":"pass_yds_def"}).get_text())
            pass_yards[int(temp[0])] = pass_yds
        except Exception:
            pass_yards[int(temp[0])] = None

        #get opponent rush yards
        try:
            rush_yds = int(link.parent.parent.find("td", {"data-stat":"rush_yds_def"}).get_text())
            rush_yards[int(temp[0])] = rush_yds
        except Exception:
            rush_yards[int(temp[0])] = None

    return (boxscores, after_bye, opp_scores, pass_yards, rush_yards)


"""=====================================================================================================+
| This function will set the offensive line ranks for the teams for a given year                        |
+====================================================================================================="""
def LineRanks(teams, line, year):
    #get soup object from team line ranks at football outsiders
    request = requests.get("http://www.footballoutsiders.com/stats/{}{}".format(line, year))
    soup = BeautifulSoup(request.text, "lxml")

    #find table then iterate over rows
    table = soup.find("table")
    for row in BeautifulSoup(str(table), "lxml").find_all("tr"):
        #split row into carrot delimited string
        row = row.get_text("^", strip=True).split("^")

        #if the first segment is not a number it is not an active rank row
        if not row[0].isnumeric():
            continue

        #enter here for olines
        if line == "ol":
            for team in teams:
                if row[1] in team_dict[team]:
                    teams[team].oline_rush = int(row[0])

            for team in teams:
                if row[12] in team_dict[team]:
                    teams[team].oline_pass = int(row[13])

        #enter here for dline
        if line == "dl":
            for team in teams:
                if row[1] in team_dict[team]:
                    teams[team].dline_rush = int(row[0])

            for team in teams:
                if row[12] in team_dict[team]:
                    teams[team].dline_pass = int(row[13])

    return


"""=====================================================================================================+
| This function will set the overall team defense ranks                                                 |
+====================================================================================================="""
def TeamDefense(teams, year):
    #get the request from football outsiders
    request = requests.get("http://www.footballoutsiders.com/stats/teamdef{}".format(year))
    soup = BeautifulSoup(request.text, "lxml")

    #find the first table on this page
    table = soup.find("table")
    for row in BeautifulSoup(str(table), "lxml").find_all("tr"):

        #store each table row into a carrot delimited string
        row = row.get_text("^", strip=True).split("^")

        #if the first part of the string is not numeric this does not contain ranking info, continue
        if not row[0].isnumeric():
            continue

        #set the appropriate ranks
        for team in teams:
            if row[1] in team_dict[team]:
                teams[team].def_pass_rank = row[7]
                teams[team].def_rush_rank = row[9]

    return


"""=====================================================================================================+
| This will get the rush and pass ranks for every team this year                                        |
+====================================================================================================="""
def TeamOffense(teams, year):
    #get html request and soup
    request = requests.get("{}/years/{}".format(url, year))
    soup = BeautifulSoup(request.text, "lxml")

    #get comment soup
    comments = soup.find_all(text=lambda text:isinstance(text, Comment))
    csoup = BeautifulSoup(str(comments), "lxml")

    #list of tables we'll evaluate
    tables = ["passing", "rushing"]

    for table in tables:
        #get the table we're evaluating
        temp = csoup.find("table", {"id":"{}".format(table)})

        #for each row we're gonna set the ranks based on the table we're in
        for row in temp.tbody.find_all("tr"):
            link = row.find("a")
            team = link.get("href").replace("/teams/", "").replace("/{}.htm".format(year), "")
            if table == "passing":
                teams[team].off_pass_rank = int(row.th.get_text())
            else:
                teams[team].off_rush_rank = int(row.th.get_text())

    return


"""=====================================================================================================+
| Convert height string to inches                                                                       |
+====================================================================================================="""
def HeightToInches(height):
    height = height.split("-")
    return ((int(height[0]) * 12) + int(height[1]))


"""=====================================================================================================+
| This iterates over the weekly boxscores and update the appropriate stats for the teams and the players|
+====================================================================================================="""
def WeeklyStats(teams, year):
    for team in teams:
        #get team and boxscores object
        print(team)
        t = teams[team]
        boxscores = t.boxscores

        for week in boxscores:
            link = boxscores[week]
            print(link)

            #get the soup object
            request = requests.get("{}{}".format(url, link))
            soup = BeautifulSoup(request.text, "lxml")

            #get a comment soup object
            comments = soup.find_all(text=lambda text:isinstance(text, Comment))
            csoup = BeautifulSoup(str(comments), "lxml")

            #get the gameday and time
            gamemeta = soup.find("div", {"class":"scorebox_meta"}).get_text("^", strip=True)
            t.week_gametime[week] = GetGametime(gamemeta.split("^")[2])
            t.week_gameday[week] = gamemeta.split("^")[0].split()[0]

            #teams in game
            matchup_soup = soup.find("div", {"class":"scorebox"})
            matchup = matchup_soup.find_all(href=re.compile("teams"))

            for item in matchup:
                if team in item.get("href"):
                    continue
                else:
                    t.weekly_opp[week] = item.get("href").replace("/teams/", "").replace("/{}.htm".format(year), "")

            #set team stats and whether they are the home or away team
            if team in link:
                t.weekly_home[week] = True
            else:
                t.weekly_home[week] = False

            #get the game playing conditions
            PlayingConditions(csoup.find("table", {"id":"game_info"}), t, week)

            #get the player and defense stats for this week
            WeekFantasyDef(link, csoup, team, t.week_def_stats, t.weekly_home[week])

            #now get the player stats for this week
            WeekFantasyPlayers(link, csoup, t.players)

    return


"""=====================================================================================================+
| Gets the gametime formatted from the passed in string                                                 |
+====================================================================================================="""
def GetGametime(time):
    if "am" in time:
        gametime = time[2:].replace("am","")

    else:
        gametime = time[2:].replace("pm","")
        hour = gametime.split(":")[0]
        hour = int(hour) + 12
        gametime = str(hour) + ":" + gametime.split(":")[1]

    return gametime


"""=====================================================================================================+
| This sets the playing conditions for the team this week                                               |
+====================================================================================================="""
def PlayingConditions(text, team, week):
    #get soup object
    soup = BeautifulSoup(str(text), "lxml")

    #get playing condition dicts
    team.week_roof[week] = None
    team.week_surface[week] = None
    team.week_weather[week] = {"Temp":None, "Rel Humidity":None, "Wind":None, "Wind Chill":None}

    #iterate over rows in table
    for row in soup.find_all("th"):

        #try setting roof
        if "Roof" in row.get_text():
            try:
                team.week_roof[week] = row.parent.td.get_text()
            except Exception:
                continue

        #try setting playing surface
        if "Surface" in row.get_text():
            try:
                team.week_surface[week] = row.parent.td.get_text(strip=True)
            except Exception:
                continue

        #try setting weather dict
        if "Weather" in row.get_text():
            try:
                weather = row.parent.td.get_text().split()

                try:
                    humidity_index = weather.index("humidity") + 1
                    rel_humidity = int(weather[humidity_index].replace("%","").replace(",", ""))
                except Exception:
                    rel_humidity = None

                try:
                    wind_index = weather.index("mph") - 1
                    wind_speed = int(weather[wind_index])
                except Exception:
                    wind_speed = None

                try:
                    chill_index = weather.index("chill") + 1
                    wind_chill = int(weather[chill_index])
                except Exception:
                    wind_chill = None

                team.week_weather[week] = {"Temp":int(weather[0]), "Rel Humidity":rel_humidity,
                                           "Wind":wind_speed, "Wind Chill":wind_chill}

            except Exception:
                continue

    return


"""=====================================================================================================+
| This will get the player and defense stats from the current game                                      |
+====================================================================================================="""
def WeekFantasyDef(box_link, csoup, team, def_stats, home):
    #get weekly def stats object for this team and week
    def_stats[box_link] = WeeklyTeamDefense()
    ds = def_stats[box_link]

    #get defense table
    def_table = csoup.find("table", {"id":"player_defense"})

    #iterate over rows in table to set defense stats
    for row in def_table.find_all("tr"):
        try:
            row.find("td", {"data-stat":"team"}).get_text() in team_dict[team]
        except Exception:
            continue

        ds.sacks += float(row.find("td", {"data-stat":"sacks"}).get_text())
        ds.forced_fumbles += int(row.find("td", {"data-stat":"fumbles_forced"}).get_text())
        ds.interceptions += int(row.find("td", {"data-stat":"def_int"}).get_text())
        ds.tds += int(row.find("td", {"data-stat":"def_int_td"}).get_text())
        ds.tds += int(row.find("td", {"data-stat":"fumbles_rec_td"}).get_text())
        ds.tackles += int(row.find("td", {"data-stat":"tackles_solo"}).get_text())

    #get overall team table to grab time defense on field
    team_table = csoup.find("table", {"id":"team_stats"})

    for row in team_table.find_all("tr"):
        try:
            row.find("th", {"data-stat":"stat"}).get_text()
        except Exception:
            continue

        #find row with time of possession stat
        if row.find("th", {"data-stat":"stat"}).get_text() == "Time of Possession":

            #if they're the home team visitor time of possession is how long def on field and vice versa
            if home is True:
                opp_pos = row.find("td", {"data-stat":"vis_stat"}).get_text()
            else:
                opp_pos = row.find("td", {"data-stat":"home_stat"}).get_text()

            #manipulate string and convert time onfield into float
            opp_pos = opp_pos.split(":")
            seconds = float(opp_pos[1])/float(60)
            decimal = str(seconds).split(".")
            onfield = "{}.{}".format(opp_pos[0], decimal[1])
            ds.time_onfield = float(onfield)

    return


"""=====================================================================================================+
| This will grab the player stats for the passed in game                                                |
+====================================================================================================="""
def WeekFantasyPlayers(box_link, csoup, players):
    #get offensive table
    table = csoup.find("table", {"id":"player_offense"})

    #iterate over players on the team
    for player in players:
        p = players[player]
        pos = p.position.upper()

        #if this players position isn't in fantasy_pos or known, keep going as they're not likely to be important
        if pos not in fantasy_pos:
            continue

        #find the row for this player
        for row in table.find_all("th", {"data-append-csv":"{}".format(player)}):
            #get parent segment since the player id is in the head segment
            p_row = row.parent

            #set the QB stats
            try:
                if pos == "QB":
                    p.fant_stats[box_link] = QBStats()
                    qb = p.fant_stats[box_link]

                    qb.completions += int(p_row.find("td", {"data-stat":"pass_cmp"}).get_text())
                    qb.attempts += int(p_row.find("td", {"data-stat":"pass_att"}).get_text())
                    if qb.attempts > 0:
                        qb.accuracy += float(float(qb.completions)/float(qb.attempts) * float(100))
                    else:
                        qb.accuracy = 0
                    qb.interceptions += int(p_row.find("td", {"data-stat":"pass_int"}).get_text())
                    qb.fumbles += int(p_row.find("td", {"data-stat":"fumbles"}).get_text())
                    qb.pass_tds += int(p_row.find("td", {"data-stat":"pass_td"}).get_text())
                    qb.pass_yards += int(p_row.find("td", {"data-stat":"pass_yds"}).get_text())
                    qb.rush_tds += int(p_row.find("td", {"data-stat":"rush_td"}).get_text())
                    qb.rush_yards += int(p_row.find("td", {"data-stat":"rush_yds"}).get_text())
                    qb.rush_att += int(p_row.find("td", {"data-stat":"rush_att"}).get_text())
                    qb.sacked += int(p_row.find("td", {"data-stat":"pass_sacked"}).get_text())
                    if qb.attempts > 0:
                        qb.qbr += float(p_row.find("td", {"data-stat":"pass_rating"}).get_text())
                    else:
                        qb.qbr = 0

                #set skill position stats if they are not a QB
                else:
                    p.fant_stats[box_link] = SkillStats()
                    ss = p.fant_stats[box_link]

                    ss.rush_att += int(p_row.find("td", {"data-stat":"rush_att"}).get_text())
                    ss.rush_yards += int(p_row.find("td", {"data-stat":"rush_yds"}).get_text())
                    ss.rush_tds += int(p_row.find("td", {"data-stat":"rush_td"}).get_text())
                    ss.targets += int(p_row.find("td", {"data-stat":"targets"}).get_text())
                    ss.receptions += int(p_row.find("td", {"data-stat":"rec"}).get_text())
                    ss.rec_yards += int(p_row.find("td", {"data-stat":"rec_yds"}).get_text())
                    ss.rec_tds += int(p_row.find("td", {"data-stat":"rec_td"}).get_text())
                    ss.fumbles += int(p_row.find("td", {"data-stat":"fumbles"}).get_text())
            except Exception:
                continue

    return


"""=====================================================================================================+
| This will grab each of this players fantasy games for each week this season                           |
+====================================================================================================="""
def FantasyPoints(teams, year):
    #iterate over team
    for team in teams:
        print(team)
        #iterate over players
        t = teams[team]
        for player in t.players:
            #get player object and continue if fantasy position not in the list
            p = t.players[player]
            if not p.position.upper() in fantasy_pos:
                continue
            print(p.name)
            #request player fantasy page
            request = requests.get("{}{}/fantasy/{}/".format(url, p.link, year))

            #get soup object
            soup = BeautifulSoup(request.text, "lxml")
            table = soup.find("table", {"id":"player_fantasy"})

            #iterate over rows and store draftkings points using boxscores as an index
            try:
                for row in table.tbody.find_all("tr"):
                    boxscore = row.find(href=re.compile("boxscore")).get("href")
                    pts_text = row.find("td", {"data-stat":"draftkings_points"}).get_text()

                    try:
                        pts = float(pts_text)
                    except Exception:
                        pts = None

                    p.weekly_fantasy[boxscore] = pts
            except:
                continue

    return


"""=====================================================================================================+
| Write things to a file                                                                                |
+====================================================================================================="""
def WriteToFile(teams, year):
    #we're createing three different files
    file_type = ["skill", "qb", "def"]

    #depending on the file we're going to follow a different path
    for item in file_type:
        #for each week in this
        for week in range(1, 18):
            for team in teams:
                t = teams[team]
                try:
                    link = t.boxscores[week]
                except Exception:
                    continue

                aft_bye = t.after_bye == week

                if item != "def":
                    for player in t.players:
                        p = t.players[player]
                        opp = teams[t.weekly_opp[week]]

                        if p.position.upper() not in fantasy_pos:
                            continue

                        try:
                            st = p.fant_stats[link]
                        except Exception:
                            continue

                        try:
                            week_pts = p.weekly_fantasy[link]
                        except Exception:
                            continue

                        if item == "skill":
                            if p.position.upper() == "QB":
                                continue

                            fieldnames = ["player", "fant_pts", "position", "height", "weight", "rookie", "team", "opp", "home",
                                          "opp_def_align", "after_bye", "oline_rush", "oline_pass", "opp_dline_rush", "opp_dline_pass",
                                          "gametime", "gameday", "roof", "surface", "temp", "rel_hum", "wind", "wind_chill",
                                          "off_pass_rank", "off_rush_rank", "opp_def_pass_rank", "opp_def_rush_rank", "rush_att",
                                          "rush_yards", "rush_tds", "targets", "receptions", "rec_yards", "rec_tds", "fumbles"]

                            writepath = "{}\week{}\skill.csv".format(year, week)
                            mode = "a" if os.path.exists(writepath) else "w"

                            skillfile = open("{}\week{}\skill.csv".format(year, week), mode, newline="")
                            writer = csv.DictWriter(skillfile, fieldnames=fieldnames)
                            if mode == "w":
                                writer.writeheader()

                            writer.writerow({"player":p.name, "fant_pts":week_pts, "position":p.position, "height":p.height, "weight":p.weight,
                                             "rookie":p.is_rookie, "team":team, "opp":t.weekly_opp[week], "home":t.weekly_home[week],
                                             "opp_def_align":opp.def_alignment, "after_bye":aft_bye, "oline_rush":t.oline_rush, "oline_pass":t.oline_pass,
                                             "opp_dline_rush":opp.dline_rush, "opp_dline_pass":opp.dline_pass, "gametime":t.week_gametime[week],
                                             "gameday":t.week_gameday[week], "roof":t.week_roof[week], "surface":t.week_surface[week],
                                             "temp":t.week_weather[week]["Temp"], "rel_hum":t.week_weather[week]["Rel Humidity"], "wind":t.week_weather[week]["Wind"],
                                             "wind_chill":t.week_weather[week]["Wind Chill"], "off_pass_rank":t.off_pass_rank, "off_rush_rank":t.off_rush_rank,
                                             "opp_def_pass_rank":opp.def_pass_rank, "opp_def_rush_rank":opp.def_rush_rank, "rush_att":st.rush_att,
                                             "rush_yards":st.rush_yards, "rush_tds":st.rush_tds, "targets":st.targets, "receptions":st.receptions,
                                             "rec_yards":st.rec_yards, "rec_tds":st.rec_tds, "fumbles":st.fumbles})

                            skillfile.close()

                        else:
                            if p.position.upper() != "QB":
                                continue

                            fieldnames = ["player", "fant_pts", "position", "height", "weight", "rookie", "team", "opp", "home",
                                          "opp_def_align", "after_bye", "oline_rush", "oline_pass", "opp_dline_rush", "opp_dline_pass",
                                          "gametime", "gameday", "roof", "surface", "temp", "rel_hum", "wind", "wind_chill", "off_pass_rank",
                                          "off_rush_rank", "opp_def_pass_rank", "opp_def_rush_rank", "rush_att", "rush_yards", "rush_tds",
                                          "completions", "attempts", "accuracy", "interceptions", "fumbles", "pass_yards", "pass_tds",
                                          "sacked", "qbr"]

                            writepath = "{}\week{}\qb.csv".format(year, week)
                            mode = "a" if os.path.exists(writepath) else "w"

                            qbfile = open("{}\week{}\qb.csv".format(year, week), mode, newline="")
                            writer = csv.DictWriter(qbfile, fieldnames=fieldnames)

                            if mode == "w":
                                writer.writeheader()

                            writer.writerow({"player":p.name, "fant_pts":week_pts, "position":p.position, "height":p.height, "weight":p.weight,
                                             "rookie":p.is_rookie, "team":team, "opp":t.weekly_opp[week], "home":t.weekly_home[week],
                                             "opp_def_align":opp.def_alignment, "after_bye":aft_bye, "oline_rush":t.oline_rush, "oline_pass":t.oline_pass,
                                             "opp_dline_rush":opp.dline_rush, "opp_dline_pass":opp.dline_pass, "gametime":t.week_gametime[week],
                                             "gameday":t.week_gameday[week], "roof":t.week_roof[week], "surface":t.week_surface[week],
                                             "temp":t.week_weather[week]["Temp"], "rel_hum":t.week_weather[week]["Rel Humidity"], "wind":t.week_weather[week]["Wind"],
                                             "wind_chill":t.week_weather[week]["Wind Chill"], "off_pass_rank":t.off_pass_rank, "off_rush_rank":t.off_rush_rank,
                                             "opp_def_pass_rank":opp.def_pass_rank, "opp_def_rush_rank":opp.def_rush_rank, "rush_att":st.rush_att,
                                             "rush_yards":st.rush_yards, "rush_tds":st.rush_tds, "completions":st.completions, "attempts":st.attempts, "accuracy":st.accuracy,
                                             "interceptions":st.interceptions, "fumbles":st.fumbles, "pass_yards":st.pass_yards, "pass_tds":st.pass_tds,
                                             "sacked":st.sacked, "qbr":st.qbr})

                            qbfile.close()

                else:
                    opp = teams[t.weekly_opp[week]]
                    wd = t.week_def_stats[link]

                    fieldnames = ["team", "opp", "opp_pts", "opp_pass_yards", "opp_rush_yards", "def_align", "after_bye",
                                  "dline_pass", "dline_rush", "opp_oline_pass", "opp_oline_rush", "gametime", "gameday",
                                  "roof", "surface", "temp", "rel_hum", "wind", "wind_chill", "def_pass_rank", "def_rush_rank",
                                  "opp_pass_rank", "opp_rush_rank", "sacks", "forced_fumbles", "interceptions", "tds", "tackles", "time_onfield"]

                    writepath = "{}\week{}\def.csv".format(year, week)
                    mode = "a" if os.path.exists(writepath) else "w"

                    deffile = open("{}\week{}\def.csv".format(year, week), mode, newline="")
                    writer = csv.DictWriter(deffile, fieldnames=fieldnames)

                    if mode == "w":
                        writer.writeheader()

                    writer.writerow({"team":team, "opp":t.weekly_opp[week], "opp_pts":t.opp_score[week], "opp_pass_yards":t.opp_pass_yds[week],
                                     "opp_rush_yards":t.opp_rush_yds[week], "def_align":t.def_alignment, "after_bye":aft_bye, "dline_pass":t.dline_pass,
                                     "dline_rush":t.dline_rush, "opp_oline_pass":opp.oline_pass, "opp_oline_rush":opp.oline_rush, "gametime":t.week_gametime[week],
                                     "gameday":t.week_gameday[week], "roof":t.week_roof[week], "surface":t.week_surface[week], "temp":t.week_weather[week]["Temp"],
                                     "rel_hum":t.week_weather[week]["Rel Humidity"], "wind":t.week_weather[week]["Wind"], "wind_chill":t.week_weather[week]["Wind Chill"],
                                     "def_pass_rank":t.def_pass_rank, "def_rush_rank":t.def_rush_rank, "opp_pass_rank":opp.off_pass_rank, "opp_rush_rank":opp.off_rush_rank,
                                     "sacks":wd.sacks, "forced_fumbles":wd.forced_fumbles, "interceptions":wd.interceptions, "tds":wd.tds, "tackles":wd.tackles,
                                     "time_onfield":wd.time_onfield})

                    deffile.close()

    return


#########################################################################################################
#
# CLASS DEFINITIONS BELOW
#
#########################################################################################################
"""=====================================================================================================+
***This is a class that stores information regarding this team for the given year***
--------------
    name - team name
    coaches - team coaches (hc, oc, dc, other asst)
    players - players on this team
    link - link to the teams PFR page
    def_alignment - the defenses alignment that season
    boxscores - links to the teams games that year
    oline_rush - offensive line rush rank from http://www.footballoutsiders.com
    oline_pass - offensive line pass rank
    dline_rush - defensive line rank against rush
    dline_pass - defensive line rank against pass
    week_def_stats - weekly team defense stats object
    week_gametime - gametime for this week
    week_gameday - gameday for this week
    week_roof - stadium roof type for this week
    week_surface - playing surface this week
    week_weather - weather for this week
    weekly_opp - opponent this team played this week
    weekly_home - whether or not this team is home
    def_pass_rank - overall def pass rank
    def_rush_rank - overall def rush rank
    off_pass_rank - overall off pass rank
    off_rush_rank - overall off rush rank
+====================================================================================================="""
class TeamObj():
    def __init__(self, name, coaches, players, link):
        self.name = name
        self.coaches = coaches
        self.players = players
        self.link = link
        self.def_alignment = str
        self.boxscores = {}
        self.after_bye = int
        self.oline_rush = int
        self.oline_pass = int
        self.dline_rush = int
        self.dline_pass = int
        self.week_def_stats = {}
        self.week_gametime = {}
        self.week_gameday = {}
        self.week_roof = {}
        self.week_surface = {}
        self.week_weather = {}
        self.weekly_opp = {}
        self.weekly_home = {}
        self.def_pass_rank = int
        self.def_rush_rank = int
        self.off_pass_rank = int
        self.off_rush_rank = int
        self.opp_score = {}
        self.opp_pass_yds = {}
        self.opp_rush_yds = {}


"""=====================================================================================================+
***This is a class that stores a players name, position, and a link to their page***
--------------
    name - players full name
    position - players position
    team - team the player is on
    link - link to the players page
    height - players height
    weight - players weight
    is_rookie - whether or not this player was a rookie that season
    prev_season - this is their previous season output, if they are a rookie than this is their career college stats
    season_stats - overall stats for that season
    fant_stats - weekly fantasy stats for this object
+====================================================================================================="""
class PlayerObj():
    def __init__(self, name, position, team, link, weight, height, rook):
        self.name = name
        self.position = position
        self.team = team
        self.link = link
        self.height = height
        self.weight = weight
        self.is_rookie = rook
        #self.prev_season = {}
        #self.season_stats = {}
        self.weekly_fantasy = {}
        self.fant_stats = {}


""""====================================================================================================+
***This is a class that will link to the defensive stats and store all of the weekly defensive stats***
--------------
    sacks - team sacks
    forced_fumbles - times this defense forced a fumble
    interceptions - the number of interceptions by this team in this game
    tds - how many touchdowns this defense had this week
    tackles - how many tackles did this team make
    time_onfield - overall time that this defense was on the field this week
+====================================================================================================="""
class WeeklyTeamDefense():
    def __init__(self):
        self.sacks = float(0)
        self.forced_fumbles = int(0)
        self.interceptions = int(0)
        self.tds = int(0)
        self.tackles = int(0)
        self.time_onfield = float


"""=====================================================================================================+
***This is a player class that will store weekly passing stats object for that player***
--------------
    fantasy_pts - how many fantasy points this player scored this week
    completions - the number of completed passes by this qb
    attempts - the total number of pass attempts this qb had
    accuracy - completions / attempts
    interceptions - qb interceptions
    fumbles - fumbles this qb had
    pass_tds - total pass touchdowns by the qb this game
    pass_yards - total pass yards for the qb this game
    rush_tds - total rush touchdowns
    rush_yards - total rush yards for this player
    rush_att - total rush attempts
+====================================================================================================="""
class QBStats():
    def __init__(self):
        self.completions = int(0)
        self.attempts = int(0)
        self.accuracy = float(0)
        self.interceptions = int(0)
        self.fumbles = int(0)
        self.pass_tds = int(0)
        self.pass_yards = int(0)
        self.rush_tds = int(0)
        self.rush_yards = int(0)
        self.rush_att = int(0)
        self.sacked = int(0)
        self.qbr = float(0)


"""=====================================================================================================+
***This is a class that will store weekly rushing and receiving stats for use in the player object***
--------------
    fantasy_pts - how many fantasy points they scored
    rush_att - the number of rush attempts this player had
    rush_yards - total rush yards for this player this week
    targets - total number of receiving targets for this player
    receptions - number of receptions for this player
    rec_yards - number of receiving yards for this player
    rush_tds - number of rushing touchdowns for this player
    rec_tds - number of receiving touchdowns for this player
    fumbles - times this player fumbled
    redzone_att - redzone attempts for this player
    redzone_tds - redzone touchdowns for this player
+====================================================================================================="""
class SkillStats():
    def __init__(self):
        self.rush_att = int(0)
        self.rush_yards = int(0)
        self.rush_tds = int(0)
        self.targets = int(0)
        self.receptions = int(0)
        self.rec_yards = int(0)
        self.rec_tds = int(0)
        self.fumbles = int(0)


"""=====================================================================================================+
***This is a class for this player's season stats***
--------------
    stats from the previous season for this player (much of this is similar to above)
+====================================================================================================="""
class Season():
    def __init__(self):
        self.team = str
        self.starts = int
        self.games = int
        self.fant_rank = int
        self.fant_pts = int
        self.qb_rate = float
        self.completions = int
        self.pass_td = int
        self.pass_att = int
        self.pass_yards = int
        self.adj_ypa = float
        self.interceptions = int
        self.rush_td = int
        self.rush_att = int
        self.rush_yards = int
        self.targets = int
        self.rec_tds = int
        self.receptions = int
        self.rec_yards = int
        self.fumbles = int


#########################################################################################################
#
# THIS IS THE CALL TO THE MAIN FUNCTION
#
#########################################################################################################
if __name__ == "__main__":
    main()
