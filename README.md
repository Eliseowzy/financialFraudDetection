# A Financial Fraud Detection Case based on Enron
> The work of few bad men or the dark shadow of American dream?[1,2]

![The logo of Enron Corporation](./externalResources/logo.png)

## Upcoming
```
Submission of group list:				19 Feb 2021
Submission of case study briefing:		26 Feb 2021
Project Presentation:				29-30 Apr 2021
Project Report submission:			8 May 2021
```
- Team Members: Wang Zhiyi, Zhang Siyu, Li Junjie
- Ref:
  - [1] https://en.wikipedia.org/wiki/Enron:_The_Smartest_Guys_in_the_Room
  - [2] https://www.bilibili.com/video/BV124411V7Zx?p=2&spm_id_from=pageDriver
- Data Source:
  - [Kaggle Enron Dataset](!https://www.kaggle.com/wcukierski/enron-email-dataset)

## Specification of data
> This is a specification of data.
> This specification is compiled by the steps and topics.
### Data Preprocess
- `split_1`: store the converted raw data by sengments, each segment composed by 10,000 emails, the last one is composed by 9,999.
- `email_split`: store the regular data extracted from `split_1`
### Word Cloud
- `word_cloud`: stores word cloud pictures in `.png`s, and `.txt` stores the top 200 frequent words.
- `word_hash`:
- `word_list`:
### Community Detection
- `email_communities`
  - `unweighted`: not in use yet.
  - `visualization`:
    - `gexf_files`: graph stored in `.gexf` format.
    - `gml_files`: graph stored in `.mgl` format.
    - `imgs`: community detection digrams.
- `email_corpus`: store the corpus of email content in `.txt` format.
    - each file stores 10,000 emails, the last one stores 9,999 emails.
- `email_corpus_by_person`: store the corpus by person, each file name represents an email send address.
- `email_graph`
  - `unweighted`: stores the *"From"* addresses and *"To"* addresses of each email.
  - `unweighted_clean_data`: stores the regular *"From"* addresses and *"To"* addresses of each email, recommanded to use.
  - **Note:** *"Cc"* addresses are treated as part of *"To"* addresses.
