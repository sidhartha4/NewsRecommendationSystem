from bs4 import BeautifulSoup
from datetime import timedelta, date
import sqlite3, requests, zlib, json, time, gzip
print requests.__version__

API_Key = "9efd2a2f-a45e-4722-8179-900137fbde5d"    # Sidhartha

start_date = date(2016, 7, 19)
end_date = date(2016, 7, 20)

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)
        
def main():
    fp = gzip.open('../data/datewiseGuardianArticles.txt.gz', 'wb')
    for single_date in daterange(start_date, end_date):
        print single_date.strftime('%d')
        try:
            url = "http://content.guardianapis.com/search?format=json&from-date="+single_date.strftime("%Y-%m-%d")+"&to-date="+single_date.strftime("%Y-%m-%d")+"&page=1&page-size=100&api-key="+API_Key
            print url
            r = requests.get(url)
            time.sleep(2)

            newsObj = {\
                "date":single_date.strftime("%Y-%m-%d"),\
                "Infodata":r.json()\
            }
            fp.write("{0}\n".format(json.dumps(newsObj)))

            articleCount = newsObj['Infodata']['response']['total']
            numIterations = articleCount/100 + 2
            
            for i in range(2, numIterations):
                try:
                    url = "http://content.guardianapis.com/search?format=json&from-date="+single_date.strftime("%Y-%m-%d")+"&to-date="+single_date.strftime("%Y-%m-%d")+"&page="+str(i)+"&page-size=100&api-key="+API_Key
                    r = requests.get(url)
                    time.sleep(2)
                    
                    newsObj = {\
                        "date":single_date.strftime("%Y-%m-%d"),\
                        "Infodata":r.json()\
                    }
                    fp.write("{0}\n".format(json.dumps(newsObj)))
                except:
                    print "Failinner at {0}".format(i)
        except:
            print "Failouter "+single_date.strftime("%Y-%m-%d")
    fp.close()
            
if __name__ == "__main__":
     main()