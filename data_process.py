import os
import argparse
import numpy as np
import pandas as pd
import json 

def process_string(content):    
    # Processing strings
    with open(content, 'r') as f:
        speech = json.load(f)

    string = speech['results']['transcripts'][0]['transcript']


    # COUNT FILLERS ================================================================
    
    # Count pauses, unintelligible words, and repetitions

    data = speech['results']['items']
    start = []
    end = []
    words = []
    count_pause = 0
    count_unintelligible = 0
    count_repetitions = 0
    count_trailing = 0
    i = 0
    while i < len(data):
        words.append(data[i]['alternatives'][0]['content'])
        if data[i]['type'] == "pronunciation":
            start.append(float(data[i]['start_time']))
            end.append(float(data[i]['end_time']))
            if float(data[i]['alternatives'][0]['confidence']) < .50:
                count_unintelligible += 1
        i += 1
    i = 1
    while (i < len(start)):
        if (start[i] - end[i - 1] > 0.25):
            count_pause += 1
        if (words[i] == words[i - 1]):
            count_repetitions += 1
        i += 1
    x = [string, count_pause, count_unintelligible, count_trailing, count_repetitions]
    return x



