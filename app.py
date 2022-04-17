# -*- coding: utf-8 -*-
"""
Created on 17.04.2022

@author: Manish Yadav
"""

import streamlit as st
import spacy
from annotated_text import annotated_text
from spacy.lang.en.stop_words import STOP_WORDS
from string import punctuation
from heapq import nlargest
import plotly.express as px
import plotly.graph_objects as go
import matplotlib.pyplot as plt


def SummmaryWriter(text, model):
    nlp = spacy.load(model)
    
    ### Data cleaning
    doc = nlp(text)
    tokens = [token.text for token in doc]
    
    punctuation1 = punctuation + '\n'

    ### creating word frequency counter -> how mny times a
    ### (non stop and non punctuation) word is appearing
    word_freq={}
    stop_words = list(STOP_WORDS)
    
    for word in doc:
        if word.text.lower() not in stop_words:
            if word.text.lower() not in punctuation1:
                if word.text not in word_freq.keys():
                    word_freq[word.text] = 1
                else:
                    word_freq[word.text] += 1
    
    ### norrmalizing using max frequency
    max_freq = max(word_freq.values())
    
    for word in word_freq.keys():
        word_freq[word] = word_freq[word]/max_freq
    
    ### sentence tokenization
    sent_tokens = [sent for sent in doc.sents]
    
    ### giving score to individual words in each sentence.
    sent_score = {}
    
    for sent in sent_tokens:
        for word in sent:
            if word.text.lower() in word_freq.keys():
                if sent not in sent_score.keys():
                    sent_score[sent] = word_freq[word.text.lower()]
                else:
                    sent_score[sent] += word_freq[word.text.lower()]
    
    ### grab sentences with max. score : first 30%
    ### those sentences will become the summary of article    
    TopSentsNum = round(len(sent_score)*0.3)
        
    ### summarize
    summary = nlargest(TopSentsNum, iterable=sent_score, key=sent_score.get)
    final_summary = [word.text for word in summary]
    final_summary = " ".join(final_summary)
    
    text_len = len(text)
    summary_len = len(final_summary)
    
    return final_summary, text_len, summary_len
    

#### app description
st.write("""      
# Text summarization app

### This app summarizes any large english text.
#### You can select one of the provided models from the left sidebar.
       
 """     )




selected_model = st.sidebar.selectbox("Select a spacy model", options=["en_core_web_sm", "en_core_web_md"])

### input text
text_input = st.text_area("Type a text to anonymize")

### or upoad file
uploaded_file = st.file_uploader("or Upload a file", type=["doc", "docx", "pdf", "txt"])
if uploaded_file is not None:
    text_input = uploaded_file.getvalue()
    text_input = text_input.decode("utf-8")

summarize = st.checkbox("Summarize")

if summarize:
    st.markdown("**Summarized text**")
    st.markdown("---")
    final_summary, text_len, summary_len = SummmaryWriter(text_input, selected_model)
    annotated_text(*final_summary)
    st.markdown("---")
    st.markdown("---")
    ### bar-plot
    texts = ['Original text', 'Summary']
    plot_data = [text_len, summary_len]
        
    from matplotlib.pyplot import figure

    fig = plt.figure(figsize=(4, 2))
    plt.bar(texts, plot_data)
    plt.ylabel('Word count', fontsize=15)
    plt.xticks(fontsize=15)
    
    st.pyplot(fig)
    
    
    
    
    
    