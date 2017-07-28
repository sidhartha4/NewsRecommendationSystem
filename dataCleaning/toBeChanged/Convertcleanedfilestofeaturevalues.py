from sklearn import svm, metrics
from sklearn.cross_validation import StratifiedKFold
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.naive_bayes import BernoulliNB, MultinomialNB
import pickle, numpy, gzip, sqlite3, random
import unicodedata
import sys
reload(sys)
sys.setdefaultencoding("utf8")

publishedArticleNumber = 20419
NotpublishedArticleNumber = 119894
takepublishedfromevery = int(publishedArticleNumber/5000)
takenotpublishedfromevery = int(NotpublishedArticleNumber/5000)
requiredData = int(NotpublishedArticleNumber/20419)

def predictUsingNaiveBayes(X_train, X_test, Y_train):
    vectorizer = TfidfVectorizer(sublinear_tf=True, max_df=0.5, stop_words='english')
    X_train = vectorizer.fit_transform(X_train)
    X_test = vectorizer.transform(X_test)

    clf = MultinomialNB(alpha=.01)
    clf.fit(X_train, Y_train)
    predicted = clf.predict_proba(X_test)

    return predicted
	
def furtherCleaning():
	abstractList = None
	authorList = None
	topicsList = None
	productionOfficeList = None
	bodyList = None
	toneTypeList = None
	tagList = None
	numberOfWordsList = None
	outputList = None
	
	with open('CleanedData/trailtext.txt') as f:
		abstractList = f.read().splitlines()
		abstractList = numpy.array(abstractList)
	with open('CleanedData/author.txt') as f:
		authorList = f.read().splitlines()
		authorList = numpy.array(authorList)
	with open('CleanedData/topics.txt') as f:
		topicsList = f.read().splitlines()
		topicsList = numpy.array(topicsList)
	with open('CleanedData/productionOffice.txt') as f:
		productionOfficeList = f.read().splitlines()
		productionOfficeList = numpy.array(productionOfficeList)
	#with open('CleanedData/body.txt') as f:
	#	bodyList = f.read().splitlines()
	#	bodyList = numpy.array(bodyList)
	with open('CleanedData/toneType.txt') as f:
		toneTypeList = f.read().splitlines()
		toneTypeList = numpy.array(toneTypeList)
	with open('CleanedData/tagList.txt') as f:
		tagList = f.read().splitlines()
		tagList = numpy.array(tagList)
	with open('CleanedData/numberOfWords.txt') as f:
		numberOfWordsList = f.read().splitlines()
		numberOfWordsList = numpy.array(numberOfWordsList)
	with open('CleanedData/output.txt') as f:
		outputList = f.read().splitlines()
		
	
	fpauthor0 = open('CleanedData/0author.txt', 'w')
	fpauthor1 = open('CleanedData/1author.txt', 'w')
	fptopics0 = open('CleanedData/0topics.txt', 'w')
	fptopics1 = open('CleanedData/1topics.txt', 'w')
	fpProductionOffice0 = open('CleanedData/0productionOffice.txt', 'w')
	fpProductionOffice1 = open('CleanedData/1productionOffice.txt', 'w')
	fpbody0 = open('CleanedData/0body.txt', 'w')
	fpbody1 = open('CleanedData/1body.txt', 'w')
	fptone0 = open('CleanedData/0toneType.txt', 'w')
	fptone1 = open('CleanedData/1toneType.txt', 'w')
	fptagList0 = open('CleanedData/0tagList.txt', 'w')
	fptagList1 = open('CleanedData/1tagList.txt', 'w')
	fpnumberOfWords0 = open('CleanedData/0numberOfWords.txt', 'w')
	fpnumberOfWords1 = open('CleanedData/1numberOfWords.txt', 'w')
	fptrailtext0 = open('CleanedData/0trailtext.txt', 'w')
	fptrailtext1 = open('CleanedData/1trailtext.txt', 'w')
	
	i = 0
	j = 1
	for out in outputList:
		if out == "1":
			
			trailtext = abstractList[i]
			fptrailtext1.write(trailtext+"\n")
			author = authorList[i]
			fpauthor1.write(author+"\n")
			topics = topicsList[i]
			fptopics1.write(topics+"\n")
			productionOffice = productionOfficeList[i]
			fpProductionOffice1.write(productionOffice+"\n")
			#body = unicodedata.normalize('NFKD', bodyList[i]).encode('ascii','ignore')
			#fpbody1.write(body+"\n")
			toneType = toneTypeList[i]
			fptone1.write(toneType+"\n")
			tag =tagList[i]
			fptagList1.write(tag+"\n")
			numwor = numberOfWordsList[i]
			fpnumberOfWords1.write(numwor+"\n")
		else:
			if j%requiredData == 0:
				trailtext = abstractList[i]
				fptrailtext0.write(trailtext+"\n")
				author = authorList[i]
				fpauthor0.write(author+"\n")
				topics = topicsList[i]
				fptopics0.write(topics+"\n")
				productionOffice = productionOfficeList[i]
				fpProductionOffice0.write(productionOffice+"\n")
				#body = unicodedata.normalize('NFKD', bodyList[i]).encode('ascii','ignore')
				#fpbody0.write(body+"\n")
				toneType = toneTypeList[i]
				fptone0.write(toneType+"\n")
				tag = tagList[i]
				fptagList0.write(tag+"\n")
				numwor = numberOfWordsList[i]
				fpnumberOfWords0.write(numwor+"\n")
				
			j = j+1
		i = i+1
	
	fpauthor0.close()
	fpauthor1.close()
	fptopics0.close()
	fptopics1.close()
	fpProductionOffice0.close()
	fpProductionOffice1.close()
	fpbody0.close()
	fpbody1.close()
	fptone0.close()
	fptone1.close()
	fptagList0.close()
	fptagList1.close()
	fpnumberOfWords0.close()
	fpnumberOfWords1.close()
	fptrailtext0.close()
	fptrailtext1.close()
	
def main():
	abstractList0 = None
	abstractList1 = None
	authorList0 = None
	authorList1 = None
	topicsList0 = None
	topicsList1 = None
	productionOfficeList0 = None
	productionOfficeList1 = None
	toneTypeList0 = None
	toneTypeList1 = None
	tagList0 = None
	tagList1 = None
	numberOfWordsList0 = None
	numberOfWordsList1 = None
	
	
	with open('CleanedData/0trailtext.txt') as f:
		abstractList0 = f.read().splitlines()
		abstractList0 = numpy.array(abstractList0)
	with open('CleanedData/1trailtext.txt') as f:
		abstractList1 = f.read().splitlines()
		abstractList1 = numpy.array(abstractList1)
	with open('CleanedData/0author.txt') as f:
		authorList0 = f.read().splitlines()
		authorList0 = numpy.array(authorList0)
	with open('CleanedData/1author.txt') as f:
		authorList1 = f.read().splitlines()
		authorList1 = numpy.array(authorList1)
	with open('CleanedData/0topics.txt') as f:
		topicsList0 = f.read().splitlines()
		topicsList0 = numpy.array(topicsList0)
	with open('CleanedData/1topics.txt') as f:
		topicsList1 = f.read().splitlines()
		topicsList1 = numpy.array(topicsList1)
	with open('CleanedData/0productionOffice.txt') as f:
		productionOfficeList0 = f.read().splitlines()
		productionOfficeList0 = numpy.array(productionOfficeList0)
	with open('CleanedData/1productionOffice.txt') as f:
		productionOfficeList1 = f.read().splitlines()
		productionOfficeList1 = numpy.array(productionOfficeList1)
	#with open('CleanedData/body.txt') as f:
	#	bodyList = f.read().splitlines()
	#	bodyList = numpy.array(bodyList)
	with open('CleanedData/0toneType.txt') as f:
		toneTypeList0 = f.read().splitlines()
		toneTypeList0 = numpy.array(toneTypeList0)
	with open('CleanedData/1toneType.txt') as f:
		toneTypeList1 = f.read().splitlines()
		toneTypeList1 = numpy.array(toneTypeList1)
	with open('CleanedData/0tagList.txt') as f:
		tagList0 = f.read().splitlines()
		tagList0 = numpy.array(tagList0)
	with open('CleanedData/1tagList.txt') as f:
		tagList1 = f.read().splitlines()
		tagList1 = numpy.array(tagList1)
	with open('CleanedData/0numberOfWords.txt') as f:
		numberOfWordsList0 = f.read().splitlines()
		numberOfWordsList0 = numpy.array(numberOfWordsList0)
	with open('CleanedData/1numberOfWords.txt') as f:
		numberOfWordsList1 = f.read().splitlines()
		numberOfWordsList1 = numpy.array(numberOfWordsList1)
	
	print(tagList1[0].replace ("&", " "))
	
	X_naivetrain = []
	Y_naivetrain = []
	X_trainabstract = []
	Y_trainabstract = []
	X_testabstract = []
	Y_testabstract = []
	num = int(len(abstractList0)/5000)
	print num
	num2 = int(len(abstractList1)/5000)
	print num2
	j = 0
	for i in range(len(abstractList0)):
		if i%num == 0:
			X_naivetrain.append(abstractList0[i])
			#X_naivetrain.append(float(numberOfWordsList0[i]))
			Y_naivetrain.append(0)
		else:
			X_testabstract.append(abstractList0[i])
			#X_testabstract.append(float(numberOfWordsList0[i]))
			Y_testabstract.append(0)
	
	for i in range(len(abstractList1)):
		if i%num2 == 0:
			X_naivetrain.append(abstractList1[i])
			#X_naivetrain.append(float(numberOfWordsList1[i]))
			Y_naivetrain.append(1)
		else:
			X_testabstract.append(abstractList1[i])
			#X_testabstract.append(float(numberOfWordsList1[i]))
			Y_testabstract.append(1)
	
	X_naivetrain = numpy.array(X_naivetrain)
	Y_naivetrain = numpy.array(Y_naivetrain)
	X_testabstract = numpy.array(X_testabstract)
	Y_testabstract = numpy.array(Y_testabstract)
	abstract_feature_scores = predictUsingNaiveBayes(X_naivetrain, X_testabstract, Y_naivetrain)
	#abstract_feature_scores = X_testabstract
	abstract_feature_scores = numpy.array(abstract_feature_scores)
	#j = 0
	print(len(Y_testabstract))
	print(len(abstract_feature_scores))
	print(abstract_feature_scores[0])
	numpy.savetxt('featureValues/newoutput.txt',Y_testabstract)
	numpy.savetxt('featureValues/newwordcount_feature_scores.txt',abstract_feature_scores)
	#for i in range(len(Y_testabstract)):
	#	if abstract_feature_scores[i] == Y_testabstract[i]:
	#		j = j+1
	#print j
	#print(float(j)/len(Y_testabstract))
	#print(abstract_feature_scores)
	print(abstract_feature_scores[0])
	#print(abstract_feature_scores[0][1])
	
if __name__ == "__main__":
	#furtherCleaning()
    main()
	
	#abstract_feature_scores = numpy.loadtxt('featureValues/abstract_feature_scores.txt')
	#print(len(abstract_feature_scores))
	#print(abstract_feature_scores[0][0])
	#print(abstract_feature_scores[0][1])