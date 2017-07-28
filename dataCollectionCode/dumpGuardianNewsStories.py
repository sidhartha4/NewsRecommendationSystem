from random import randint
from bs4 import BeautifulSoup
from selenium import webdriver
import sqlite3, requests, zlib, json, time, gzip
from subprocess import Popen, STDOUT
from selenium.webdriver.firefox.firefox_binary import FirefoxBinary

conn = sqlite3.connect('guardianAllNewsDump.db')
c = conn.cursor()

def createTable():
     c.execute('''CREATE TABLE IF NOT EXISTS articles (url TEXT PRIMARY KEY NOT NULL, htmlDump BLOB)''')
     conn.commit()

def checkDataSanity():
     cursor = c.execute('SELECT * FROM articles')
     for row in cursor:
          content = zlib.decompress(row[1])
          print content
          break
     conn.close()
     
def main():
     xvfbCmdLine = "/usr/bin/Xvfb :10 -nolisten tcp -ac -cc 4 -screen 0 1200x800x24"
     xvfbProcess = Popen(xvfbCmdLine, shell=True, stderr=STDOUT)
     
     binary = FirefoxBinary(firefox_path="../Personalized-Reco/firefox/firefox")
     binary.add_command_line_options('--display=:10.0')
     driver = webdriver.Firefox(firefox_binary=binary)
     driver.set_window_size(1200, 800) # optional
            
     fp = gzip.open('datewiseGuardianArticles.txt.gz', 'rb')
     for line in fp:
          try:
               data = json.loads(line)
               result = data['Infodata']['response']['results']
               for j in result:                  
                    url = j['webUrl'].strip()
                    cursor = c.execute('SELECT COUNT(*) FROM articles WHERE url = (?)', (url,))
                    articleCount = 0
                    for row in cursor:
                         articleCount = int(row[0])
                         
                    if articleCount == 0:
                         driver.get(url)
                         content = driver.page_source
                         compressedHTMLDump = buffer(zlib.compress(content.encode('utf8')))
                         c.execute('INSERT INTO articles VALUES (?, ?)', (url, compressedHTMLDump))
                         conn.commit()
                         time.sleep(randint(120, 300))
          except Exception as e:
               print e
     fp.close()
     conn.close()
     driver.quit()
     xvfbProcess.kill()
     xvfbProcess.wait()

if __name__ == "__main__":
     createTable()
     main()
     #checkDataSanity()