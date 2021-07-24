import javalang
import os

def benchmarkPreprocessing():
    path = "C:/PhD/Datasets/Benchmark-CloneAdvisor/"

    for root, dirs, files in os.walk(path):
        # dirs.sort()
        for j in range(len(files)):
            name,extension=os.path.splitext(files[j])

            if(extension=='.java'):
                filePath = root + "/" + files[j]
                with open(filePath, encoding="utf8", errors='ignore') as f:
                    content = f.readlines()
                tokens = []
                tokens.append('<soc>')
                tokenize = list(javalang.tokenizer.tokenize(''.join(content)))
                for m in range(len(tokenize)):
                            tokentype = tokenize[m].__class__.__name__
                            if (tokentype == 'DecimalFloatingPoint' or tokentype == 'DecimalInteger' or tokentype == 'Integer' or
                                    tokentype == 'OctalInteger' or tokentype == 'BinaryInteger' or tokentype == 'HexInteger' or
                                    tokentype == 'FloatingPoint' or tokentype == 'HexFloatingPoint' or tokentype == 'Boolean' or tokentype == 'Literal'):
                                tokens.append("<num_val>")
                            elif (tokentype == 'Character' or tokentype == 'String'):
                                tokens.append("<str_val>")
                            else:
                                tokens.append(tokenize[m].value)
                tokens.append('<eoc>')
                with open('Data/benchmarkmethods.txt', 'a') as outfile:
                    outfile.write(" ".join(tokens)+'\n')
                with open('Data/functionalityIds_bm.txt', 'a') as outfile:
                    outfile.write(name+'\n')

def readFile(filename):
    text_file = open(filename, 'r', encoding="utf8")
    data = text_file.read()
    listOfSentences = data.split("\n")
    return listOfSentences

def generateInputSequences():
    sequences=readFile('Data/benchmarkmethods.txt')
    for i in range(len(sequences)):
        tokens=sequences[i].split(' ')
        inputTokens=tokens[0:20]
        with open('Data/inputSequence_bm.txt', 'a') as outfile:
            outfile.write(" ".join(inputTokens) + '\n')

benchmarkPreprocessing()
generateInputSequences()