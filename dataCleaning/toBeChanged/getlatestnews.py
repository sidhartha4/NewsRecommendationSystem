#!/usr/bin/python
from random import randint
from bs4 import BeautifulSoup
#from selenium import webdriver
import sqlite3, requests, zlib, json, time, gzip
#from subprocess import Popen, STDOUT
#from selenium.webdriver.firefox.firefox_binary import FirefoxBinary
from datetime import timedelta, date
import pickle
import unicodedata
import numpy
import psycopg2

conn = psycopg2.connect(database="newspaper", user="postgres", password="25erase79", host="127.0.0.1", port="5432")
print "Opened database successfully"

myUrlSet = numpy.load('urlThis6.npy')
myUrlSet = numpy.array(myUrlSet)
cur = conn.cursor()

#query =  "INSERT INTO guardianpublisharticles (url, newstype, headinglines,author, publishtime,photo ,newspapername) VALUES (%s, %s, %s, %s,%s,%s,%s);"
#data = ("c", "a", "a","a","a","https://static.guim.co.uk/sys-images/Guardian/Pix/pictures/2015/1/1/1420138679072/4b442864-77be-40c9-acb8-835956f9c739-220x132.jpeg","theguardian")

#cur.execute(query, data)
#conn.commit()

i = 0
j = 0
numberPublished = 0
notPublished = 0

with gzip.open('allGuardianArticlesData_2015to2016.txt.gz','r') as fin:  
		for line in fin:
			try:
				line = json.loads(line)
				dateToday = line['date']
				Infodata = line['Infodata']['response']['results']
				if dateToday != "2016-06-15":
					print(dateToday)
					continue
				for r in Infodata:
					print(dateToday)
					flag = 0
					publishedwebUrl = ""
					abstract = ""
					trailtext = ""
					author = ""
					topics = ""
					productionOffice = ""
					body = ""
					toneType = ""
					tagList = ""
					headline = ""
					imageurl = ""
					numberOfWords = 0
					flag1 = 0
					flag2 = 0
					flag3 = 0
					for rahead in r['tags']:
						try:
							if rahead['type'] == "contributor" and 'webTitle' in rahead:
								if author == "":
									flag1 = 1
									author = rahead['webTitle']
								else:
									author = author+"&"+rahead['webTitle']
									
							if rahead['type'] == "keyword" and 'webTitle' in rahead:
								if tagList == "":
									flag2 = 1
									tagList = rahead['webTitle']
								else:
									tagList = tagList+"&"+rahead['webTitle']
							
							if rahead['type'] == "tone" and 'webTitle' in rahead:
								if toneType == "":
									flag3 = 1
									toneType = rahead['webTitle']
								else:
									toneType = toneType+"&"+rahead['webTitle']
						except:
							continue
					if flag1 == 0 or flag2 == 0 or flag3 == 0:
						flag = 1
						
					if 'blocks' in r:
						l1 = r['blocks']
						if 'main' in l1:
							l2 = l1['main']
							if 'elements' in l2:
								l3 = l2['elements']
								for l33 in l3:
									if 'assets' in l33:
										l4 = l33['assets']
										l6 = 0
										for l5 in l4:
											if 'file' in l5:
												l6 = 1
												imageurl = l5['file']
												#print(imageurl)
												break
								
					if 'webUrl' in r :
						publishedwebUrl = r['webUrl']
					else:
						flag = 1
					if 'sectionId' in r:
						topics = r['sectionId']
					else:
						flag = 1
					if 'webTitle' in r:
						headline = r['webTitle']
					else:
						flag = 1
					if 'fields' in r :
						if 'standfirst' in r['fields']:
							abstract = r['fields']['standfirst']
						else:
							flag = 1
						if 'productionOffice' in r['fields']:
							productionOffice = r['fields']['productionOffice']
						else:
							flag = 1
						if 'body' in r['fields']:
							body = r['fields']['body']
						else:
							flag = 1
						if 'wordcount' in r['fields']:
							numberOfWords = r['fields']['wordcount']
						else:
							flag = 1
						if 'trailText' in r['fields']:
							trailtext = r['fields']['trailText']
						else:
							flag = 1
					else:
						flag = 1
					
					if flag == 1:
						j = j +1
					else:
						print(publishedwebUrl)
						
						abstract = unicodedata.normalize('NFKD', abstract).encode('ascii','ignore')
						trailtext = unicodedata.normalize('NFKD', headline).encode('ascii','ignore')
						author = unicodedata.normalize('NFKD', author).encode('ascii','ignore')
						topics = unicodedata.normalize('NFKD', topics).encode('ascii','ignore')
						publishedwebUrl = unicodedata.normalize('NFKD',publishedwebUrl).encode('ascii','ignore')
						if isinstance(dateToday,unicode):
							dateToday = unicodedata.normalize('NFKD',dateToday).encode('ascii','ignore')
						print(publishedwebUrl)
						
						for iaa in range(len(myUrlSet)):
							#print(myUrlSet[iaa])
							if str(publishedwebUrl) in str(myUrlSet[iaa][0]) or str(myUrlSet[iaa][0]) in str(publishedwebUrl):
								
								print(1)
								query =  "INSERT INTO guardianpublisharticles1 (url, newstype, headinglines,author, publishtime,photo ,newspapername) VALUES (%s, %s, %s, %s,%s,%s,%s);"
								data = (publishedwebUrl, topics, trailtext,author,dateToday,imageurl,"theguardian")

								cur.execute(query, data)
								conn.commit()
								break

						
						i = i+1
				
			except:
				print("imhere")
				continue





print "Records created successfully";
conn.close()


'''
for item in items:
    city = item[0]
    price = item[1]
    info = item[2]

'''