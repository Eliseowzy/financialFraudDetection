"""
Main module, implements the workflow
Author: Zhiyi Wang
Date: 04-20-2021
Version: 1.1
"""
import DataPreprocess as data_preprocess


import WordCloud as word_cloud

import CommunityDetection as community_detection


def main():
    data_preprocess.split_data('./data/emails.csv')
    data_preprocess.convert_email()
    data_preprocess.build_corpus()
    data_preprocess.build_email_corpus_by_selected_person()
    word_cloud.create_word_cloud()
    word_cloud.output_word_frequencies(200)
    community_detection.output_gexf_file(graph_type="unweighted", min_degree=100, max_degree=200)



if __name__ == '__main__':
    main()
