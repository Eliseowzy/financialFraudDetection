import os
import wordcloud
import nltk

from nltk.corpus import stopwords
from nltk.tokenize import word_tokenize


# nltk.download('stopwords')
# nltk.download('punkt')

def create_word_cloud():
    input_path = r'./data/email_corpus/'
    output_path = r'./data/word_cloud/'
    for file in os.listdir(input_path):
        with open(input_path + file, 'r') as f:
            # print(file)
            tmp = f.read()
            # print('123')
            # Create a word cloud instance and set the parameters
            tmp = remove_stop_words(tmp)
            word_cloud = wordcloud.WordCloud(width=1000, height=700, background_color='white', font_path='msyh.ttc',
                                             max_words=80)
            # Generate the word cloud
            word_cloud.generate(tmp)
            # print(tmp)
            ls = file.split('.')
            word_cloud.to_file(output_path + ls[0] + '.png')
        f.close()
        break


def remove_stop_words(text):
    # Import default stop words set
    stop_words = set(stopwords.words('english'))
    # Add some unmeaning words
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


create_word_cloud()
