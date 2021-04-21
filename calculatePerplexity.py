###############This file contains code for caluclating perplexity to determine naturalness
###############We determine naturalness for predicted clone methods, orignal clone methods, and recommended clone methods
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.metrics.pairwise import linear_kernel
import torch
import math
from statistics import mean
import numpy as np

from transformers import (
    GPT2LMHeadModel,
    GPT2Tokenizer,
    GPT2Config
)


def readFile(filename):
    text_file = open(filename, 'r', encoding="utf8")
    data = text_file.read()
    listOfSentences = data.split("\n")
    return listOfSentences


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


def chunks2(l, n):
    n = max(1, n)
    return (l[i:i + n] for i in range(0, len(l), n))


def score(sentence, model, tokenizer):
    # try:
    input_ids = torch.tensor(tokenizer.encode(sentence)).unsqueeze(0)  # Batch size 1 ,max_length=1024
    if len(input_ids[0]) > 1024:
        inputList = list(chunks2(input_ids[0], 1024))
        lossList = []
        for i in range(len(inputList)):
            input1 = inputList[i]
            input1 = input1.to('cpu')
            if len(input1) > 1:
                with torch.no_grad():
                    outputs1 = model(input1, labels=input1)
                loss1, logits1 = outputs1[:2]
                lossList.append(math.exp(loss1))
        ppl = mean(lossList)
        return round(ppl, 3)
    else:
        input_ids = input_ids.to('cpu')
        with torch.no_grad():
            outputs = model(input_ids, labels=input_ids)
        loss, logits = outputs[:2]
        return round(math.exp(loss), 3)


def get_col(arr, col):
    return map(lambda x: x[col], arr)


def calculatePerplexity(predicted, topk, orignal, model, tokenizer):
    orignalPerplexity = score(orignal, model, tokenizer)
    predictedPerplexity = score(predicted, model, tokenizer)
    topKPerplexity = []
    for i in range(len(topk)):
        topKPerplexity.append(score(topk[i][1], model, tokenizer))

    return topKPerplexity, orignalPerplexity, predictedPerplexity



def startProcess():
    tokenizer = GPT2Tokenizer.from_pretrained('DeepClone/')
    config = GPT2Config.from_pretrained('DeepClone/')
    model = GPT2LMHeadModel.from_pretrained('DeepClone/', config=config)
    model.eval()
    cloneCorpus = readFile("Data/clonecorpus.txt")
    cloneCode = list(set(cloneCorpus))
    cloneOutput, orignalOutput, inputsequences= readData()
    topKPerplexity = {}
    meanPerplexityPredicted=[]
    meanPerplexityOrignal=[]
    foldername = "Results/"
    for m in range(len(cloneOutput)):
        with open(foldername + "perplexityresults.txt", "a", encoding="utf-8") as outfile:
            topKPredicted = getTopKCloneResultsDocSim(cloneCode, cloneOutput[m], 10)
            topkPP,groundTruthPerplexity,DeepClonePerplexity = calculatePerplexity(cloneOutput[m], topKPredicted, orignalOutput[m], model,tokenizer)
            outfile.write(','.join(map(str, topkPP)))
            outfile.write(','+str(groundTruthPerplexity)+','+str(DeepClonePerplexity))
            outfile.write('\n')
            outfile.close()
            # Calculate Perplexity score of topK samples
            for i in range(len(topkPP)):
                pscore = []
                if topKPerplexity.get(i) == None:
                    pscore.append(topkPP[i])
                    topKPerplexity[i] = pscore
                else:
                    pscore = topKPerplexity[i]
                    pscore.append(topkPP[i])
                    topKPerplexity[i] = pscore

            meanPerplexityOrignal.append(groundTruthPerplexity)
            meanPerplexityPredicted.append(DeepClonePerplexity)


startProcess()