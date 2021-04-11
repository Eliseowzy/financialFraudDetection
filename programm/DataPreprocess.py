import pandas as pd
from pandas.core import indexing
import re

df_original = None
emails_count = 0
emails_count_in_file = 10000
file_count = 1


def load_data(file_name=None):
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
    # Split the data, each file contains 10000 emails
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


def extract_email_send_map():
    # for each file
    for cnt in range(1, 52):
        cur_df = pd.read_csv(
            './data/split_1/emails_{}.csv'.format(cnt))
        tmp_df = pd.DataFrame()
        print(cnt)
        for index, row in cur_df.iterrows():
            email = row['message']
            tmp = email.split()
            # ---- message_id ----
            email_dct = {'Message_ID': tmp[1]}
            # ---- time_stamp ----
            time_list = tmp[3:10]
            msg_date = ' '.join(time_list)
            email_dct['Time_Stamp'] = msg_date
            # ---- email address "From" ----
            email_dct["From"] = tmp[11]
            # ---- email address "To" ----
            receive_list = []
            cur = 12
            if tmp[cur] == "To:":  # There exists "To:" in message
                cur += 1
                while tmp[cur] != "Subject:":
                    receive_list.append(tmp[cur])
                    cur += 1
                # ----Then extract email subject----
                cur += 1
                subject_list = []
                while tmp[cur] != "Mime-Version:":
                    subject_list.append(tmp[cur])
                    cur += 1
                    subject = " ".join(subject_list)
                    email_dct["Subject"] = subject
            elif tmp[cur] != "To:":  # If not, use "X-To:" as receiver address
                cur = tmp.index("X-To:")
                cur += 1
                while tmp[cur] != "X-cc:":
                    receive_list.append(tmp[cur])
                    cur += 1
                # ---- Then extract email subject ----
                cur = 13
                subject_list = []
                while tmp[cur] != "Mime-Version:":
                    subject_list.append(tmp[cur])
                    cur += 1
                    subject = " ".join(subject_list)
                    email_dct["Subject"] = subject
            to_address = ' '.join(receive_list)
            email_dct["To"] = to_address
            # --------- email X-cc ----------
            cc_list = []
            cur = tmp.index("X-cc:") + 1
            while tmp[cur] != "X-bcc:":
                cc_list.append(tmp[cur])
                cur += 1
                cc_address = ', '.join(cc_list)
                email_dct["Cc"] = cc_address
            # --------- X-Folder ---------
            cur = tmp.index("X-Folder:") + 1
            email_dct["X_Folder"] = tmp[cur]
            cur = tmp.index("X-Origin:") + 1
            email_dct["X_Origin"] = tmp[cur]
            # --------- Text ---------
            cur = tmp.index("X-FileName:")
            text_index = cur + 3
            text_list = tmp[text_index:]
            text = ' '.join(text_list)
            email_dct['Text'] = text
            tmp_df = tmp_df.append(email_dct, ignore_index=True)
        tmp_df.to_csv('./data/email_split/emails_{}.csv'.format(cnt), index=False)
        # tmp_df.to_excel('./data/email_split/emails_{}.xlsx'.format(cnt), index=False)


def main():
    # load_data('./data/emails.csv')
    # load_data()
    # extract_message_id()
    extract_email_send_map()


if __name__ == '__main__':
    main()
