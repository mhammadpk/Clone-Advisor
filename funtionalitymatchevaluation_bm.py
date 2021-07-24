from rouge import Rouge
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import torch
import math
import numpy as np
from statistics import mean

def calculateFunctionalMetrics(gtFuncationalId, topKFuncationalId):
    rank = 1.0
    mrr = 0.0
    top1 = 0.0
    top3 = 0.0
    top5 = 0.0
    top10 = 0.0
    for j in range(10):
        if gtFuncationalId.strip() == topKFuncationalId[j].strip():
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
    return top1, top3, top5, top10, mrr
    
def getFunctionalGroup(cloneList, total_function_snippets):
    functionIds = []
    snippets=[x[1] for x in total_function_snippets]
    indexF=-1
    functions=[x[0] for x in total_function_snippets]
    for i in range(len(cloneList)):
        for j in range(len(snippets)):
            if snippets[j]==cloneList[i]:
                indexF=j
                break
        if indexF==-1:
            print(i)
        else:
            functionIds.append(functions[indexF])

    return functionIds

def readData():
    text_file = open("ExpData/generatedClones_bm.txt", 'r')
    data = text_file.read()
    listOfSentences = data.split("\n")
    indexes = []
    for i in range(len(listOfSentences)):
        if listOfSentences[i] == "":
            indexes.append(i)

    predictedClones = [e for i, e in enumerate(listOfSentences) if
                       i not in indexes] 

    text_file = open("Data/benchmarkmethods.txt", 'r')
    data = text_file.read()
    listOfSentences = data.split("\n")
    orignalClones = [e for i, e in enumerate(listOfSentences) if
                     i not in indexes]  

    text_file = open("Data/functionalityIds_bm.txt", 'r')
    data = text_file.read()
    listOfSentences = data.split("\n")
    functionalityIdBm = [e for i, e in enumerate(listOfSentences) if
                     i not in indexes]


    text_file = open("Data/inputSequence_bm.txt", 'r')
    data = text_file.read()
    listOfSentences = data.split("\n")
    inputSequences = [e for i, e in enumerate(listOfSentences) if
                      i not in indexes]  

    return predictedClones, orignalClones, inputSequences, functionalityIdBm

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

def get_col(arr, col):
    return map(lambda x: x[col], arr)

def functionalEvaluation():
    cloneCorpus = readFile("Data/clonecorpus.txt")
    cloneCode = list(set(cloneCorpus))
    functionalityIds =  readFile("Data/functionalityIds.txt")#np.load("functionalityIds.npy")
    total_function_snippets = [(s, t) for s, t in zip(functionalityIds, cloneCorpus)]
    cloneOutput, orignalOutput, inputsequences,functionalityIdBm= readData()
    mrrList = []
    top1List = []
    top3List = []
    top5List = []
    top10List = []
    foldername = "Results/"
    it=0
    for m in range(len(functionalityIdBm)):#cloneOutput)):
        gtFuncationalId = functionalityIdBm[m]  # getFunctionalGroup([orignalOutput[m]], total_function_snippets)
      # if gtFuncationalId in ['10','17','18','21','22','25','32','33','34','37','39','40','43','5','9']:#['5']:#"['10', '22', '25', '26']:
              # ['10', '22', '25', '26', '5', '9']:
          # ['10', '14', '17', '21', '22', '25', '26', '28', '36', '38','39','5', '7', '9']:
        ###get ground truth functional Id

        topKPredicted = getTopKCloneResultsDocSim(cloneCode, cloneOutput[it], 10)
        topKFuncationalId = getFunctionalGroup(list(get_col(topKPredicted, 1)), total_function_snippets)
        cloneOutputList = []
        cloneOutputList.append(cloneOutput[it])
        top1, top3, top5, top10, mrr = calculateFunctionalMetrics(gtFuncationalId, topKFuncationalId)
        mrrList.append(mrr)
        top1List.append(top1)
        top3List.append(top3)
        top5List.append(top5)
        top10List.append(top10)
        it=it+1
        with open(foldername + "funationalitymatch_bm.txt", "a", encoding="utf-8") as outfile:
            outfile.write(str(mrr) +','+ str(top1) + ',' + str(top3) + ',' + str(top5) + ',' + str(top10))
            outfile.write('\n')
            outfile.close()
    print("MRR",str(mean(mrrList)))
    print("Top1", str(mean(top1List)))
    print("Top3", str(mean(top3List)))
    print("Top5", str(mean(top5List)))
    print("Top10", str(mean(top10List)))

functionalEvaluation()