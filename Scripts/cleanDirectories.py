'''
File: cleanDirectories.py
File Created: Sunday, 24th June 2018 12:04:21 pm
Author: Oliver DeBarros (debarros.oliver@gmail.com)
Description: 
    Runs through pfr directories and removes unnecessary files
'''

import os

for year in range(2008, 2018):
    for week in range(1, 18):
        filepath = "{}\\week{}\\".format(year, week)
        os.remove(filepath + "qb.csv")
        os.remove(filepath + "skill.csv")
        os.rename(filepath + "def.csv", filepath + "def_stats.csv")