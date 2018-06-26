# -*- coding: utf-8 -*-
"""
Created on Wed Jun 13 11:27:33 2018

@author: raghug
"""

from sqlalchemy import create_engine
from pandas import DataFrame
import configparser

config = configparser.ConfigParser()
try:
    config.read('app.conf')
except Exception as e:
    print(str(e))

connect = None

def get_dataframe(query):
    try:
        mysql = config['MYSQL']
        
        mysql_conf = "mysql://%s:%s@%s:%s/%s" %(mysql['user'], mysql['pass'], mysql['host'], mysql['port'], mysql['schema'])
        
        engine = create_engine(mysql_conf)
        
        connect = engine.connect()
        
        cursor = connect.execute(query)
        
        df = DataFrame(cursor.fetchall(), columns=cursor.keys())
        
        df.to_csv('speciality_info.csv')
        
        return df
        
    except Exception as e:
        print(str(e))
    finally:
        if connect : connect.close()