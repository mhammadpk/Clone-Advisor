from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel

def readData():
	text_file = open("Data/predictedClones.txt", 'r')
	data = text_file.read()
	listOfSentences = data.split("\n")
	indexes = []
	for i in range(len(listOfSentences)):
		if listOfSentences[i] == "":
			indexes.append(i)

	predictedClones = [e for i, e in enumerate(listOfSentences) if
					   i not in indexes]

	text_file = open("Data/groundTruthClones.txt", 'r')
	data = text_file.read()
	listOfSentences = data.split("\n")
	orignalClones = [e for i, e in enumerate(listOfSentences) if
					 i not in indexes]

	text_file = open("Data/inputSequence.txt", 'r')
	data = text_file.read()
	listOfSentences = data.split("\n")
	inputSequences = [e for i, e in enumerate(listOfSentences) if
					  i not in indexes]


	return predictedClones, orignalClones, inputSequences

def get_col(arr, col):
	return map(lambda x: x[col], arr)

def getTopKCloneResultsDocSim(cloneLibrary, clone, k):
	vectorizer = TfidfVectorizer()
	vectors = vectorizer.fit_transform([clone] + cloneLibrary)
	# Calculate the word frequency, and calculate the cosine similarity of the search terms to the documents
	cosine_similarities = linear_kernel(vectors[0:1], vectors).flatten()
	document_scores = [item.item() for item in cosine_similarities[1:]]  # convert back to native Python dtypes
	total_score_snippets = [(score, title) for score, title in zip(document_scores, cloneLibrary)]
	topk = sorted(total_score_snippets, reverse=True, key=lambda x: x[0])[:k]
	return topk


def readFile(filename):
	text_file = open(filename, 'r',encoding="utf8")
	data = text_file.read()
	listOfSentences = data.split("\n")
	return listOfSentences

def calculateExactMatch():
	cloneCorpus = readFile("Data/clonecorpus.txt")
	cloneCode = list(set(cloneCorpus))
	cloneOutput, orignalOutput, inputsequences = readData()
	count=0    
	foldername = "Results/"
	for m in range(len(cloneOutput)):
		with open(foldername + "exactmatch.txt", "a", encoding="utf-8") as outfile:
			topKPredicted = getTopKCloneResultsDocSim(cloneCode, cloneOutput[m], 10)
			predictedSnippets = list(get_col(topKPredicted, 1))
			rank = 1.0
			mrr = 0.0
			top1 = 0.0
			top3 = 0.0
			top5 = 0.0
			top10 = 0.0

			for j in range(10):
				if orignalOutput[m].strip() == predictedSnippets[j].strip():
					mrr += 1.0 / rank
					if rank <= 1.0:
						top1 += 1.0
					if rank <= 3.0:
						top3 += 1.0
					if rank <= 5.0:
						top5 += 1.0
					if rank <= 10.0:
						top10 += 1.0
					break
				rank = rank + 1.0
			outfile.write(str(mrr)+','+str(top1)+','+str(top3)+','+str(top5)+','+str(top10))
			outfile.write('\n')
			outfile.close()
		count=count+1
	print("Total MRR", str(mrr / count))
	print("Total Top1 Accuracy", str(top1/count))
	print("Total Top3 Accuracy", str(top3/count))
	print("Total Top5 Accuracy", str(top5/count))
	print("Total Top10 Accuracy", str(top10/count))

calculateExactMatch()