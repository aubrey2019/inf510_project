import requests
from bs4 import BeautifulSoup 
import json
import sqlite3
import matplotlib.pyplot as plt 
import argparse
import re
import pandas as pd
import matplotlib


class analysis():
    def __init__(self):
        self.conn = sqlite3.connect("../data/crimerecord.db") 
        self.c = self.conn.cursor() 
        
    def create_data_base(self): 
        # create database
        # creat TABLE  recordwith total
        
        self.c.execute('DROP TABLE IF EXISTS Records2') 
        self.c.execute('CREATE TABLE Records2 (school_id Integer, name Text, month Text,Total Integer)')
    
    def STAT(self):
        print("\n\n###################### CRIME RECORDS DISTRIBUTIONS ######################") 
        self.create_data_base()
        
        sql="""select *,(drugs+"vehicle-crime"+shoplifting+burglary+robbery+"anti-social-behaviour"+"possession-of-weapons"+"public-order"+ "bicycle-theft"+
                    "theft-from-the-person"+ "other-theft"+ "violent-crime"+ "criminal-damage-arson"+"other-crime") as Total from Records """
        self.c.execute(sql)
        results = self.c.fetchall()
    
        for result in results:
            self.c.execute("""Insert into Records2 (school_id,name,month,Total) VALUES (?,?,?,?) """,(result[0],result[1],int(result[2].split('-')[1]),result[-1]))
        self.conn.commit()   
        
        # visulize Top 10 schools that have the most crime records
       
        self.c.execute('DROP TABLE IF EXISTS RecordsBySchool') 
        self.c.execute('CREATE TABLE RecordsBySchool (school_id Integer, name Text,Total Integer)')
        sql='select school_id,name,sum(Total) from Records2 GROUP BY name ORDER BY sum(Total) DESC'
        self.c.execute(sql)
        results = self.c.fetchall()
        x=[]
        y=[]
        for result in results:
            self.c.execute("""Insert into RecordsBySchool (school_id,name,Total) VALUES (?,?,?) """,(result[0],result[1],result[2]))
            x.append(result[1])
            y.append(result[2])
        
        self.conn.commit()   
        
        r=(list(results))[0:10]
        r.reverse()
        
        df=pd.DataFrame(list(r))
        cols=['school_id','name','crime records']
        df.columns=cols
        df.plot.barh(x='name', y='crime records',title='TOP 10 SCHOOLS WITH HIGHEST CRIME RECORDS')
        plt.tight_layout()
        plt.savefig('Top 10  dangerous schools.jpg')
     
        
      
        # visulize crime records' distribution by month
       
        self.c.execute('DROP TABLE IF EXISTS RecordsByMonth') 
        self.c.execute('CREATE TABLE RecordsByMonth (school_id Integer, month Integer,Total Integer)')
        sql='select school_id,month,sum(Total) from Records2 GROUP BY month ORDER BY month'
        self.c.execute(sql)
        results = self.c.fetchall()
        for result in results:
            self.c.execute("""Insert into RecordsByMonth (school_id,month,Total) VALUES (?,?,?) """,(result[0],result[1],result[2]))
        
        self.conn.commit()   
        
        
        r=list(results)
        r.append(results[1])
        del r[1]
        #r.reverse()
        df=pd.DataFrame(list(r))
        cols=['school_id','month','crime records']
        df.columns=cols
        df.plot(x='month', y='crime records',title='CRIME RECORDS DISTRIBUTION BY MONTH')
        plt.savefig('crime records distruibution by month.jpg')
        plt.tight_layout()
        promptword='\n\nThe two basic statistical figures have been saved in the same path.'
        print(promptword)


        
        
        
    def query(self):

        INPUT=0

        while INPUT!=8:
            promptword='\n\n\nFor Query 2,4,5, the figure results will be saved in the same path.\n'
            print(promptword)
        

            INPUT=input('INPUT A NUMBER TO MAKE YOUR QUERY\n \
            1.Get shcool\'s rank and location informations;\n \
            2.Get a school\'s crime records;\n \
            3.Get a month\'s crime records;\n \
            4.Get the trend for a type of crime in UK;\n \
            5.Get the trend for a type of crime of a school;\n \
            6.Get the top 10 dangerous school;\n \
            7.Get the school without crime records;\n \
            8.Quit.\n')

  
            
            if INPUT=='1':
                self.c.execute("""select s.rank,s.name,c.lat,c.lng from Schools s left join Coordinates c on s.school_id=c.school_id """)
                results = self.c.fetchall()
                df=pd.DataFrame(results)
                cols=["rank","name","lat","lng"]
                df.columns=cols
                print(df)
             
                
            
            elif INPUT=='2':
                try:
                    school=input('Input the school name you want to query :\n')
                    self.c.execute(f"""select * from Records where name='{school}' """)
                    results = self.c.fetchall()
                except:
                    print("Please input a correct name")
                cols=["school_id","name","month","drugs","vehicle-crime","shoplifting","burglary","robbery","anti-social-behaviour","possession-of-weapons","public-order", "bicycle-theft","theft-from-the-person", "other-theft","violent-crime", "criminal-damage-arson","other-crime"]
                df=pd.DataFrame(results)
                df.columns=cols
                print(df)
                
                dic={}
                for x in cols[3:-1]:
                    if df[x].sum()!=0 and x!='other-crime':
                        dic[x]=df[x].sum()
                
                a=sorted(dic.items(),key=lambda item:item[1])
                a=pd.DataFrame(a)
                a.plot.barh(x=0,y=1,label='Records',title='Crime Records of '+school+" by crime type")
                plt.tight_layout()
                plt.savefig('Crime Records of '+school+" by crime type"+'.jpg')
                
               
            
            elif INPUT=='3':
                try:
                    month=input('Input the month you want to query :\n')
                    month='2019-'+month
                    self.c.execute(f"""select "month",sum("drugs"),sum("vehicle-crime"),sum("shoplifting"),\
                          sum("burglary"),sum("robbery"),sum("anti-social-behaviour"),\
                          sum("possession-of-weapons"),sum("public-order"),sum("bicycle-theft"),\
                          sum("theft-from-the-person"),sum("other-theft"),\
                          sum("violent-crime"),sum("criminal-damage-arson"),sum("other-crime") \
                          from Records where month='{month}' GROUP BY month""")
                    results = self.c.fetchall()
                    cols=["month","drugs","vehicle-crime","shoplifting","burglary","robbery","anti-social-behaviour","possession-of-weapons","public-order", "bicycle-theft","theft-from-the-person", "other-theft","violent-crime", "criminal-damage-arson","other-crime"]
                    df=pd.DataFrame(results)
                    df.columns=cols
                    print(df)
                except:
                    print("Please input a correct month")
                
                    
            elif INPUT=='4':
                try:
                    crimetype=input('Please choose a type from["drugs","vehicle-crime","shoplifting","burglary","robbery","anti-social-behaviour","possession-of-weapons","public-order", "bicycle-theft","theft-from-the-person", "other-theft","violent-crime", "criminal-damage-arson"] to make a query :\n')
                    ct='"'+crimetype+'"'
                    self.c.execute(f"""select month, sum({ct}) from Records Group by month""")
                    results = self.c.fetchall()
                    results=list(results)
                    results.append(results[1])
                    del results[1]
                    cols=["month",crimetype]
                    df=pd.DataFrame(results)
                    df.columns=cols
                    df.plot(x="month",y=crimetype,title='CRIME RECORDS DISTRIBUTION of '+crimetype+' BY MONTH')
                    plt.tight_layout()
                    plt.savefig('CRIME RECORDS DISTRIBUTION of '+crimetype+' BY MONTH'+'.jpg')

                except:
                    print("Please input a correct crimetype")
                
            
            
            
            elif INPUT=='5':
                try:
                    crimetype=input('Please choose a type from["drugs","vehicle-crime","shoplifting","burglary","robbery","anti-social-behaviour","possession-of-weapons","public-order", "bicycle-theft","theft-from-the-person", "other-theft","violent-crime", "criminal-damage-arson"] to make a query :\n')
                    ct='"'+crimetype+'"'
                    schoolname=input("Please input the school you want to view:\n")
                    self.c.execute(f"""select month, sum({ct}) from Records where name="{schoolname}" Group by month""")
                    results = self.c.fetchall()
                    results=list(results)
                    results.append(results[1])
                    del results[1] 
                    cols=["month",crimetype]
                    df=pd.DataFrame(results)
                    df.columns=cols
                    df.plot(x="month",y=crimetype,title='CRIME RECORDS DISTRIBUTION of '+crimetype+ ' in ' +schoolname+' BY MONTH')
                    plt.tight_layout()
                    plt.savefig('CRIME RECORDS DISTRIBUTION of '+crimetype+ ' in ' +schoolname+' BY MONTH'+'.jpg')

                except:
                    print("Please input a correct crimetype and school name")
                
             
            
            
            
            
            elif INPUT=='6':
                self.c.execute("""select name, Total from RecordsBySchool order by Total DESC """)
                results = self.c.fetchall()
                df=pd.DataFrame(results[0:10])
                cols=["name","Total Crime Records"]
                df.columns=cols
                print(df)
     
                
                
                
                
            elif INPUT=='7':
                self.c.execute("""select name, Total from RecordsBySchool where Total=0 """)
                results = self.c.fetchall()
                df=pd.DataFrame(results)
                cols=["name","Total Crime Records"]
                df.columns=cols
                print(df)
                
               
                
            elif INPUT=='8':
                break
                
            else:
                print("please enter a correct number")

 

        return df
                
#test 
#a=analysis()
#a1=a.STAT()
#a2=a.query()

                
            

        
        
