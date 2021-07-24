import random
def readFile(filename):
    text_file = open(filename, 'r', encoding="utf8")
    data = text_file.read()
    listOfSentences = data.split("\n")
    return listOfSentences

def generateSequences():
    cloneCorpus=readFile("Data/clonecorpus_projectcodenet.txt")
    for i in range(0,len(cloneCorpus)):
        code=cloneCorpus[i]
        tokens=code.split(' ')
        codeLen=int(len(tokens)/5)
        inputSequence=' '.join(tokens[0:codeLen])
        with open("Data/inputSequence_projectcodenet.txt", "a", encoding="utf-8", errors='ignore') as txt_file:
            txt_file.write(inputSequence + "\n")

def readOrignalCode(filename):
    text_file = open(filename, 'r', encoding="utf8")
    data = text_file.read()
    listOfSentences = data.split(" <CODESPLIT> ")
    return listOfSentences


def randomSequence():
    inputSequences=readFile("Data/inputSequence_projectcodenet_20tokens.txt")
    cloneCorpus= readFile("Data/clonecorpus_projectcodenet.txt")
    functionalityId = readFile("Data/functionalityId_projectcodenet.txt")
    filename= readFile("Data/fileName_projectcodenet.txt")
    orignalCorpus=readOrignalCode("Data/orignalcode_projectcodenet.txt")

    for i in range(0,len(inputSequences),300):
        shuffled_data = list(zip(inputSequences[i:i+300], cloneCorpus[i:i+300],functionalityId[i:i+300],filename[i:i+300],orignalCorpus[i:i+300]))
        shuffled_subsequences=shuffled_data
        random.shuffle(shuffled_subsequences)
        inputSequencesShuffle=[]
        cloneCorpusShuffle=[]
        functionalityIdShuffle=[]
        filenameShuffle=[]
        orignalCorpusShuffle=[]

        inputSequencesShuffle[:], cloneCorpusShuffle[:],functionalityIdShuffle[:],filenameShuffle[:],orignalCorpusShuffle[:]\
            = zip(*shuffled_subsequences)

        with open("Data/inputSequence_projectcodenet_20tokens_shuffle.txt", "a", encoding="utf-8", errors='ignore') as txt_file:
                txt_file.write("\n".join(inputSequencesShuffle))
                txt_file.write("\n")

        with open("Data/clonecorpus_projectcodenet_shuffle.txt", "a", encoding="utf-8", errors='ignore') as txt_file:
                txt_file.write("\n".join(cloneCorpusShuffle))
                txt_file.write("\n")

        with open("Data/functionalityId_projectcodenet_shuffle.txt", "a", encoding="utf-8", errors='ignore') as txt_file:
                txt_file.write("\n".join(functionalityIdShuffle))
                txt_file.write("\n")
        with open("Data/fileName_projectcodenet_shuffle.txt", "a", encoding="utf-8",
                      errors='ignore') as txt_file:
                txt_file.write("\n".join(filenameShuffle))
                txt_file.write("\n")
        with open("Data/orignalcode_projectcodenet_shuffle.txt", "a", encoding="utf-8",
                      errors='ignore') as txt_file:
                txt_file.write(" <CODESPLIT> ".join(orignalCorpusShuffle))
                txt_file.write("\n")

    print("get")

randomSequence()
# functionalityId=readFile("Data/functionalityId_projectcodenet.txt")
# uniqueIds=list(set(functionalityId))