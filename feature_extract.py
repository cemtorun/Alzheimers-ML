#==============================================================================
#   Lexicosyntatic, semantic and other Feature Extraction 
#==============================================================================

import os
import nltk
import data_process as dp
import argparse
import numpy as np
import pandas as pd
import math
from scipy import spatial
from nltk.corpus import brown
from collections import Counter
from nltk.stem.wordnet import WordNetLemmatizer 
lmtzr = WordNetLemmatizer()

# POS TAGS
#NN	noun, singular 'desk', #NNS	noun plural	'desks', #NNP	proper noun, singular	'Harrison', #NNPS	proper noun, plural	'Americans'
#PRP	personal pronoun	I, he, she, #PRP$	possessive pronoun	my, his, hers, 
#VB	verb, base form	take, #VBD	verb, past tense	took, #VBG	verb, gerund/present participle	taking
#VBN	verb, past participle	taken, #VBP	verb, sing. present, non-3d	take, #VBZ	verb, 3rd person sing. present	takes
#RB	adverb	very, silently,#RBR	adverb, comparative	better, #RBS	adverb, superlative	best
#CC	coordinating conjunction, #IN	preposition/subordinating conjunction
#TO	to	go 'to' the store, #RP	particle	give up, #MD	modal	could, will
#CD	cardinal digit, #LS	list marker	1), #FW	foreign word, #UH	interjection	errrrrrrrm
#DT	determiner, #PDT	predeterminer	'all the kids'
#EX	existential there (like: "there is" ... think of it like "there exists")
#JJ	adjective	'big', #JJR	adjective, comparative	'bigger', #JJS	adjective, superlative	'biggest'
#POS	possessive ending	parent's
#WDT	wh-determiner	which, #WP	wh-pronoun	who, what
#WP$	possessive wh-pronoun	whose, #WRB	wh-abverb	where, when

def similarity(content, POS_tag):          
    temp_info = nltk.pos_tag(nltk.word_tokenize(content))
    temp_fd = nltk.FreqDist(tag for (word, tag) in temp_info)
    tot_pos = sum([temp_fd[tag] for tag in POS_tag])  #sum(temp_fd.values())
    
    local_pos_vec = []
    for tag in POS_tag:
        if tag in list(temp_fd.keys()):
            local_pos_vec.append(temp_fd[tag]/tot_pos)
        else:
            local_pos_vec.append(0)
            
    return local_pos_vec         

def get_tag_info(input):    
    
    # ----------------- Initialize ---------------
    input_text = input[0]
    data = nltk.word_tokenize(input_text) # the string produced by process_string separated into a list of words
    data_tag_info = []
    feature_set = []
    ttr = {}
    
    features = {'prp_count': 0, 'VP_count': 1, 'NP_count': 2, 'prp_noun_ratio': 3, 'word_sentence_ratio': 4,
                                    'count_pauses': 5, 'count_unintelligible': 6, 'count_repetitions': 7,
                                    'ttr': 8, 'R': 9, 'ARI': 10, 'CLI': 11}
    
    feature_set = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    feature_set[5] = input[1]
    feature_set[6] = input[2]
    feature_set[7] = input[4]
        
    # --------------- Noun tag and Verb tag lists ---------------   

    noun_list = ['NN', 'NNS', 'NNP', 'NNPS']
    verb_list = ['VB', 'VBD', 'VBG', 'VBN', 'VBP']
    
    # ---------- Define production rules / VP, NP definition ----------
    grammar = r"""
    DTR: {<DT><DT>}
    NP: {<DT>?<JJ>*<NN.*>} 
    PP: {<IN><NP>} 
    VPG: {<VBG><NP | PP>}
    VP: {<V.*><NP | PP>}     
    CLAUSE: {<NP><VP>} 
    """  
    
    # ---------- Distribution feature ----------    
    text = brown.words(categories='news')
    tag_info = nltk.pos_tag(text)
    tag_fd = nltk.FreqDist(tag for (word, tag) in tag_info)
    del_key = []
    for key in tag_fd.keys():
        if not key.isalpha():
            del_key.append(key)
    while not (del_key == []):
        tag_fd.pop(del_key.pop(), None)

    POS_tag = ['NN', 'IN', 'DT', 'VBD', 'VBFG', 'VBG', 'PRP', 'JJ', 'NNP', 'RB', 'NNS', 'CC']        
    tot_pos = sum([tag_fd[tag] for tag in POS_tag])  #sum(tag_fd.values())
    
    global_pos_vec = []
    for tag in POS_tag:
        if tag in list(tag_fd.keys()):
            global_pos_vec.append(tag_fd[tag]/tot_pos)
        else:
            global_pos_vec.append(0)

    # ---------------------tagging information -------------------
    for i in range(len(data)):
        text = data  
        # ========= LEXICOSYNTACTIC FEATURES =========
        
        #  ------- POS tagging ------- 
        tag_info = np.array(nltk.pos_tag(text))
        tag_fd = nltk.FreqDist(tag for i, (word, tag) in enumerate(tag_info))
        freq_tag = tag_fd.most_common()
        data_tag_info.append(freq_tag)
        
        # ------- Lemmatize each word -------    
        #text_root = []
        text_root = [lmtzr.lemmatize(j) for indexj, j in enumerate(text)]
        for indexj, j in enumerate(text):
            if tag_info[indexj,1] in noun_list:
                text_root[indexj] = lmtzr.lemmatize(j) 
            elif tag_info[indexj,1] in verb_list:
                text_root[indexj] = lmtzr.lemmatize(j,'v')             
        
        # ------- Phrase type ------- 
        sentence = nltk.pos_tag(text)
        cp = nltk.RegexpParser(grammar)
        phrase_type = cp.parse(sentence)  
        
        # ------- Pronoun frequency -------
        prp_count = sum([pos[1] for pos in freq_tag if pos[0]=='PRP' or pos[0]=='PRP$'])
        feature_set[features['prp_count']] = prp_count
        
        # ------- Noun frequency -------
        noun_count = sum([pos[1] for pos in freq_tag if pos[0] in noun_list])
        
        # ------- Gerund frequency -------
        vg_count = sum([pos[1] for pos in freq_tag if pos[0]=='VBG'])
        
        # ------- Pronoun-to-Noun ratio -------
        if noun_count != 0:
            prp_noun_ratio = prp_count/noun_count
        else:
            prp_noun_ratio = prp_count
        feature_set[features['prp_noun_ratio']] = prp_noun_ratio
        
        # Noun phrase, Verb phrase, Verb gerund phrase frequency        
        NP_count = 0
        VP_count = 0
        VGP_count = 0
        for index_t, t in enumerate(phrase_type):
            if not isinstance(phrase_type[index_t],tuple):
                if phrase_type[index_t].label() == 'NP':
                    NP_count = NP_count + 1
                elif phrase_type[index_t].label() == 'VP': 
                    VP_count = VP_count + 1
                elif phrase_type[index_t].label() == 'VGP':
                    VGP_count = VGP_count + 1
        feature_set[features['NP_count']] = NP_count
        feature_set[features['VP_count']] = VP_count                  
        # ------- TTR type-to-token ratio ------- 
        numtokens = len(text)
        freq_token_type = Counter(text)  # or len(set(text)) # text_root
        v = len(freq_token_type)
        ttr = float(v)/numtokens 
        feature_set[features['ttr']] = ttr                  
        
        # ------- Honore's statistic ------- 
        freq_token_root = Counter(text_root)
        occur_once = 0
        for j in freq_token_root:
            if freq_token_root[j] == 1:
                occur_once = occur_once + 1
        v1 = occur_once
        R = 100 * math.log(numtokens / (1 - (v1/v)))
        feature_set[features['R']] = R
                
        # ------- Automated readability index ------- 
        num_char = len([c for c in input_text if c.isdigit() or c.isalpha()])
        num_words = len([word for word in input_text.split(' ') if not word=='' and not word=='.'])
        num_sentences = input_text.count('.') + input_text.count('?')
        ARI = 4.71*(num_char/num_words) + 0.5*(num_words/num_sentences) - 21.43
        feature_set[features['ARI']] = ARI
        
        # ------- Coleman–Liau index -------
        L = (num_char/num_words)*100
        S = (num_sentences/num_words)*100
        CLI = 0.0588*L - 0.296*S - 15.8 
        feature_set[features['CLI']] = CLI               
            
        # ------- Word-to-sentence_ratio -------
        word_sentence_ratio = num_words/num_sentences
        feature_set[features['word_sentence_ratio']] = word_sentence_ratio
 
    return feature_set  
