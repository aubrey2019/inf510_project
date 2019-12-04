import requests
from bs4 import BeautifulSoup 
import json
import sqlite3
import matplotlib.pyplot as plt 
import argparse
import re
import pandas as pd
import matplotlib
from school import school
from coordinate import coordinate
from crime import crime
from analysis import analysis


def parse_args():
    description='you should add those parameters'
    parser=argparse.ArgumentParser(description=description)
    parser.add_argument('--remote',type=str,help='for remote use')
    parser.add_argument('--local',type=str,help='for local use')
    parser.add_argument('--test',type=str,help='for test use')
    
    args=parser.parse_args()
    return args
   
if __name__ == '__main__':
    args = parse_args()
    if args.remote:
        print("\n\n###################### Getting UK Top 100 Universitied ######################")      
        s = school()
        s.school()
        print("\n\n###################### Data Management complete ######################")
        
        print("\n\n###################### Getting Coordinate Data ######################")
        c=coordinate()
        c.store_coordinate()
        print("\n\n###################### Data Management complete ######################")
        
        print("\n\n###################### Searching Crime Records ######################")
        crime=crime()
        crime.store_record()
        print("\n\n###################### Data Management complete ######################")

        a=analysis()
        a.STAT()
        a.query()



        

    elif args.local:
        a=analysis()
        a.STAT()
        a.query()

    elif args.test:
        print("For test, we only get data for top 38 schools")
        print("\n\n###################### Getting UK Top 38 Universitied ######################")      
        s = school()
        s.school_test()
        print("\n\n###################### Data Management complete ######################")
        
        print("\n\n###################### Getting Coordinate Data ######################")
        c=coordinate()
        c.store_coordinate()
        print("\n\n###################### Data Management complete ######################")
        
        print("\n\n###################### Searching Crime Records ######################")
        crime=crime()
        crime.store_record()
        print("\n\n###################### Data Management complete ######################")

        a=analysis()
        a.STAT()
        a.query()
    else:
        print("Not available Parameter")





