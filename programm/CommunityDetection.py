"""
Community Detection module.
Author: Zhiyi Wang
Date: 04-20-2021
Version: 1.1
"""

import pandas as pd
import os
import community as community_louvain
import matplotlib.cm as cm
import matplotlib.pyplot as plt
import networkx as nx


def build_email_graph():
    """
    Build the email send graph, nodes: people, edges: no weight, 1 or 0.
    Clean the data and store the data in csv file.
    Returns:
        None
    """
    input_path = r'./data/email_split/'
    output_path = r'./data/email_graph/unweighted/'
    # head_words = ['From', 'Message_ID', 'Text', 'Time_Stamp', 'To', 'X_Folder', 'X_Origin', 'Subject', 'Cc']

    for i in os.listdir(input_path):
        # Store the email graph
        email_graph = pd.DataFrame(columns=["From", "To"])
        print(i)
        # read email tables from memory
        emails = pd.read_csv(input_path + i)
        # read three columns; from to and cc
        emails = emails[['From', 'To', 'Cc']]
        # For each email
        for email in emails.itertuples():

            from_address = str(email[1])
            to_addresses = str(email[2]).split()
            cc_addresses = email[3]
            # If there some Cc address
            if not pd.isna(cc_addresses):
                # Extract Cc addresses as a list
                cc_addresses = str(email[3]).split()
                # Add the Cc address into To address.
                to_addresses.extend(cc_addresses)
            # Build the data email graph frame
            for to_address in to_addresses:
                # Filter out irregular addresses
                if "@" not in to_address or "<" in to_address or ">" in to_address or "/" in to_address:
                    continue
                to_address = to_address.strip(",")
                # Append regular data records
                email_graph = email_graph.append({"From": from_address, "To": to_address}, ignore_index=True)
        # Load the email graph as csv
        email_graph.to_csv(output_path + i, index=False)
        print("{} success".format(i))
    return None


def clean_graph_data():
    input_path = r'./data/email_graph/unweighted/'
    output_path = r'./data/email_graph/unweighted_clean_data/'

    for i in os.listdir(input_path):
        print(i)
        emails = pd.read_csv(input_path + i)
        email_graph = pd.DataFrame(columns=["From", "To"])
        for email in emails.itertuples():
            from_address = email[1]
            to_address = email[2]
            while ',' in to_address:
                to_address = to_address.replace(',', '')
            while '\"' in to_address:
                to_address = to_address.replace('\"', '')
            from_address = from_address.lower()
            to_address = to_address.lower()
            new_email = {"From": from_address, "To": to_address}
            email_graph = email_graph.append(new_email, ignore_index=True)
        email_graph.to_csv(output_path + i, index=False)
    return None


def filter_graph_nodes(min_degree, max_degree):
    input_path = r'./data/email_graph/unweighted_clean_data/'
    G = nx.Graph()
    for i in os.listdir(input_path):
        print(i)
        graph_df = pd.read_csv(input_path + i)
        for edge in graph_df.itertuples():
            if edge[1] != edge[2]:
                start = str(edge[1])
                end = str(edge[2])
                if '.' in start:
                    index_1 = start.index('@')
                    start = start[0:index_1]
                if '.' in end:
                    index_2 = end.index('@')
                    end = end[0:index_2]
                G.add_edge(start, end)

    nodes_removed = []
    for node in G.nodes:
        if G.degree(node) < min_degree:
            nodes_removed.append(node)
        if G.degree(node) > max_degree:
            nodes_removed.append(node)
    G.remove_nodes_from(nodes_removed)
    nodes_zero_degree = []
    for node in G.nodes:
        if G.degree(node) == 0:
            nodes_zero_degree.append(node)
    G.remove_nodes_from(nodes_zero_degree)
    return G


def detect_community_unweighted(min_degree=120, max_degree=500):
    """
    Detect communities from unweighted graph
    Returns:

    """
    G = filter_graph_nodes(min_degree, max_degree)
    # compute the best partition
    partition = community_louvain.best_partition(G)
    draw_communities(G, partition)
    return None


def output_gexf_file(graph_type, min_degree, max_degree):
    G = filter_graph_nodes(min_degree=min_degree, max_degree=max_degree)
    nx.write_gexf(G, r'.\data\email_communities\{}\visualization\gexf_files\{}_min_degree_{}_max_degree_{}.gexf'.format(
        graph_type, graph_type, min_degree, max_degree))
    return None


def output_gml_file(graph_type, min_degree, max_degree):
    G = filter_graph_nodes(min_degree=min_degree, max_degree=max_degree)
    nx.write_gml(G, r'.\data\email_communities\{}\visualization\gml_files\{}_min_degree_{}_max_degree{}.gml'.format(
        graph_type, graph_type, min_degree, max_degree))
    return None


def draw_communities(G, partition):
    """
    Draw a graph with community detection result.
    Args:
        G: a graph
        partition: the result of community detection

    Returns:

    """
    # draw the graph
    pos = nx.spring_layout(G)
    # color the nodes according to their partition
    cmap = cm.get_cmap('viridis', max(partition.values()) + 1)
    nx.draw_networkx_nodes(G, pos, partition.keys(), node_size=40,
                           cmap=cmap, node_color=list(partition.values()))
    nx.draw_networkx_edges(G, pos, alpha=0.5)
    # nx.draw_networkx_labels(G, pos)
    plt.show()
    # print(G.edges)
    return None
