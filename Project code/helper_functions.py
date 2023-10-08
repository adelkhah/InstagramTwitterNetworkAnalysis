import re
import networkx as nx
import argparse
import collections


def sort_and_small_dict(d, n):
    sorted_dict = collections.OrderedDict(sorted(d.items(), key=lambda x: -x[1]))
    firstnpairs = list(sorted_dict.items())[:n]
    return firstnpairs


def centrality_to_str_arr(centrality):
    str_arr = []
    for item in centrality:
        str_arr.append(item[0] + ' | ' + str(round(item[1], 2)))
    return str_arr




def create_undirected_graph_from_txt(input_txt_file):
    nodes = set()
    edges = []
    G = nx.Graph()

    with open(input_txt_file, 'r', encoding='utf-8') as f:
        for line in f:
            eachl = line[:-1]
            accounts = eachl.split(" ")
            account_1 = accounts[0]
            account_2 = accounts[1]

            nodes.add(account_1)
            nodes.add(account_2)
            edges.append([account_1, account_2])

    for account in nodes:
        G.add_node(account)

    for accounts in edges:
        G.add_edge(accounts[0], accounts[1])

    return G


def add_cluster_to_json(input_dict, cluster_dict):
    nodes = input_dict['nodes']
    links = input_dict['links']

    for item in nodes:
        item['group'] = cluster_dict[item['name']]

    out_dict = {'nodes': nodes, 'links': links}

    return out_dict
