"""
Main module, implements the workflow
Author: Zhiyi Wang
Date: 04-11-2021
Version: 1.0
"""
#import DataPreprocess as data_preprocess
import WordCloud as word_cloud


def main():
    # data_preprocess.split_data('./data/emails.csv')
    # data_preprocess.convert_email()
    # data_preprocess.build_corpus()
    # word_cloud.create_word_cloud()
    # word_cloud.test()
    # word_cloud.more_test_cloudword(200)
    word_cloud.output_word_frequencies(200)



if __name__ == '__main__':
    main()
