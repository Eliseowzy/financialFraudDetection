"""
Word cloud module.
Author: Zhang Siyu
Date: 04-13-2021
Version: 2.0
"""

import os
import wordcloud
import re 
from collections import Counter
import heapq


from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# For the first time, these three lines should be executed to download Dependencies
# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')


def create_word_cloud():
    """
    Build and store a word cloud as .png file.
    You should set input_path and output_path firstly.
    
    Returns:
        None
        
    """
    input_path = r'./data/email_corpus/'
    output_path = r'./data/word_cloud/'
    
    # hash words in files and create hash files 
    # that collect the same words in a certain file
    hash_path_list = create_hash_file(input_path)
    
    # get word frenquencies
    words_fren = get_word_fren(hash_path_list)
    
    # create a word cloud with 100 words
    word_cloud = wordcloud.WordCloud(width=1000, height=700, background_color='white', font_path='msyh.ttc', max_words=100).fit_words(words_fren)
    word_cloud.to_file(output_path  + 'word_cloud_pic.png')
    
    return None

def more_test_cloudword(word_number):
    output_path = r'./data/word_cloud/'
    # the address of word hash files
    hashFileDir = r'./data/word_hash/'
    hash_path_list = []
    for i in range(1, 101):
        hash_path_list.append(hashFileDir + str(i) + '.txt')
    # get word frenquencies
    words_fren = get_word_fren(hash_path_list)
    
    # create a word cloud with 100 words
    word_cloud = wordcloud.WordCloud(width=1000, height=700, background_color='white', font_path='msyh.ttc', max_words=100).fit_words(words_fren)
    word_cloud.to_file(output_path  + 'word_cloud_pic' + '_for' + str(word_number) +'.png')
    return None

def output_word_frequencies(word_number):
    output_path = r'./data/word_cloud/'
    
    # the address of word hash files
    hashFileDir = r'./data/word_hash/'
    hash_path_list = []
    for i in range(1, 101):
        hash_path_list.append(hashFileDir + str(i) + '.txt')

    results = get_word_fren(hash_path_list)
        
    output_word_freq_file = open(output_path + 'word_frequencies' + '_for' + str(word_number) +'.txt', 'w')  
    for item in results.most_common(word_number):
        output_word_freq_file.write(' '.join(str(s) for s in item) + '\n')
    output_word_freq_file.close()       
    return None    
    
    
    
    
def create_hash_file(input_path):
    """
    Create 100 .txt files that hash the same words to the same .txt file 
    You should set tempDir firstly.
    Args:
        input_path: address of corpus file
    Returns:
        word_hash_path: all address of word hash files
        

    """
    
    # the address of word hash files
    tempDir = r'./data/word_hash/'
    
    # Import default stop words set
    stop_words = set(stopwords.words('english'))
    # Add some words you what to remove
    custom_words = ["pm", "a", "i", "p", "l", "t", "he", "she", "j", "w", "may", "can", "could", "you", "him",
                    "her", "sent", "please", "we", "us", "it", "am","im",
                    "said", "time", "get", "take", "make", "if",
                    "day", "year", "week", "today", "would",
                    "in", "date", "this", "like", "for", "also", 
                    "his", "imggif", "original", "regards", "use",
                    "message", "forwarded", "one", "two", "thank", "thanks", "put", "put",
                    "cc", "will", "may", "subject", "from", "to", "ct", "re", "th",
                    "image", "let", "well", "good", "want", "last",
                    "send", "see", "still", "think", "go", "attached", "back", "made", 
                    "following", "per", "es", "way", "first", "forward", "dont", "email",
                    "going", "need", "years", "much", "many", "group", "people", "since", 
                    "team", "list", "provide", "look", "click", "nron", 
                    ]
    custom_words = set(custom_words)
    stop_words = stop_words.union(custom_words)
    
    # transfer sentences to lists
    pattern = re.compile(r'\w+')
    
    # create .txt files for word hash
    temp_path_list = []
    for i in range(1,101):
        temp_path_list.append(open(tempDir + str(i) + '.txt', mode='w'))
    # wirte the same words to the same .txt file     
    for file in os.listdir(input_path):
        with open(input_path + file, 'r') as f:
            tmp = f.read()
            words_list = pattern.findall(tmp)
            for word in words_list:
                if len(word) >= 2 and len(word) <= 20 :
                    word = word.lower()
                    if not word in stop_words:
                        temp_path_list[hash(word)%100].write(word+'\n')
        f.close()
    for f in temp_path_list:
       f.close()
       
    # get address str   
    word_hash_path = []
    for i in range(1, 101):
        word_hash_path.append(tempDir + str(i) + '.txt')
    return word_hash_path

def get_word_fren(hash_path_list):
    """
    count number of each word
    Args:
        hash_path_list: all address of word hash files
    Returns:
        results: Frequncies of words
        

    """   
    results = Counter()
    # words_fren_100 = Counter()
    for file in hash_path_list:
        with open(file, 'r') as f:
            words_list = f.readlines()
            words_list = list(map(lambda x: x.strip('\n'),words_list))
            # word_count = Counter(words_list)
            results.update(words_list)
            # print(results)
    # words_fren_list = list(results.keys())
    # words_fren_list_100 = heapq.nlargest(100, results, key = lambda x:x[1])
    
    return results



    

def remove_stop_words(text):
    """
    remove stop words in a string
    Args:
        text: a piece of corpus

    Returns:
        res: the piece of corpus without stop words

    """
    # Import default stop words set
    stop_words = set(stopwords.words('english'))
    # Add some words you what to remove
    custom_words = ["PM", "A", "I", "P", "L", "T", "He", "She", "J", "W", "may", "can", "could", "you", "You", "him",
                    "her", "Sent", "please", "we", "us", "it",
                    "said", "time", "get", "take", "if", "day", "year",
                    "in", "date", "this", "like", ""
                    "his", "imggif", "original", "regards",
                    "message", "forwarded", "one", "thank", "put", "put",
                    "cc", "will", "may", "subject", "from", "to", "ct",
                    "image",
                    ]
    custom_words = set(custom_words)
    stop_words = stop_words.union(custom_words)
    word_tokens = word_tokenize(text)
    filtered_sentence = [wt for wt in word_tokens if not wt in stop_words]
    res = " ".join(filtered_sentence)
    return res