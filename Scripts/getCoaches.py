'''
File: getCoaches.py
File Created: Sunday, 17th June 2018 9:31:47 pm
Author: Oliver DeBarros (debarros.oliver@gmail.com)
Description: 
    This script generates csv files for each teams coaches for each season.
'''

import csv
import getPFR as pfr


'''---------------------------------------------------------------------------+
| Call into the main function
+---------------------------------------------------------------------------'''
def main():

    #get team links once
    team_links = pfr.GetTeamLinks()
    
    #iterate over years
    for year in range(2009, 2018):
        teams = pfr.CreateTeamObjs(team_links, year)
        writeCoaches(teams, year)


'''---------------------------------------------------------------------------+
| Write this seasons coaches to a separate csv file 
+---------------------------------------------------------------------------'''
def writeCoaches(teams, year):
    fieldnames = ["ID", "Name", "Team", "Role", "Season"]
    f = open("{}\\coaches.csv".format(year), "w", newline='')
    writer = csv.DictWriter(f, fieldnames)
    writer.writeheader()

    for team in teams:
        t = teams[team]

        for coach in t.coaches:
            c = t.coaches[coach]
            writer.writerow({"ID": c["link"][9:-4], "Name": c["name"], "Team": team, "Role": coach, "Season": year})
    
    f.close()

if __name__ == "__main__":
    main()