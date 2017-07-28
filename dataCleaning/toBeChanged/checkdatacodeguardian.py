from sklearn import svm, metrics
from sklearn.cross_validation import StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
import pickle, numpy, gzip, sqlite3, random
import json
import sys
reload(sys)
sys.setdefaultencoding("utf8")
	
def main():	
	#'''
	with gzip.open('allGuardianArticlesData_2015to2016.txt.gz','r') as fin:  
		i = 0;	
		for line in fin:
			line = json.loads(line)
			#print(line['date'])
			Infodata = line['Infodata']['response']['results']
			for r in Infodata:
				print(r['webUrl'])
			i = i+1
			if(i>0):
				break
	#'''
	'''
	
	with gzip.open('nytimesPrintEditions.gz','r') as fin:  
		i = 0;	
		for line in fin:
			line = json.loads(line)
			print(line)
			
	'''
if __name__ == '__main__':
    main()