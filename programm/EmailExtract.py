"""
Email message extract module.
Author: Zhiyi Wang
Date: 04-11-2021
Version: 1.0
"""

import pandas as pd


def extract_emails(input_email_data_frame):
    """ Extract emails from a single csv file, then store the data as csv format
    The format of input file is:
        file    message
        ---------------------
        file: id of each message
        message: content of each message, including from, to, cc, text, etc.
    The format of output file is:
        From	Message_ID	Text	Time_Stamp	To	X_Folder	X_Origin	Subject	Cc
        ---------------------
        Message_ID: the id of each email, identify each email
        Time_Stamp: the timestamp of each email, eg. "Mon, 14 May 2001 16:39:00 -0700 (PDT)"
        From: an email address where the message send
        To: target address (list)
        Cc: carbon copy address (list)
        Subject: the subject of each email
        Text: the content of each email
        X_Folder: map between person and "From"
        X_Origin: the original address of each (forwarded) email

    Args:
        input_email_data_frame:

    Returns:
        email_df

    """
    cur_df = input_email_data_frame
    email_df = pd.DataFrame()
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
        email_df = email_df.append(email_dct, ignore_index=True)
    return email_df
