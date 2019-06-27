'''
File: addPlayerID.py
File Created: Saturday, 23rd June 2018 11:44:05 pm
Author: Oliver DeBarros (debarros.oliver@gmail.com)
Description: 
    This will identify the players from each team and add
    their player id to the stats files
'''

import getPFR as pfr
import csv

'''---------------------------------------------------------------------------+
| Define main function
+---------------------------------------------------------------------------'''
def main():
    team_links = pfr.GetTeamLinks()
    for year in range(2008, 2018):
        teams = pfr.CreateTeamObjs(team_links, year)

        insertIDs(teams, year, "qb")
        insertIDs(teams, year, None)


def insertIDs(teams, year, position):
    for week in range(1, 18):
        if (position == "qb"):
            f = open("{}\\week{}\\qb.csv".format(year, week), "r")
        else:
            f = open("{}\\week{}\\skill.csv".format(year, week), "r")

        reader = csv.DictReader(f)
        header = list(reader.fieldnames)        
        header.insert(0, "player_id")

        if (position == "qb"):
            w = open("{}\\week{}\\qb_stats.csv".format(year, week), "w", newline="")
        else:
            w = open("{}\\week{}\\non-qb_stats.csv".format(year, week), "w", newline="")

        writer = csv.DictWriter(w, fieldnames=header)
        writer.writeheader()

        for row in reader:
            t = teams[row["team"]]
            for player in t.players:
                p = t.players[player]
                if (row["player"] == p.name and row["position"] == p.position):
                    player_id = p.link[11:-4]
                    row["player_id"] = player_id
            if not row["fant_pts"]:
                row["fant_pts"] = 0
            row["position"] = row["position"].upper()
            writer.writerow(row)
        
        f.close()
        w.close()


if __name__ == "__main__":
    main()