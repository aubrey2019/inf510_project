import requests
from bs4 import BeautifulSoup 
import json
import sqlite3
import matplotlib.pyplot as plt 
import argparse
import re

class coordinate():
    def __init__(self):
        self.conn = sqlite3.connect("../data/crimerecord.db") 
        self.c = self.conn.cursor() 
    
    def create_data_base(self): 
        # create database
        # creat TABLE coordinate 
        self.c.execute('DROP TABLE IF EXISTS Coordinates') 
        self.c.execute('CREATE TABLE Coordinates (school_id INTEGER PRIMARY KEY,name TEXT, lat FLOAT, lng FLOAT)')
    
    def page_get(self, url):
    # check status of url/api 
        try:
            p = requests.get(url)
            p.raise_for_status()
        except requests.exceptions.ConnectionError:
            print("Connection Error")
            return None
        except requests.exceptions.HTTPError:
            print("HTTP Error")
            return None 
        else:
            return p
    
    def coordinate(self,place):
        url='https://maps.googleapis.com/maps/api/geocode/json?address='+place+',uk&key=AIzaSyA8bDB0t3qqvvvOtwTrcxm0_lfX28UG8ZQ'
        a=self.page_get(url)
        j=json.loads(a.content)
        x=j['results'][0]['geometry']['location']['lat']
        y=j['results'][0]['geometry']['location']['lng']
        return (x,y)
    
    def store_coordinate(self):
        self.create_data_base()
        sql="SELECT school_id,name FROM schools order by school_id" 
        self.c.execute(sql)
        results = self.c.fetchall()
        
        for school in results:
            (lat,lng)=self.coordinate(school[1])
            self.c.execute('INSERT INTO coordinates(school_id,name,lat,lng) VALUES(?,?,?,?)',(school[0],school[1],lat,lng))
        
        self.conn.commit()

        
        
