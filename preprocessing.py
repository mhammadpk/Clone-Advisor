import javalang
# import pandas as pd
import os
# from shutil import copyfile
# import filecmp
import numpy as np
# from os import listdir
# from os.path import isfile, join
def readFile(filename):
    text_file = open(filename, 'r', encoding="utf8")
    data = text_file.read()
    listOfSentences = data.split("\n")
    return listOfSentences

def buildSearchCorpus(path, selectedProblems):
    files = [val for sublist in [[os.path.join(i[0], j) for j in i[2]] for i in os.walk(path)] for
             val in
             sublist]
    for i in range(len(files)):
        try:
            tokens = []
            filename = files[i].split('\\')[2]
            foldername = files[i].split('\\')[1]
            if foldername in selectedProblems:
                with open(files[i], encoding="utf8", errors='ignore') as f:
                    content = f.readlines()
                orignalcode="\n".join(content)
                # content[0] = "socCLNE " + content[0]
                # content[len(content)-1] = content[len(content)-1]+" eocCLNE"

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

                with open("Data/clonecorpus_projectcodenet.txt", "a", encoding="utf-8", errors='ignore') as txt_file:
                    # txt_file.write()
                    txt_file.write("<soc> "+" ".join(tokens)+" <eoc>\n")
                    # txt_file.write("<eoc>\n")

                with open("Data/orignalcode_projectcodenet.txt", "a", encoding="utf-8", errors='ignore') as txt_file:
                    txt_file.write(orignalcode)
                    txt_file.write(" <CODESPLIT> ")
                with open("Data/functionalityId_projectcodenet.txt", "a", encoding="utf-8", errors='ignore') as txt_file:
                    txt_file.write(foldername+"\n")

                with open("Data/fileName_projectcodenet.txt", "a", encoding="utf-8", errors='ignore') as txt_file:
                    txt_file.write(filename+"\n")
        except Exception as e:
            print(e)
            with open("Data/clonecorpus_projectcodenet.txt", "a", encoding="utf-8", errors='ignore') as txt_file:
                txt_file.write("<EXCEPT>\n")

            with open("Data/functionalityId_projectcodenet.txt", "a", encoding="utf-8", errors='ignore') as txt_file:
                txt_file.write(foldername + "\n")

            with open("Data/fileName_projectcodenet.txt", "a", encoding="utf-8", errors='ignore') as txt_file:
                txt_file.write(filename + "\n")
            print(foldername+"/"+filename)
            pass

def buildExperimentalTokens(files,savepath):
    tokens = []
    testingSequence20=[]
    testingSequenceportion=[]
    for i in range(len(files)):
        try:
            with open(files[i], encoding="utf8", errors='ignore') as f:
                    content = f.readlines()
            # orignalcode="\n".join(content)
            tokenize = list(javalang.tokenizer.tokenize(''.join(content)))
            tokens.append("<soc>")
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
            tokens.append("<eoc>")

        except Exception as e:
            # print(e)
            print(files[i])
            pass
    with open(savepath, 'a',encoding="utf8") as outfile:
         outfile.write(" ".join(tokens) + '\n')



def buildExperimentalCorpus(path):
    training=[]
    testing=[]
    validation=[]
    trainingSet=[]
    testingSet=[]
    validationSet=[]
    N=300
    testingFunction=[]
    for root, dirs, files in os.walk(path):
        # for j in range(len(files)):
            # foldername=root.split(path + "\\")[1]
        if len(files)==300:
            np.random.shuffle(files)
            training = files[:int(N * 0.8)]
            trainingSet=trainingSet+[root+"\\"+x for x in training]
            validation = files[int(N * 0.8):int(N * 0.9)]
            validationSet = validationSet+[root +"\\"+ x for x in validation]
            testing = files[int(N * 0.9):]
            testingSet = testingSet+[root +"\\"+ x for x in testing]
            testingFunction.append(root.split("\\")[1])

            # name,extension=os.path.splitext(files[j])
    buildExperimentalTokens(trainingSet,"ExpData/training_pcn.txt")
    buildExperimentalTokens(validationSet, "ExpData/validation_pcn.txt")
    buildExperimentalTokens(testingSet, "ExpData/testing_pcn.txt")

    with open("ExpData/testing_pcn_func.txt", 'w',encoding="utf8") as outfile:
         outfile.write("\n".join(testingFunction))


    # for
    # files = [val for sublist in [[os.path.join(i[0], j) for j in i[2]] for i in os.walk(path)] for
    #          val in
    #          sublist]

    #
    #             with open("Data/clonecorpus_projectcodenet.txt", "a", encoding="utf-8", errors='ignore') as txt_file:
    #                 # txt_file.write()
    #                 txt_file.write("<soc> "+" ".join(tokens)+" <eoc>\n")
    #                 # txt_file.write("<eoc>\n")
    #
    #             with open("Data/orignalcode_projectcodenet.txt", "a", encoding="utf-8", errors='ignore') as txt_file:
    #                 txt_file.write(orignalcode)
    #                 txt_file.write(" <CODESPLIT> ")
    #             with open("Data/functionalityId_projectcodenet.txt", "a", encoding="utf-8", errors='ignore') as txt_file:
    #                 txt_file.write(foldername+"\n")
    #
    #             with open("Data/fileName_projectcodenet.txt", "a", encoding="utf-8", errors='ignore') as txt_file:
    #                 txt_file.write(filename+"\n")
    #     except Exception as e:
    #         print(e)
    #         with open("Data/clonecorpus_projectcodenet.txt", "a", encoding="utf-8", errors='ignore') as txt_file:
    #             txt_file.write("<EXCEPT>\n")
    #
    #         with open("Data/functionalityId_projectcodenet.txt", "a", encoding="utf-8", errors='ignore') as txt_file:
    #             txt_file.write(foldername + "\n")
    #
    #         with open("Data/fileName_projectcodenet.txt", "a", encoding="utf-8", errors='ignore') as txt_file:
    #             txt_file.write(filename + "\n")
    #         print(foldername+"/"+filename)
    #         pass

# selectedProblems=readFile("Data\genericProblems.txt")
# buildSearchCorpus("Project_CodeNet_Java250",selectedProblems)
buildExperimentalCorpus("Project_CodeNet_Java250")