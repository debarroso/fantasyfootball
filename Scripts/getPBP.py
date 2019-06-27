'''
File: getPBP.py
File Created: Monday, 18th June 2018 12:50:41 am
Author: Oliver DeBarros (debarros.oliver@gmail.com)
Description: 
    This script will get all of the plays for each team of the season
'''

from bs4 import BeautifulSoup
import csv
import requests
import re
import getPFR as pfr

teams = []
url = "https://www.pro-football-reference.com/play-index/play_finder.cgi?request=1&match=summary_all&"

'''---------------------------------------------------------------------------+
| Call into main function
+---------------------------------------------------------------------------'''
def main():
    links = pfr.GetTeamLinks()
    for link in links:
        teams.append(link.replace("teams", "").replace("/", ""))

    for year in range(2008, 2018):
        for week in range(1, 18):
            f = open("{}\\week{}\\weekpbp.csv".format(year, week), "w", newline="")
            header = [
                "game_id", "team", "opp", "player_id", "quarter", "time", "down",
                "togo", "location", "score", "detail", "yards", "touchdown"
            ]
            writer = csv.DictWriter(f, header)
            writer.writeheader()

            for team in teams:
                print("{}|{}|{}".format(year, week, team))
                params = "year_min={}&year_max={}&team_id={}&game_type=R&week_num_min={}&week_num_max={}&no_play=N".format(year, year, team, week, week)
                r = requests.get(url + params)

                soup = BeautifulSoup(r.text, "lxml")

                try:
                    table = soup.find("table", {"id": "all_plays"}).find("tbody")
                except:
                    continue

                ParseTable(table, team, writer)
        
            f.close()


def ParseTable(table, team, writer):
    for row in table.find_all("tr"):
        for player in row.find_all(href=re.compile("players")):
            writer.writerow({
                "game_id": row.find(href=re.compile("boxscores")).get("href")[11:-4],
                "team": row.find("td", {"data-stat": "team"}).find(href=re.compile("teams")).get("href")[7:-1],
                "opp": row.find("td", {"data-stat": "opp"}).find(href=re.compile("teams")).get("href")[7:-1],
                "player_id": player.get("href")[11:-4],
                "quarter": row.find("td", {"data-stat": "quarter"}).get_text(),
                "time": row.find("td", {"data-stat": "qtr_time_remain"}).get_text(),
                "down": row.find("td", {"data-stat": "down"}).get_text(),
                "togo": row.find("td", {"data-stat": "yds_to_go"}).get_text(),
                "location": getLocation(team, row),
                "score": row.find("td", {"data-stat": "score"}).get_text(),
                "detail": row.find("td", {"data-stat": "description"}).get_text(),
                "yards": row.find("td", {"data-stat": "yards"}).get_text() if len(row.find("td", {"data-stat": "yards"}).get_text()) > 0 else 0,
                "touchdown": ("touchdown" in row.find("td", {"data-stat": "description"}).get_text())
            })

def getLocation(team, row):
    row_text = row.find("td", {"data-stat": "location"}).get_text()
    yardline = re.findall(r'\d+', row_text)
    
    try:
        if team in row_text.lower():
            return int(yardline[0]) + 50
    
        else:
            return int(yardline[0])

    except:
        return None


if __name__ == "__main__":
    main()