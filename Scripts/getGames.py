'''
File: getGames.py
File Created: Sunday, 17th June 2018 10:50:56 pm
Author: Oliver DeBarros (debarros.oliver@gmail.com)
Description: 
    Gets all of the games for the season
'''

from bs4 import BeautifulSoup
import csv
import requests
import re

url = "https://www.pro-football-reference.com/years/"


'''---------------------------------------------------------------------------+
| Call into this scripts main file
+---------------------------------------------------------------------------'''
def main():
    for year in range(2009, 2018):
        r = requests.get("{}{}/games.htm".format(url, year))
        soup = BeautifulSoup(r.text, "lxml")

        table = soup.find("table", {"id": "games"})
        writeTableRows(table.find_all("tr"), year)


'''---------------------------------------------------------------------------+
| This method will parse the table object and write the contents to a file
+---------------------------------------------------------------------------'''
def writeTableRows(table, year):
    f = open("{}\\games.csv".format(year), "w", newline="")
    header = ["Game_ID", "Week", "Day", "Home", "Winner", "Loser", "W_Pts", "L_Pts",
              "W_Yards", "L_Yards", "TOW", "TOL"]

    writer = csv.DictWriter(f, fieldnames=header)
    writer.writeheader()

    for row in table:
        week = row.find("th", {"data-stat": "week_num"}).get_text()
        if week.isdigit():
            game_id = row.find(href=re.compile("boxscore")).get("href")
            winner = row.find("td", {"data-stat": "winner"}).find(href=re.compile("teams")).get("href")
            loser = row.find("td", {"data-stat": "loser"}).find(href=re.compile("teams")).get("href")
            row_dict = {"Game_ID": game_id[11:-4],
                        "Week": int(week),
                        "Day": row.find("td", {"data-stat": "game_day_of_week"}).get_text(),
                        "Home": game_id[-7:-4],
                        "Winner": winner[7:10],
                        "Loser": loser[7:10],
                        "W_Pts": row.find("td", {"data-stat": "pts_win"}).get_text(),
                        "L_Pts": row.find("td", {"data-stat": "pts_lose"}).get_text(),
                        "W_Yards": row.find("td", {"data-stat": "yards_win"}).get_text(),
                        "L_Yards": row.find("td", {"data-stat": "yards_lose"}).get_text(),
                        "TOW": row.find("td", {"data-stat": "to_win"}).get_text(),
                        "TOL": row.find("td", {"data-stat": "to_lose"}).get_text()}
            
            writer.writerow(row_dict)

    f.close()            


if __name__ == "__main__":
    main()
