import pandas 
import numpy as np
import os

def break_on_time(df, time_jump, save_name=None):
    """
    Breaks a dataframe into multiple dataframes based on time jumps
    :param df: pandas dataframe
    :param time_jump: time in seconds to break on
    :return: list of dataframes
    """
    start_times = df['Start Time'].values
    print(start_times)
    sentences = df['Text'].values
    text = []
    currString = sentences[0] + " "
    currStartIndex = 0
    for i in range(1, len(start_times)):
        if start_times[i] - start_times[currStartIndex] > time_jump:
            currString += sentences[i] + " "
            text.append(currString)
            currString = ""
            currStartIndex = i+1
        else:
            currString += sentences[i] + " "
    if currStartIndex < len(start_times):
        text.append(currString)
    if save_name is not None:
        with open(f"Chunked_Transcripts/{save_name}", 'w') as f:
            for line in text:
                f.write(line + "\n")
    return text

df = pandas.read_csv('Transcripts/transcript_Alexander_the_Great.csv')
r = break_on_time(df, 30, save_name='Alexander_the_Great.txt')
print(r)
        
