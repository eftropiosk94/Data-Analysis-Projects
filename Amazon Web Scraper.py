from bs4 import BeautifulSoup
import requests
import smtplib
import time
import datetime

#Connect to the URL from where we will be scraping the data

URL = 'https://www.amazon.com/Funny-Data-Systems-Business-Analyst/dp/B07FNW9FGJ/ref=sr_1_3?dchild=1&keywords=data%2Banalyst%2Btshirt&qid=1626655184&sr=8-3&customId=B0752XJYNL&th=1'
headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/113.0", "Accept-Encoding":"gzip, deflate", "Accept":"text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT":"1","Connection":"close", "Upgrade-Insecure-Requests":"1"}

page = requests.get(URL, headers=headers)

soup1 = BeautifulSoup(page.content, "html.parser") #we just pull the DOCTYPE HTML, the page from the url

soup2 = BeautifulSoup(soup1.prettify(), 'html.parser') #we use the .prettify in soup1 to make it look better

title = soup2.find(id='productTitle').get_text()  #If I want to scrape the title of the profuct, I have to go to the html
# and find how the title is given there. The id productTitle is the code for the product Title

#price = soup2.find(id='priceblock_ourprice').get_text()
print(title)
#print(price)

#price = price.strip()[1:] # 1: means that I want it to take everything from the position 1 and on. I am dropping the $ which was in the position 0
title = title.strip()

import datetime

today = datetime.date.today()

import csv

header = ['Title', 'Date', 'Price']
data = [title, today] #+price

with open('AmazonWebScraperDataset.csv', 'w', newline='', encoding = 'UTF8') as f:
    writer = csv.writer(f) #creating the csv
    writer.writerow(header) #importing the header
    writer.writerow(data) #importing the data

import pandas as pd

df = pd.read_csv('/Users/eftropioskaragkiozis/AmazonWebScraperDataset.csv')

print(df)

#Now appending data to the csv
with open('AmazonWebScraperDataset.csv', 'a+', newline='', encoding = 'UTF8') as f:
    writer = csv.writer(f)
    writer.writerow(data) #importing the data

#Automating the procedure of daily checking for price changes
def check_price():
    URL = 'https://www.amazon.com/Funny-Data-Systems-Business-Analyst/dp/B07FNW9FGJ/ref=sr_1_3?dchild=1&keywords=data%2Banalyst%2Btshirt&qid=1626655184&sr=8-3&customId=B0752XJYNL&th=1'
    headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10.15; rv:109.0) Gecko/20100101 Firefox/113.0",
               "Accept-Encoding": "gzip, deflate",
               "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8", "DNT": "1",
               "Connection": "close", "Upgrade-Insecure-Requests": "1"}
    # Here one can find their User Agent in order to fill the headers: https://httpbin.org/get and connect the computer with the above url

    page = requests.get(URL, headers=headers)

    soup1 = BeautifulSoup(page.content, "html.parser")  # we just pull the DOCTYPE HTML from the url

    soup2 = BeautifulSoup(soup1.prettify(), 'html.parser')

    title = soup2.find(
        id='productTitle').get_text()
    price = soup2.find(id='priceblock_ourprice').get_text()

    price = price.strip()[1:]
    title = title.strip()

    import datetime

    today = datetime.date.today()

    import csv

    header  = ['Title', 'Date', 'Price']

    data = [title, today]

    with open('AmazonWebScraperDataset.csv', 'a+', newline = '', encoding = 'UTF8') as f:
        writer = csv.writer(f)
        writer.writerow(data)

while(True):
    check_price()
    time.sleep(86400) #check every 24 hours

import pandas as pd

df = pd.read_csv('/Users/eftropioskaragkiozis/AmazonWebScraperDataset.csv')

print(df)


def send_mail():
    server = smtplib.SMTP_SSL('smtp.gmail.com', 465)
    server.ehlo()
    #server.starttls()
    server.ehlo()
    server.login('eftropioskaragkiozis@gmail.com', 'XXXXXXXXX')

    subject = 'The object is below 15€'
    body = 'Time to buy'

    msg = f"Subject : {subject}\n\n{body}"

    server.sendmail('eftropioskaragkiozis@gmail.com', msg)
