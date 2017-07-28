import sqlite3
from random import randint
from bs4 import BeautifulSoup
from selenium import webdriver
import requests, zlib, json, time, gzip
from subprocess import Popen, STDOUT
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from datetime import timedelta, date

conn = sqlite3.connect('../data/guardianPrintNewsDump.db')
c = conn.cursor()


start_date = date(2016, 7, 18)
end_date = date(2016, 7, 20)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

def createTable():
     c.execute('''CREATE TABLE IF NOT EXISTS printNewspaper (url TEXT PRIMARY KEY NOT NULL, htmlDump BLOB)''')
     conn.commit()

def checkDataSanity():
    cursor = c.execute('SELECT * FROM printNewspaper')
    a = 0
    for row in cursor:
        print(row[0])
        content = zlib.decompress(row[1])
        soup = BeautifulSoup(content, 'html.parser')
        scholars=soup.find_all("a", { "data-link-name" : "article" ,"tabindex" : "-1"});

def main():
    xvfbCmdLine = "/usr/bin/Xvfb :11 -nolisten tcp -ac -cc 4 -screen 0 1200x800x24"
    xvfbProcess = Popen(xvfbCmdLine, shell=True, stderr=STDOUT)
     
    binary = FirefoxBinary(firefox_path="../Personalized-Reco/firefox/firefox")
    binary.add_command_line_options('--display=:11.0')
    driver = webdriver.Firefox(firefox_binary=binary)
    driver.set_window_size(1200, 800) # optional
     
    for single_date in daterange(start_date, end_date):
        try:
            if single_date.month == 1:
                url = "http://www.theguardian.com/theguardian/{0}/jan/{1}".format(single_date.strftime('%Y'), single_date.strftime('%d'))
            elif single_date.month == 2:
                 url = "http://www.theguardian.com/theguardian/{0}/feb/{1}".format(single_date.strftime('%Y'), single_date.strftime('%d'))
            elif single_date.month == 3:
                 url = "http://www.theguardian.com/theguardian/{0}/mar/{1}".format(single_date.strftime('%Y'), single_date.strftime('%d'))
            elif single_date.month == 4:
                 url = "http://www.theguardian.com/theguardian/{0}/apr/{1}".format(single_date.strftime('%Y'), single_date.strftime('%d'))
            elif single_date.month == 5:
                 url = "http://www.theguardian.com/theguardian/{0}/may/{1}".format(single_date.strftime('%Y'), single_date.strftime('%d'))
            elif single_date.month == 6:
                 url = "http://www.theguardian.com/theguardian/{0}/jun/{1}".format(single_date.strftime('%Y'), single_date.strftime('%d'))
            elif single_date.month == 7:
                 url = "http://www.theguardian.com/theguardian/{0}/jul/{1}".format(single_date.strftime('%Y'), single_date.strftime('%d'))
            elif single_date.month == 8:
                 url = "http://www.theguardian.com/theguardian/{0}/aug/{1}".format(single_date.strftime('%Y'), single_date.strftime('%d'))
            elif single_date.month == 9:
                 url = "http://www.theguardian.com/theguardian/{0}/sep/{1}".format(single_date.strftime('%Y'), single_date.strftime('%d'))
            elif single_date.month == 10:
                 url = "http://www.theguardian.com/theguardian/{0}/oct/{1}".format(single_date.strftime('%Y'), single_date.strftime('%d'))
            elif single_date.month == 11:
                 url = "http://www.theguardian.com/theguardian/{0}/nov/{1}".format(single_date.strftime('%Y'), single_date.strftime('%d'))
            elif single_date.month == 12:
                 url = "http://www.theguardian.com/theguardian/{0}/dec/{1}".format(single_date.strftime('%Y'), single_date.strftime('%d'))

            cursor = c.execute('SELECT COUNT(*) FROM printNewspaper WHERE url = (?)', (url,))
            articlecount = 0
            for row in cursor:
                articleCount = int(row[0])

            if articleCount == 0:
                driver.get(url)
                content = driver.page_source
                compressedHTMLDump = buffer(zlib.compress(content.encode('utf8')))
                c.execute('INSERT INTO printNewspaper VALUES (?, ?)', (url, compressedHTMLDump))
                time.sleep(randint(120, 300))

        except Exception as e:
               print e

    conn.close()
    driver.quit()
    xvfbProcess.kill()
    xvfbProcess.wait()
     
if __name__ == "__main__":
    #createTable()
    #main()
    checkDataSanity()