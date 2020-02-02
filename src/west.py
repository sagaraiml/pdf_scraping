
# -*- coding: utf-8 -*-
"""
Created on Dec 2019

@author: Sagar_Paithankar
"""
import sys
import os
path = r'G:\Anaconda_CC\scraping'
os.chdir(path)
import logging
from datetime import datetime, timedelta
from tabula import read_pdf
import numpy as np
import pandas as pd
import requests, json
from helpers import apis
from helpers import email_alert
import linecache

#long_date = (datetime.now() - timedelta(1))
#region = None

logger = logging.getLogger('WR_Data_Inserstion')
try:
    hdlr = logging.FileHandler(path + '/logs/WR_{a}.log'.format(a=datetime.now().strftime("%y%h%d%H%M")))
except FileNotFoundError:
    os.mkdir('logs')
    hdlr = logging.FileHandler(path + '/logs/WR_{a}.log'.format(a=datetime.now().strftime("%y%h%d%H%M")))
formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
hdlr.setFormatter(formatter)
logger.addHandler(hdlr)
logger.setLevel(logging.INFO)
logger.info('Data Insertion Started')

def get_exception():
    exc_type, exc_obj, tb = sys.exc_info()
    f = tb.tb_frame
    line_no = tb.tb_lineno
    filename = f.f_code.co_filename
    linecache.checkcache(filename)
    line = linecache.getline(filename, line_no, f.f_globals)
    return filename, line_no, line.strip(), exc_obj

def get_data(long_date):
    try:
        print("here we are going for >> ", long_date.date()) 
        #region = "WR"
        d = long_date.strftime("%Y-%m-%d")
        url = "http://59.185.241.150:8080/pentaho/api/repos/%3Ahome%3Awrldc%3AControl%20Room%3APower%20Supply%20Position%20Report.prpt/report?userid=wrldc&password=password&output-target=pageable%2F"+\
        "pdf&Date="+d+\
        "T15%3A31%3A08.000%2B0530&accepted-page=-1&showParameters=true&renderMode=REPORT&htmlProportionalWidth=false"
        
        cdf = read_pdf(url, multiple_tables=True, pages=[1])[1]
        return cdf
    except Exception as e:
        if hasattr(e, 'message'):
            raise e.message
        else:
            raise e
def preprocess_data(cdf, long_date):
    try:
        raw = cdf.copy()    
        raw = raw.drop([0,2,3,4,5]).reset_index(drop=True)
        raw.iloc[4, 0] = "DADRA AND NAGAR HAVELI"
        raw.iloc[4, 1:11] = np.array(raw.iloc[5, 1:11])
        raw = raw.drop([0,5,6])
        raw.reset_index(inplace=True, drop=True)
        raw.iloc[8, 0] = "MADHYA PRADESH"
        raw.iloc[8, 1:11] = np.array(raw.iloc[9, 1:11])
        raw = raw.drop([0,1,9,10])
        raw.reset_index(inplace=True, drop=True)
        a = raw.iloc[:, 2].str.split(expand=True).reset_index(drop=True)
        #dtype setting
        df = raw.iloc[:, :2].reset_index(drop=True)
        df = pd.concat([df,a], axis=1)
        df = pd.concat([df,(raw.iloc[:, 3:].reset_index(drop=True))], axis=1)
        #formarting
        cols = ["state","thermal","hydro","wind","solar","others","total",\
                "net_schedule","drawal","ui","availability","requirement",\
                "shortage", "consumption"]
        df.columns = cols
        df = df.replace("-", np.nan)
        df = df.iloc[:-1, :]
        df.set_index("state", inplace=True)
        df = df.astype("float64")
        df.reset_index(inplace=True)
        cols.insert(0, "date")
        cols.insert(2, "region")
        df["date"] = str(long_date.date())
        region = "WR"
        df["region"] = region
        for c in ["state", "date", "region"] :
            df[c] = df[c].astype(str)    
        df = df[cols]
        return df
    except Exception as e:
        if hasattr(e, 'message'):
            raise e.message
        else:
            raise e

def insert_data(df):
    try:
        result = apis.store_forecast_api(df)
        return result
    except Exception as e:
        if hasattr(e, 'message'):
            raise e.message
        else:
            raise e 

def send_notification(to, subject, body):
    data = dict()
    data['to'] = to
    data['subject'] = subject
    data['body'] = body
    data['channel_type'] = 'email'
    jsdata = json.dumps(data)
    respo = requests.post(url = "https://apis.dummy.com/api/send-notification",
            headers = {'Content-type': 'application/json', 'Accept': 'text/plain'}, data= jsdata)
    return respo

def main():
    try:
        logger.info('========================================================================')
        sdt, tdt = "2019-12-16", "2019-12-17"
        #crndate = datetime.now() - timedelta(days=1)
        #sdt = tdt = crndate
        for long_date in pd.date_range(pd.Timestamp(sdt), pd.Timestamp(tdt), freq='D'):
            logger.info("we are going for >> {a}".format(a=long_date.date()))
            logger.info("getting the data")
            cdf = get_data(long_date)
            logger.info("preprocessing the data")
            df = preprocess_data(cdf, long_date)
            logger.info('into the insert_data function')
            result = insert_data(df)
            logger.info(result)
        logger.info('========================================================================')
    except:
        filename, line_no, line_strip, exc_obj = get_exception()
        to = ["sagar.paithankar@dummy.com"]
        subject = "Error : real time iex data scrapping failure"
        body = "Exception File : {a} \n \
        Exception Line No : {b} \n \
        Exception Line Syntax : {c} \n \
        Exception Reason : {d}".format(a=filename,b=line_no,c=line_strip,d=exc_obj)
        email_alert.send_notification(to, subject, body) 
        logger.info(body)
        logger.info('========================================================================')

if __name__ == '__main__':
    main()