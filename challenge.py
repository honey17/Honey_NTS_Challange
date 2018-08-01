#!/usr/bin/env python

import re
import boto3
import json
import ast
import urllib2
import pandas as pd
from bs4 import BeautifulSoup


def read_webpage(url):
    """crawling the data from a website

    input         : url
    variable used : text,page
    return type   :  str"""

    page = urllib2.urlopen(url)
    soup = BeautifulSoup(page, "html.parser")
    text = soup.find_all('p')
    con_str = " "
    for tt in text[3:]:
        con_str += tt.text
    text = re.sub(r'http\S+', '', con_str)
    return text


url = "https://blogs.wsj.com/cio/2018/06/18/software-microservices-open-up-new-business-models-for-companies/"
text = read_webpage(url)


def getting_key_phrases(text):
    """Finding keyPhrase
    
    input         : str
    variable used : data_comprehend,dict_data,df
    return type   : dataFrame""" 
    
    
    comprehend = boto3.client(service_name='comprehend', region_name='us-east-1')
    data_comprehend = json.dumps(comprehend.detect_key_phrases(
        Text=text[:4500], LanguageCode='en'), sort_keys=True, indent=4)
    dict_data = ast.literal_eval(data_comprehend)
    df = pd.DataFrame(dict_data['KeyPhrases'])
    df = df[['Text', 'Score']]
    df = df.drop_duplicates(subset='Text')
    df = df.sort_values('Score', ascending=False)
    return df


df_key_phrase = getting_key_phrases(text)
print df_key_phrase
