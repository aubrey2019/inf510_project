import requests
from bs4 import BeautifulSoup 
import json
import sqlite3
import matplotlib.pyplot as plt 
import argparse
import re

class crime():
    def __init__(self):
        self.conn = sqlite3.connect("../data/crimerecord.db") 
        self.c = self.conn.cursor()
    
    def create_data_base(self): 
        # create database
        # creat TABLE coordinate 
        self.c.execute('DROP TABLE IF EXISTS Records') 
        self.c.execute('CREATE TABLE Records(school_id INTEGER, name TEXT, month TEXT)')

    
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
    
    def get_record(self,month,lat,lng):
        try:
            url='https://data.police.uk/api/crimes-at-location?date=2019-'+month+'&lat='+lat+'&lng='+lng
            r=self.page_get(url)
            j=json.loads(r.content)
            cate={}
            for x in j:
                t=x['category']
                cate[t]=1+cate.get(t,0)
            return cate
        except:
            return None
    
    def store_record(self):
        self.create_data_base()
        
        sql="SELECT * FROM coordinates order by school_id" 
        self.c.execute(sql)
        results = self.c.fetchall()
        
        #get all the records for ecah school from Jan. to Oct, 2019
        info_list=[]
        
        for school in results:
            dic={}
            dic['school_id']=school[0]
            dic['name']=school[1]
            dic['records']={}
            month=1
            while month<11:
                a=self.get_record(str(month),str(school[2]),str(school[3]))
                dic['records']['2019-'+str(month)]=a
                month+=1
            info_list.append(dic)
         
        #count the total types of crime records
        crime_type=[]
        for school in info_list:
            ctype=school['records'].values()
            for x in ctype:
                if x is not None:
                    crime_type.extend(x.keys())
        crime_type=list(set(crime_type))

        #add these types to records table
        for x in crime_type:
            self.c.execute(f"alter table Records add '{x}' Integer ")
            
        #store data
        for school in info_list:
            for record in school['records'].keys():
                try:
                    self.c.execute('''INSERT INTO Records 
                    (school_id, name, month, drugs, 'vehicle-crime', shoplifting, burglary, robbery, 
                    'anti-social-behaviour', 'possession-of-weapons', 'public-order', 'bicycle-theft',
                    'theft-from-the-person', 'other-theft', 'violent-crime', 'criminal-damage-arson', 'other-crime') 
                    values(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)
                    ''',(school['school_id'],school['name'],record, school['records'][record].get('drugs',0),\
                        school['records'][record].get('vehicle-crime',0),\
                        school['records'][record].get('shoplifting',0),\
                        school['records'][record].get('burglary',0),\
                        school['records'][record].get('robbery',0),\
                        school['records'][record].get('anti-social-behaviour',0),\
                        school['records'][record].get('possession-of-weapons',0),\
                        school['records'][record].get('public-order',0),\
                        school['records'][record].get('bicycle-theft',0),\
                        school['records'][record].get('theft-from-the-person',0),\
                        school['records'][record].get('other-theft',0),\
                        school['records'][record].get('violent-crime',0),\
                        school['records'][record].get('criminal-damage-arson',0),\
                        school['records'][record].get('other-crime',0)))
                except:
                    pass


        self.conn.commit()
        
       
    
    