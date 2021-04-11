import pandas as pd
import os
import re
import EmailExtract as email_extract

""" This is data process module
"""
# Original data frame
df_original = None
# Total email number: 517401
emails_count = 0
# Number of emails in a file
emails_count_in_file = 10000
# File number: 51
file_count = 1


def split_data(file_name=None):
    global df_original
    global emails_count
    global emails_count_in_file
    global file_count
    df_original = pd.read_csv(file_name, error_bad_lines=False)
    print("The first 5 lines: ")
    print(df_original.head(5))
    print("The number of emails: ", end=None)
    emails_count = len(df_original)
    print(emails_count)

    # Split the original data, each file contains 10000 emails
    start = 0
    end = start + emails_count_in_file
    while end < emails_count:
        df_tmp = df_original[start:end]
        start += emails_count_in_file
        end = start + emails_count_in_file
        df_tmp.to_csv(
            './data/split_1/emails_{}.csv'.format(file_count), indexing=None)
        file_count += 1
    # The last file
    df_tmp = df_original[start:emails_count - start]
    df_tmp.to_csv(
        './data/split_1/emails_{}.csv'.format(file_count), indexing=None)
    return None


def convert_email():
    # for each file
    # Extract email and build email tables
    for cnt in range(1, 52):
        cur_df = pd.read_csv(
            './data/split_1/emails_{}.csv'.format(cnt))
        email_df = email_extract.extract_emails(cur_df)
        email_df.to_csv('./data/email_split/emails_{}.csv'.format(cnt), index=False)
        print("File {} succeed!".format(cnt))
        break
    return None


def build_corpus():
    input_path = r'./data/email_split/'
    output_path = r'./data/email_corpus/'
    for file in os.listdir(input_path):
        df = pd.read_csv(input_path + file, index_col='Message_ID')
        ls = file.split('.')
        file = ls[0] + '_corpus.txt'
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
        print(file)
    return None


def main():
    # split_data('./data/emails.csv')
    # split_data('./data/emails.csv')
    # extract_message_id()
    # convert_email()

    build_corpus()


if __name__ == '__main__':
    main()
