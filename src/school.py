import requests
from bs4 import BeautifulSoup 
import json
import sqlite3
import matplotlib.pyplot as plt 
import argparse
import re

class school():
    def __init__(self):
        self.conn = sqlite3.connect("../data/crimerecord.db") 
        self.c = self.conn.cursor() 
        
    def create_data_base(self): 
        # create database
        # creat TABLE school
        self.c.execute('DROP TABLE IF EXISTS SCHOOLS') 
        self.c.execute('CREATE TABLE Schools (school_id INTEGER PRIMARY KEY, rank INTEGER, name TEXT, score INTEGER)')
        
        
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
    
    def school(self):
        r=self.page_get('https://www.thecompleteuniversityguide.co.uk/league-tables/rankings')
        soup = BeautifulSoup(r.content, 'lxml')
        main_table=soup.findAll('table',{'class':"league-table-table"})[0]
        main_body = main_table.find('tbody')
        info_list=[]

        i=0
        while i<102:
            if i==6 or i==17:
                i+=1
                pass
            elif main_body.findAll('tr')[i]:
                school=main_body.findAll('tr')[i]
                school_rank = school.findAll('td')[1].text
                school_rank=int(re.findall(r"\d+\.?\d*",school_rank)[0])
                school_name = school.findAll('td')[3].find('a').text
                school_score = school.findAll('td')[8].text
                school_score=int(re.findall(r"\d+\.?\d*",school_score)[0])
                dic={}
                dic['rank']=school_rank
                dic['name']=school_name
                dic['score']=school_score
                info_list.append(dic)
                i+=1
        
        self.create_data_base()
        i=0
        while i<len(info_list):
            self.c.execute('INSERT INTO Schools(school_id,rank,name,score) VALUES(?,?,?,?)',(i,info_list[i]['rank'],info_list[i]['name'],info_list[i]['score']))
            i+=1
        self.conn.commit()

    def school_test(self):
        r=self.page_get('https://www.thecompleteuniversityguide.co.uk/league-tables/rankings')
        soup = BeautifulSoup(r.content, 'lxml')
        main_table=soup.findAll('table',{'class':"league-table-table"})[0]
        main_body = main_table.find('tbody')
        info_list=[]

        i=0
        while i<40:
            if i==6 or i==17:
                i+=1
                pass
            elif main_body.findAll('tr')[i]:
                school=main_body.findAll('tr')[i]
                school_rank = school.findAll('td')[1].text
                school_rank=int(re.findall(r"\d+\.?\d*",school_rank)[0])
                school_name = school.findAll('td')[3].find('a').text
                school_score = school.findAll('td')[8].text
                school_score=int(re.findall(r"\d+\.?\d*",school_score)[0])
                dic={}
                dic['rank']=school_rank
                dic['name']=school_name
                dic['score']=school_score
                info_list.append(dic)
                i+=1
        
        self.create_data_base()
        i=0
        while i<len(info_list):
            self.c.execute('INSERT INTO Schools(school_id,rank,name,score) VALUES(?,?,?,?)',(i,info_list[i]['rank'],info_list[i]['name'],info_list[i]['score']))
            i+=1
        self.conn.commit()


        
