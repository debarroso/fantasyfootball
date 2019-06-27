'''
File: getEmptyRows.py
File Created: Saturday, 23rd June 2018 3:39:32 pm
Author: Oliver DeBarros (debarros.oliver@gmail.com)
Description: 
    Find plays that don't have a time in the pbp files
'''

import csv


'''---------------------------------------------------------------------------+
| Call into this files main function
+---------------------------------------------------------------------------'''
def main():
    for year in range(2008, 2009):#2018):
        for week in range(1, 2):#18):
            pbp_file = open("{}\\week{}\\weekpbp.csv".format(year, week), "r")
            reader = csv.DictReader(pbp_file)

            print(week)
            for row in reader:
                if not (row['time']):
                    print(row['detail'] + "|" + row['yards'])
            
            pbp_file.close()


if __name__ == "__main__":
    main()