"""
Word cloud module.
Author: Zhiyi Wang
Date: 04-11-2021
Version: 1.0
"""

import os
import wordcloud

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
    for file in os.listdir(input_path):
        with open(input_path + file, 'r') as f:
            tmp = f.read()
            # Remove the stop words
            tmp = remove_stop_words(tmp)
            # Create a word cloud instance and set the parameters
            word_cloud = wordcloud.WordCloud(width=1000, height=700, background_color='white', font_path='msyh.ttc',
                                             max_words=80)
            # Generate the word cloud
            word_cloud.generate(tmp)
            # print(tmp)
            ls = file.split('.')
            word_cloud.to_file(output_path + ls[0] + '.png')
        f.close()
        return None


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
                    "her", "mpelinkscriptplayersleaguebigeownerrandomkey", "Sent", "please",
                    "his", "imggif", "Original", "Regards",
                    "Message", "Forwarded", "one", "Thank", "Put", "put",
                    "cc", "will", "may", "Subject", "From", "To", "CT",
                    "IMAGE"]
    custom_words = set(custom_words)
    stop_words = stop_words.union(custom_words)
    word_tokens = word_tokenize(text)
    filtered_sentence = [wt for wt in word_tokens if not wt in stop_words]
    res = " ".join(filtered_sentence)
    return res
