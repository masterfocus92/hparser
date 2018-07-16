from urllib import request
from bs4 import BeautifulSoup
from datetime import datetime, date, timedelta
from collections import Counter
import sys
import pymorphy2
import string
import pandas as pd

morph = pymorphy2.MorphAnalyzer()
data_file = 'data.csv'
analized_data_file = 'result.csv'

def str_to_date(st):
	s = st[::-1]
	s = s[8::]
	s = s[::-1]
	if('сегодня' in st):
		d = datetime.date(datetime.now())
		return d

	if('вчера' in st):
		d = datetime.date(datetime.now() - timedelta(days=1))
		return d

	year = datetime.date(datetime.now()).year
	month = get_month_number(s)
	day = get_day_number(s)

	d = date(year, month, day)
	return d

def get_day_number(st):
	for day in range(31, 0, -1):
		if(str(day) in st):
			return day


def get_month_number(str):

	m_list = ['январ','феврал','март','апрел',
			'мая','июн','июл','август',
			'сентябр','октябр','ноябр','декабр']
	for month in m_list:
		if(month in str):
			return m_list.index(month) + 1



def get_pages_from_habr(query):
    docs = []
    for i in range(query):
    	docs.append(request.urlopen("https://habr.com/all/page" + str(i+1)))

    return docs

def get_noun_from_doc(received_html):
    soups = []
    dict_date_headers = {}
    dict_date_noun = {}
    for doc in received_html:
    	soups.append(BeautifulSoup(doc, "html.parser"))

    for soup in soups:
    	posts_headers = soup.findAll("article", class_="post post_preview")
    	for header in posts_headers:
			key = str_to_date(header.find("span", class_="post__time").string)
    		value = header.h2.a.string
    		if(dict_date_headers.get(key) == None):
    			dict_date_headers[key]=value
    		else:
    			dict_date_headers[key] = dict_date_headers[key] + " " + value

    extude = set(string.punctuation)

    for k in dict_date_headers:
    	# making lists of words from string
    	dict_date_headers[k] = ''.join(ch for ch in dict_date_headers[k] if ch not in extude)
    	dict_date_headers[k] = dict_date_headers[k].split(" ")

    	#This list will contain only NOUN words in normal form
    	noun_list = []
    	for word in dict_date_headers[k]:
    		p = morph.parse(word)[0]
    		if(p.tag.POS == "NOUN"):
    			noun_list.append(p.normal_form)
    	dict_date_noun[k] = noun_list
    pdseries = pd.Series(dict_date_noun)
    return pdseries

def devide_by_weeks(pd_series):
	dict={}
	for idex in range(pd_series.size):
		key = pd_series.index[idex].isocalendar()[1]
		if(dict.get(key) == None):
			dict[key] = pd_series[idex]
		else:
			dict[key].extend(pd_series[idex])
	pd_series_by_week = pd.Series(dict)
	return pd_series_by_week

def analize(pd_series):
	top_list = []
	index_list = []
	for list in pd_series:
		counter = Counter(list)
		most_common_top = counter.most_common(5)
		top_list.append(most_common_top)
	for i in range(pd_series.size):
		index_list.append(pd_series.index[i])
	sr = pd.Series(top_list, index_list)
	with open(analized_data_file, 'w', encoding='utf-8') as f:
		sr.to_csv(f, sep='\t')
	return sr

def output_to_csv(pd_series):
    with open(data_file, 'w', encoding='utf-8') as file:
        pd_series.to_csv(file, sep='\t')

def main(arg1):
    print('wait for parser will parse')
    html_data = get_pages_from_habr(arg1)
    dict_of_NOUN = get_noun_from_doc(html_data)
    dict_of_NOUN = devide_by_weeks(dict_of_NOUN)
    output_to_csv(dict_of_NOUN)
    analize(dict_of_NOUN)
    print('files were write. Press Enter to exit')
    input()

main(int(sys.argv[1]))
