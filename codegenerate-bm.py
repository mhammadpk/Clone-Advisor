import torch
import math
from statistics import mean

from transformers import (
    GPT2LMHeadModel,
    GPT2Tokenizer,
    GPT2Config
)


def getModelClone(sample, model, tokenizer, isPerplexity):
    # return sample, -1
    encoded_prompt = tokenizer.encode(sample, add_special_tokens=True, return_tensors="pt")
    encoded_prompt = encoded_prompt.to('cpu')

    output_sequences = model.generate(
        input_ids=encoded_prompt,
        max_length=550 + len(encoded_prompt[0]),
        temperature=1.0,
        top_p=0.95,  # args.p,
        repetition_penalty=1,  # args.repetition_penalty,
        do_sample=True,
        num_return_sequences=1,
        pad_token_id=tokenizer.pad_token_id,
        bos_token_id=tokenizer.bos_token_id,
        eos_token_id=tokenizer.eos_token_id,
    )

    # Remove the batch dimension when returning multiple sequences
    if len(output_sequences.shape) > 2:
        output_sequences.squeeze_()
    for generated_sequence_idx, generated_sequence in enumerate(output_sequences):
        generated_sequence = generated_sequence.tolist()

        # Decode text
        text = tokenizer.decode(generated_sequence, clean_up_tokenization_spaces=True)
        text2 = text.replace('<|endoftext|>', '')
        text2 = text2.replace('<|startoftext|>', '')
        # Remove all text after the stop token
        if (text2.find('<eoc>') == -1):
            return "", -1
        else:
            text3 = text2[: text2.find('<eoc>') if '<eoc>' else None]
            text4 = text3 + "<eoc>"
            clonesnippet = text4[text4.find('<soc>'):]
            if (isPerplexity == True):
                predictedperplexity = score(clonesnippet, model, tokenizer)
                return clonesnippet, predictedperplexity
            else:
                return clonesnippet, -1


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


def readFile(filename):
    text_file = open(filename, 'r', encoding="utf8")
    data = text_file.read()
    listOfSentences = data.split("\n")
    return listOfSentences

def readOrignalCode(filename):
    text_file = open(filename, 'r', encoding="utf8")
    data = text_file.read()
    listOfSentences = data.split(" <CODESPLIT> ")
    return listOfSentences

tokenizer = GPT2Tokenizer.from_pretrained('DeepClone')
config = GPT2Config.from_pretrained('DeepClone')
model = GPT2LMHeadModel.from_pretrained('DeepClone', config=config)
model.to('cpu')

sequences = readFile('Data/inputSequence_bm.txt')
functionalityId = readFile('Data/functionalityIds_bm.txt')
# filename = readFile('Data/fileName_projectcodenet_shuffle.txt')
groundTruth = readFile('Data/benchmarkmethods.txt')
# orignalCorpus = readOrignalCode("Data/orignalcode_projectcodenet_shuffle.txt")

foldername = "ExpData9/"
m=0
selectedIssues=[5,9]
#[11, 19, 22, 24, 35, 40, 45, 6, 7, 9]

for i in range(0, 2):#len(sequences)):#
    if functionalityId[i] in selectedIssues:
                        clonesnippet, perplexity = getModelClone(sequences[i], model, tokenizer, True)
                        gtperplexity=score(groundTruth[i], model, tokenizer)
                        with open(foldername + "gt_perplexity.txt", "a",
                                  encoding="utf-8") as outfile:
                            outfile.write(str(gtperplexity) + "\n")
                        if clonesnippet!="":
                            with open(foldername + "generatedClones_bm.txt", "a",
                                      encoding="utf-8") as outfile:
                                outfile.write(clonesnippet+"\n")
                            with open(foldername + "gc_perplexity.txt", "a",
                                          encoding="utf-8") as outfile:
                                outfile.write(str(perplexity) + "\n")
                        else:
                            with open(foldername + "generatedClones_bm.txt", "a",
                                      encoding="utf-8") as outfile:
                                outfile.write("\n")
                            with open(foldername + "gc_perplexity.txt", "a",
                                          encoding="utf-8") as outfile:
                                outfile.write("\n")
                            # with open(foldername + "functionalityId.txt", "a", encoding="utf-8") as outfile:
                            #     outfile.write(functionalityId[i]+"\n")
                            # # with open(foldername + "filename.txt", "a", encoding="utf-8") as outfile:
                            #     outfile.write(functionalityId[i]+".java" + "\n")
                            # # with open(foldername + "groundTruth.txt", "a", encoding="utf-8") as outfile:
                            #     outfile.write(groundTruth[i] + "\n")
                            # with open(foldername + "orignalCode.txt", "a", encoding="utf-8") as outfile:
                            #     outfile.write(orignalCorpus[i] + " <CODESPLIT> ")
                            # m = m + 1
            # if (i+1)%300==0:
            #              m=0

# listofgeneratedClones=readFile("Data/benchmarkmethods.txt")