from rouge import Rouge
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import torch
import math
import numpy as np
from statistics import mean


def calculateFunctionalMetrics(gtFuncationalId, topKFuncationalId):
    rank = 1.0
    top1 = 0.0
    top3 = 0.0
    top5 = 0.0
    top10 = 0.0
    for j in range(10):
        if gtFuncationalId.strip() == topKFuncationalId[j].strip():
            if rank <= 1.0:
                top1 += 1.0
            if rank <= 3.0:
                top3 += 1.0
            if rank <= 5.0:
                top5 += 1.0
            if rank <= 10.0:
                top10 += 1.0
        rank = rank + 1.0
    return top1/1.0, top3/3.0, top5/5.0, top10/10.0


def getFunctionalGroup(cloneList, total_function_snippets):
    functionIds = []
    snippets = [x[1] for x in total_function_snippets]
    indexF = -1
    functions = [x[0] for x in total_function_snippets]
    for i in range(len(cloneList)):
        for j in range(len(snippets)):
            if snippets[j] == cloneList[i]:
                indexF = j
                break
        if indexF == -1:
            print(i)
        else:
            functionIds.append(functions[indexF])

    return functionIds


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
    text_file = open(filename, 'r', encoding="utf8")
    data = text_file.read()
    listOfSentences = data.split("\n")
    return listOfSentences


def get_col(arr, col):
    return map(lambda x: x[col], arr)


def functionalEvaluation():
    cloneCorpus = readFile("Data/clonecorpus.txt")
    cloneCode = list(set(cloneCorpus))
    functionalityIds = readFile("Data/functionalityIds.txt")  # np.load("functionalityIds.npy")
    total_function_snippets = [(s, t) for s, t in zip(functionalityIds, cloneCorpus)]
    cloneOutput, orignalOutput, inputsequences = readData()
    top1List = []
    top3List = []
    top5List = []
    top10List = []
    foldername = "Results/"

    for m in range(len(cloneOutput)):
        ###get ground truth functional Id
        gtFuncationalId = getFunctionalGroup([orignalOutput[m]], total_function_snippets)
        topKPredicted = getTopKCloneResultsDocSim(cloneCode, cloneOutput[m], 10)
        topKFuncationalId = getFunctionalGroup(list(get_col(topKPredicted, 1)), total_function_snippets)
        cloneOutputList = []
        cloneOutputList.append(cloneOutput[m])
        top1, top3, top5, top10 = calculateFunctionalMetrics(gtFuncationalId[0], topKFuncationalId)
        top1List.append(top1)
        top3List.append(top3)
        top5List.append(top5)
        top10List.append(top10)
        with open(foldername + "precision.txt", "a", encoding="utf-8") as outfile:
            outfile.write(str(top1) + ',' + str(top3) + ',' + str(top5) + ',' + str(top10))
            outfile.write('\n')
            outfile.close()

    print("P1", str(mean(top1List)))
    print("P3", str(mean(top3List)))
    print("P5", str(mean(top5List)))
    print("P10", str(mean(top10List)))


functionalEvaluation()