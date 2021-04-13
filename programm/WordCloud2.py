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
# import matplotlib.pyplot as plt

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize

# For the first time, these three lines should be executed to download Dependencies
# import nltk
# nltk.download('stopwords')
# nltk.download('punkt')


def create_word_cloud():
    input_path = r'./data/email_corpus/'
    output_path = r'./data/word_cloud/'
    
    # hash words in files and create hash files 
    # that collect the same words in a certain file
    hash_path_list = create_hash_file(input_path)
    
    # get word frenquencies
    words_fren = get_word_fren(hash_path_list)
    word_cloud = wordcloud.WordCloud(width=1000, height=700, background_color='white', font_path='msyh.ttc', max_words=100).fit_words(words_fren)
    word_cloud.to_file(output_path  + 'word_cloud_pic.png')
    
    # plt.imshow(wordcloud)
    # plt.axis("off")
    # plt.imshow()
    return None
    
def create_hash_file(input_path):
    # the result of word hash
    tempDir = r'./data/word_hash/'
    
    # transfer sentences to lists
    pattern = re.compile(r'\w+')
    
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
    
    temp_path_list = []
    for i in range(1,101):
        temp_path_list.append(open(tempDir + str(i) + '.txt', mode='w'))
        
    for file in os.listdir(input_path):
        with open(input_path + file, 'r') as f:
            tmp = f.read()
            # # Remove the stop words
            # tmp = remove_stop_words(tmp)
            words_list = pattern.findall(tmp)
            for word in words_list:
                if len(word) >= 2 and len(word) <= 20 :
                    word = word.lower()
                    if not word in stop_words:
                        temp_path_list[hash(word)%100].write(word+'\n')
        f.close()
    for f in temp_path_list:
       f.close()
       
    word_hash_path = []
    for i in range(1, 101):
        word_hash_path.append(tempDir + str(i) + '.txt')
    return word_hash_path

def get_word_fren(hash_path_list):
    results = Counter()
    # words_fren_100 = Counter()
    for file in hash_path_list:
        with open(file, 'r') as f:
            words_list = f.readlines()
            words_list = list(map(lambda x: x.strip('\n'),words_list))
            word_count = Counter(words_list)
            results.update(word_count)
            # print(results)
    # words_fren_list = list(results.keys())
    # words_fren_list_100 = heapq.nlargest(100, results, key = lambda x:x[1])
    
    return results

# def test():
#     tempDir = r'./data/word_hash/'
#     output_path = r'./data/word_cloud/'
#     temp_path_list = []
#     for i in range(1,101):
#         temp_path_list.append(tempDir + str(i) + '.txt')
#     words_fren_list_100 = get_word_fren(temp_path_list)
#     # print(words_fren_list_100)
#     word_cloud = wordcloud.WordCloud(width=1000, height=700, background_color='white', font_path='msyh.ttc', max_words=100).fit_words(words_fren_list_100)
#     word_cloud.to_file(output_path  + 'word_cloud_pic.png')
#     return None

    

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