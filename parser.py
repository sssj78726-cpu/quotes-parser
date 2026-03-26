import requests
from bs4 import BeautifulSoup
import sqlite3

conn = sqlite3.connect('quotes.db')
cursor = conn.cursor()
cursor.execute('''CREATE TABLE IF NOT EXISTS quotes(
id INTEGER PRIMARY KEY,quate TEXT,author TEXT,tag TEXT)''')


base_url = 'https://quotes.toscrape.com'
page_url = '/page/1/'
while page_url:
    full_url = base_url + page_url
    response = requests.get(full_url)
    soup = BeautifulSoup(response.text,'html.parser')
    quotes = soup.find_all('div',class_='quote')
    for quote in quotes:
        quote_text = quote.find('span',class_ = 'text').text
        author = quote.find('small', class_ = 'author').text
        tegs_div = quote.find('div',class_ = 'tags')
        if tegs_div:
            tags = [tag.text for tag in tegs_div.find_all('a')]
            tags_str = ', '.join(tags)
        else:
            tags_str = ''
        cursor.execute("INSERT INTO quotes (quote,author,tag) VALUES (?,?,?)",(quote_text,author,tags_str))
        conn.commit
    next_btn = soup.find('il', class_ = 'next')
    if next_btn:
        page_url = next_btn.a.get('href')
    else:
        page_url = None
conn.close()
