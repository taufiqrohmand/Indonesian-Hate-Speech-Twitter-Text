#import module
import re
import pandas as pd
import sqlite3 as sq3
import emoji


from unidecode import unidecode

#connect to database
conn = sq3.connect('Dataset/dataset_processing.db', check_same_thread=False)

#Function clean
def clean_text(text):
    #Lowercasing all the letters
    text = text.lower()
    #Remove ascii2
    text = re.sub(r'\\x[A-Za-z0-9./]+','', unidecode(text))
    #Remove emoji
    #text = re.sub(emoji.get_emoji_unicode_dict(), r'', text)
    #Remover every \\n
    text = re.sub(r'\\n',' ', text)
    #Remove punctuations only show alphabets
    text = re.sub(r"[^\w\d\s]+", " ",text)
    #Remove every new line
    text = re.sub(r'\n', ' ',text)
    #Remove space
    text = re.sub('  +', ' ',text)
    #Remover every url
    text = re.sub('url','', text)
    #remove web url
    text = re.sub(r'http\S+', '', text, flags=re.MULTILINE)
    #Remove rt (retweet)
    text = re.sub('rt ',' ', text)
    #remove word user
    text = text.replace('user', '')
    #remove space in and out
    text = text.strip()
    return text


#Function Change Alay to Normal
def change_alay(text):
    #Dataframe from SQL query
    df_alay = pd.read_sql_query('select * from alayset', conn)
    #Dataframe convert to dictionari
    dict_alay = dict(zip(df_alay['alay'], df_alay['normal'])) 
    for word in dict_alay:
        change_word = ' '.join([dict_alay[word] if word in dict_alay else word for word in text.split(' ')])
        return change_word

def removeSensor(str):
    Sensor = 'aiueo'
    for ele in Sensor:
        str = str.replace(ele, 'x')
    return str

#Sensor abusive word
def sensor_abusive(text):
    df_abusive = pd.read_sql_query('select * from abusive',conn)
    dict_abusive = dict(zip(df_abusive['label'],df_abusive['label']))
    text = text.split()
    text_normal = ''
    for str in text:
        if(bool(str in dict_abusive)):
            str = removeSensor(str)
            text_normal = text_normal + ' ' + str
        else:
            text_normal = text_normal + ' ' + str  
    text_normal = text_normal.strip()
    return text_normal
    

#Function Cleansing
def cleansing(text):
    
    text = clean_text(text)
    text = change_alay(text)
    text = sensor_abusive(text)

    return text