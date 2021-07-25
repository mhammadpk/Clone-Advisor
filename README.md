# Clone-Advisor

This repository contains the code described in paper "Clone-Advisor: Recommending Code Tokens and Clone Methods with Deep Learning and Information Retrieval". The paper is underreview at PeerJ Computer Science Journal. 

Moreover, we are sharing DeepClone model which can be downloaded from <a href="https://www.dropbox.com/sh/r152xqs5rdsvvq1/AABsMH-iCbgpSjE3Vy9d3zVWa?dl=0">this link</a>. Further explanation about DeepClone model can be found in our paper on  <a href="https://link.springer.com/chapter/10.1007/978-3-030-64694-3_9">"DeepClone: Modeling Clones to Generate Code Predictions"</a>, which is published at ICSR 2020 conference. DeepClone model has been generated with <a href="https://github.com/huggingface/transformers/tree/master/examples/pytorch/language-modeling">GPT-2 language-modeling</a> script of HuggingFace Transformers Library. 

You can follow complete instructions on how to install and setup HuggingFace Transformer's Library from this <a href="https://github.com/huggingface/transformers">link</a>. Similarly, you can follow instructions on how to perform language modeling from Section <a href="https://github.com/huggingface/transformers/tree/master/examples/pytorch/language-modeling">"GPT-2/GPT and causal language modeling"</a>? There is a need to provide training, testing and validation files to build and evaluate language model.

Following are the descriptions of the code files used in our methodology:

<ol>

  <li> buildInputSequence.py contains code to build input sequences from projectcodenet corpus
  <li> calculatePerplexity.py contains code for caluclating perplexity to determine naturalness. We determine naturalness for predicted clone methods, orignal clone methods, and recommended clone methods.
   <li> codegenerate-bm.py contains code to generate predicted clone method by using HuggingFace transformer library.
 
</ol>







