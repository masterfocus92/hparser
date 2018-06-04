# hparser.
it parse headers of habr.com and find most common nouns. This script creates two csv-table - 'data.csv' consiste of 
nouns in normale form and date of post with this words, 'result.csv' consiste of number of week in year and top-3 most 
common noun in this week. 

## Requirements
This script uses Pymorphy2 morphAnalizer to analized russian text and finding noun. More about pymorphy2 here https://pymorphy2.readthedocs.io/en/latest
datas represent by pandas series http://pandas.pydata.org/pandas-docs/version/0.22/
For headers parsing it uses BeautyfullSoap 4.0 https://www.crummy.com/software/BeautifulSoup/bs4/doc/

## Installing
To install hparser just clone repository and setup needed requirements

```
git clone https://github.com/masterfocus92/hparser.git
```
in project folder use
```
pip install -r requirements.txt
```

## Launch
To launch script just launch it in console with integer arg <= 100, where arg is number of pages need to parse.
habr.com only keep 100 pages.

### Autor
*masterfocus92* - Dmitry Lomovtsev
