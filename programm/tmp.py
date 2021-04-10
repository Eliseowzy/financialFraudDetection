import pandas as pd

cur_df = pd.read_csv('emails_1.csv')

for index, row in cur_df.iterrows():
    if index == 188:
        email = row['message']
        tmp = email.split()
        print(tmp)
        # message_id
        email_dct = {'Message_ID': tmp[1]}
        # time_stamp
        time_list = tmp[3:10]
        msg_date = ' '.join(time_list)
        email_dct['Time_Stamp'] = msg_date
        # from_address = re.findall(
        #     r'([From\:\s][a-zA-Z0-9.]+@[a-pr-zA-PRZ0-9-]+\.[a-zA-Z0-9-.]+)', i)
        # to_address = re.findall(
        #     r'([To\:\s][a-zA-Z0-9.]+@[a-pr-zA-PRZ0-9-]+\.[a-zA-Z0-9-.]+)', i)
        # email_dct['From'] = from_address
        # email_dct['To'] = to_address
        # email address "From"
        email_dct["From"] = tmp[11]
        # email address "To"
        receive_list = []
        cur = 12
        if tmp[cur] == "To:":  # There is To: in message
            cur += 1
            while tmp[cur] != "Subject:":
                receive_list.append(tmp[cur])
                cur += 1
            # Then extract email subject
            cur += 1
            subject_list = []
            while tmp[cur] != "Mime-Version:":
                subject_list.append(tmp[cur])
                cur += 1
                subject = " ".join(subject_list)
                email_dct["Subject"] = subject
        elif tmp[cur] != "To:":  # If not, use X-To
            cur = tmp.index("X-To:")
            cur += 1
            while tmp[cur] != "X-cc:":
                receive_list.append(tmp[cur])
                cur += 1
            # Then extract email subject
            cur = 13
            subject_list = []
            while tmp[cur] != "Mime-Version:":
                subject_list.append(tmp[cur])
                cur += 1
                subject = " ".join(subject_list)
                email_dct["Subject"] = subject
        to_address = ' '.join(receive_list)
        email_dct["To"] = to_address

        # email X-cc
        cc_list = []
        cur = tmp.index("X-cc:") + 1
        while tmp[cur] != "X-bcc:":
            cc_list.append(tmp[cur])
            cur += 1
            cc_address = ', '.join(cc_list)
            email_dct["Cc"] = cc_address
        # X-from
        # x_from_list = []
        # cur = tmp.index('X-From:')+1
        # while tmp[cur] != "X-To:":
        #     x_from_list.append(tmp[cur])
        #     cur += 1
        #     x_from = ''.join(x_from_list)
        #     email_dct["X_From"] = x_from
        # X-To:
        # x_from_list = []
        # cur = tmp.index('X-To:')+1
        # while tmp[cur] != "X-cc:":
        #     x_from_list.append(tmp[cur])
        #     cur += 1
        #     x_from = ''.join(x_from_list)
        #     email_dct["X_From"] = x_from
        # X-Folder
        cur = tmp.index("X-Folder:") + 1
        email_dct["X_Folder"] = tmp[cur]
        cur = tmp.index("X-Origin:") + 1
        email_dct["X_Origin"] = tmp[cur]
        # Text
        cur = tmp.index("X-FileName:")
        text_index = cur + 3
        text_list = tmp[text_index:]
        text = ' '.join(text_list)
        email_dct['Text'] = text
        print(email_dct)
