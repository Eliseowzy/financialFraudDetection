import pandas as pd
import os
# import community as community_louvain
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


def detect_community_unweighted():
    """
    Detect communities from unweighted graph
    Returns:

    """
    input_path = r'./data/email_graph/unweighted_clean_data/'
    G = nx.Graph()
    for i in os.listdir(input_path):
        graph_df = pd.read_csv(input_path + i)
        for edge in graph_df.itertuples():
            G.add_edge(edge[1], edge[2])
        # G = nx.from_pandas_dataframe(graph_df)
        for edge in G.edges:
            if edge[0] == edge[1]:
                G.remove_edge(edge[0], edge[1])
        break
    print(G.edges)

    # G = nx.erdos_renyi_graph(100, 0.01)
    # partition = community_louvain.best_partition(G)


def main():
    # clean_graph_data()
    # build_email_graph()
    detect_community_unweighted()


if __name__ == '__main__':
    main()
