# this file is used for unit test
import pandas as pd
import re

input_path = r'./data/email_split/'

output_path = r'./data/email_corpus/'
file = 'emails_10_corpus.txt'

df = pd.read_csv(input_path + 'emails_10.csv', index_col='Message_ID')
ls = file.split('.')
with open(output_path + file, 'w') as f:
    tmp = str(list(df['Text']))
    tmp = tmp[1:-1]

    # remove email address in Text
    tmp = re.sub(r"[a-zA-Z0-9\.\-+_]+@[a-z0-9\.\-+_]+\.[a-z]+", '', tmp)
    tmp = re.sub(r"[a-zA-Z/]+@[a-zA-Z]", " ", tmp)
    # remove url in text
    tmp = re.sub(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', '', tmp)
    tmp = re.sub(r'[a-zA-Z]+://[^\s]*', '', tmp)

    # remove punctuation in text
    text_pattern = re.compile(u'[\s\w]').findall(tmp)
    tmp = "".join(text_pattern)
    tmp = re.sub(r"[\d+|_]", "", tmp)

    # remove redundant space in text
    tmp = re.sub(r"\s+", " ", tmp)
    f.write(tmp)
    # print(tmp)
    # print(type(tmp))
