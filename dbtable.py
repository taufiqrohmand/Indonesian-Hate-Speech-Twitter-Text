#import module
import pandas as pd
import sqlite3 as sq3

#Create connection database
conn = sq3.connect('Dataset/dataset_processing.db')

#Create table
try:
    conn.execute("""CREATE TABLE abusive (text varchar(255));""")
    conn.execute("""CREATE TABLE alayset (alay varchar(255), normal varchar(255));""")
    print("Table has been create")
except:
    print("Table already exist")


#import data to dataframe
df_abusive = pd.read_csv("Dataset/abusive.csv", names = ['label'], encoding = 'latin-1', header = None)
df_alay = pd.read_csv("Dataset/new_kamusalay.csv", names = ['alay', 'normal'], encoding = 'latin-1', header = None)


#import dataframe to database
df_abusive.to_sql(name='abusive', con=conn, if_exists = 'replace', index = False)
df_alay.to_sql(name='alayset', con=conn, if_exists = 'replace', index = False)

#assign change
conn.commit()

#close connection
conn.close()