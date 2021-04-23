"""
Data pre-process module.
Author: Zhiyi Wang
Date: 04-23-2021
Version: 1.3
"""

import pandas as pd
import os
import re
import EmailExtract as email_extract
import datetime

# Global set
# Original data frame
df_original = None
# Total email number: 517401
emails_count = 0
# Number of emails in a file
emails_count_in_file = 10000
# File number: 51
file_count = 1


def split_data(file_name=None):
    """
    split the original data set
    Args:
        file_name: the path of original downloaded from data source
    Returns:
        None

    """
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
        # Extract the structured email data from an unstructured email text
        email_df = email_extract.extract_emails(cur_df)
        email_df.to_csv('./data/email_split/emails_{}.csv'.format(cnt), index=False)
        print("File {} succeed!".format(cnt))
        break
    return None


def clean_email_content(email_content):
    """
    Clean the content of an email
    Args:
        email_content: the string of the raw email content
    Returns:
        cleaned email string

    """
    tmp = str(email_content)
    # remove email address in Text
    tmp = re.sub(r"[a-zA-Z0-9.\-+_]+@[a-z0-9.\-+_]+\.[a-z]+", '', tmp)
    tmp = re.sub(r"[a-zA-Z/]+@[a-zA-Z]", " ", tmp)
    # remove url in text
    tmp = re.sub(r'https?://(?:[-\w.]|(?:%[\da-fA-F]{2}))+', '', tmp)
    tmp = re.sub(r'[a-zA-Z]+://[^\s]*', '', tmp)

    # remove punctuation in text
    text_pattern = re.compile(r'[\s\w]').findall(tmp)
    tmp = "".join(text_pattern)
    tmp = re.sub(r"[\d+|_]", "", tmp)

    # remove redundant space in text
    tmp = re.sub(r"\s+", " ", tmp)
    return tmp


def convert_time_stamp(time_stamp):
    """
    Convert the format of data stamp into the regular one.
    Args:
        time_stamp: The original time stamp
    Returns:
        the regular time_stamp
    """

    time_stamp = time_stamp[:-12]
    time_stamp = datetime.datetime.strptime(time_stamp, "%a, %d %b %Y %H:%M:%S")
    # time_stamp = datetime.datetime.strftime(time_stamp, "%a, %d %b %Y %H:%M:%S -0700 (PDT)")
    return time_stamp


def convert_address_to_filename(email_address):
    """
    convert the format of an email address: e.g. a.abc@abc.com into a_abc_abc_com
    Args:
        email_address: the addresses will be converted
    Returns:
        None

    """
    email_address = email_address.replace('.', '_')
    email_address = email_address.replace('@', '_')
    return email_address


def build_corpus():
    """
    Build the corpus for every 10,000 emails
    Returns:
        None
    """
    input_path = r'./data/email_split/'
    output_path = r'./data/email_corpus/'
    for file in os.listdir(input_path):
        df = pd.read_csv(input_path + file, index_col='Message_ID')
        ls = file.split('.')
        file = ls[0] + '_corpus.txt'
        with open(output_path + file, 'w') as f:
            tmp = str(list(df['Text']))
            tmp = clean_email_content(tmp)
            f.write(tmp)
            # print(tmp)
            # print(type(tmp))
        print(file)
    return None


def build_corpus_by_person():
    """
    Build corpus by person
    Returns:
        None
    """
    input_path = r'./data/email_split/'
    output_path = r'./data/email_corpus_by_person/'
    email_all = pd.DataFrame()
    for i in os.listdir(input_path):
        emails = pd.read_csv(input_path + i)
        email_all = email_all.append(emails)
    # print(email_all)
    name_set = set(email_all["From"])
    name_set = list(name_set)
    for name in name_set:
        if pd.isna(name) or '@' not in name or '>' in name or '\"' in name:
            continue
        print(name)
        cur_person_email = email_all[email_all["From"] == name]
        person_email = pd.DataFrame(columns=["Message_id", "From", "Time_stamp", "Text"])
        for email in cur_person_email.itertuples():
            text = str(email[3])
            time_stamp = email[4]
            if pd.isna(time_stamp):
                continue
            if not pd.isna(email[-2]):
                text = str(email[-2]) + text
            from_address = email[1]
            text = clean_email_content(text)
            time_stamp = str(convert_time_stamp(time_stamp))
            message_id = email[2]
            new_email = {"Message_id": message_id, "From": from_address, "Time_stamp": time_stamp, "Text": text}
            person_email = person_email.append(new_email, ignore_index=True)
        name = convert_address_to_filename(name)
        person_email.to_csv(output_path + name + '.csv', index=False)


def build_email_corpus_by_selected_person():
    """
    Build email corpus by selected persons
    Returns:
        None
    """
    # email book contains email address, first name, last name, status, etc.
    email_book = pd.read_excel(r'./data/email_book.xlsx', header=0, names=None)
    # probable emails' directory
    email_corpus_by_person_directory = './data/email_corpus_by_person/'
    # all probable emails set
    # email_file_list = [i for i in os.listdir()]
    email_file_list = [i for i in os.listdir(email_corpus_by_person_directory)]
    # for each person
    for _, person in email_book.iterrows():
        first_name = person[0]
        last_name = person[1]
        print("{}_{}".format(first_name, last_name))
        # store the person's email temporarily
        person_email_corpus = pd.DataFrame(
            columns=["FirstName", "LastName", "MessageId", "From", "Time_stamp", "Text", "Ordner", "Status"])
        # for each person's email
        for i in range(2, 6):
            person_email = person[i]
            # if this person has no email address, continue
            if pd.isna(person_email):
                continue
            # get the file name
            email_file = convert_address_to_filename(person_email) + ".csv"
            # if the file not in the probable email set, continue
            if email_file not in email_file_list:
                continue
            # read email as a dataframe
            email_file = pd.read_csv(email_corpus_by_person_directory + email_file)
            # for this person's emails
            for _, email in email_file.iterrows():
                # extract some useful information
                message_id = email[0]
                from_address = email[1]
                time_stamp = email[2]
                text = email[3]
                # build a new email dictionary
                new_email = {'FirstName': first_name, 'LastName': last_name, 'MessageId': message_id,
                             'From': from_address,
                             'Time_stamp': time_stamp, 'Text': text, 'Ordner': person[6], 'Status': person[7]}
                # append to the person's temporary email set
                person_email_corpus = person_email_corpus.append(new_email, ignore_index=True)

                # print(person_email_corpus)
                # person_email_corpus.append(new_email, ignore_index=True)
            # load the person's email
            person_email_corpus.to_csv(
                "./data/email_corpus_by_selected_person/{}".format(first_name + "_" + last_name + '.csv'), index=False)
    return None
