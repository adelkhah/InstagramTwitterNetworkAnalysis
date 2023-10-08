import networkx as nx
import relation_to_json as rel
import matplotlib.pyplot as plt
import numpy as np
import time
from igraph import *
import greedy_celf as gc
import json

def read_json_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data



def top_n_keys(d, n):
    sorted_items = sorted(d.items(), key=lambda x: x[1], reverse=True)
    top_n = [k for k, v in sorted_items[:n]]
    return top_n


def create_igraph(source, target, vertic):
    g = Graph(directed=True)
    g.add_vertices(vertic)
    g.add_edges(zip(source, target))

    return g


def convert_igraph_to_networkx(igraph_graph):
    edgelist = igraph_graph.get_edgelist()
    networkx_graph = nx.DiGraph(edgelist)
    return networkx_graph

def finding_influencer_betweeness(g,prop ,numberOfinfluencer, mc = 10):
    S, spread, timelapse, start_time = [], [], [], time.time()

    G = convert_igraph_to_networkx(g)
    between = dict(nx.betweenness_centrality(G))
    toppagerank = top_n_keys(between, numberOfinfluencer)
    for aa in toppagerank:
        S.append(aa)
        spread.append(gc.IC(g, S, prop, mc))
        timelapse.append(time.time() - start_time)

    return (S, spread, timelapse)


def finding_influencer_pagerank(g,prop ,numberOfinfluencer, mc = 10):
    S, spread, timelapse, start_time = [], [], [], time.time()

    G = convert_igraph_to_networkx(g)
    page_rank = dict(nx.pagerank(G, max_iter=1000))
    toppagerank = top_n_keys(page_rank, numberOfinfluencer)
    for aa in toppagerank:
        S.append(aa)
        spread.append(gc.IC(g, S, prop, mc))
        timelapse.append(time.time() - start_time)

    return (S, spread, timelapse)



def finding_influencer_cluster_pagerank(g,prop ,numberOfinfluencer, mc = 10):
    S, spread, timelapse, start_time = [], [], [], time.time()

    allcluster = {}
    clustersize = {}
    data = read_json_file('relations_louvain.json')
    for a in data['nodes']:
        if a['group'] not in allcluster:
            allcluster[a['group']] = []
            allcluster[a['group']].append(a['id'])
        else:
            allcluster[a['group']].append(a['id'])

    for a in allcluster:
        clustersize[a] = len(allcluster[a])

    G = convert_igraph_to_networkx(g)
    page_rank = dict(nx.pagerank(G, max_iter=1000))

    bigcluster = top_n_keys(clustersize, numberOfinfluencer)
    toppagerank = []
    for b in bigcluster:
        nod = allcluster[b]
        best = max(nod, key=lambda x: page_rank[x])
        toppagerank.append(best)


    for aa in toppagerank:
        S.append(aa)
        spread.append(gc.IC(g, S, prop, mc))
        timelapse.append(time.time() - start_time)

    return (S, spread, timelapse)


def finding_influencer_degree(g, prop,numberOfinfluencer, mc = 10):
    S, spread, timelapse, start_time = [], [], [], time.time()

    G = convert_igraph_to_networkx(g)
    deg_cen_points = dict(G.in_degree())
    topdegree = top_n_keys(deg_cen_points, numberOfinfluencer)
    for aa in topdegree:
        S.append(aa)
        spread.append(gc.IC(g, S, prop, mc))
        timelapse.append(time.time() - start_time)

    return (S, spread, timelapse)


def independent_cascade(g, S, p):
    # Simulate propagation process
    new_active, A = S[:], S[:]
    while new_active:

        # For each newly active node, find its neighbors that become activated
        new_ones = []
        for node in new_active:
            # Determine neighbors that become infected
            success = np.random.uniform(0, 1, len(g.neighbors(node, mode="out"))) < p
            new_ones += list(np.extract(success, g.neighbors(node, mode="out")))

        new_active = list(set(new_ones) - set(A))
        # Add newly activated nodes to the set of activated nodes
        A += new_active

    return A

def read_json_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data

def activate_to_json(A, data):
    print(len(A))
    for a in data['nodes']:
        if a['id'] in A:
            a['group'] = 4

    with open('02 visual\cascade.json', 'w') as outfile:
        json.dump(data, outfile)




if __name__ == '__main__':
    file_name = 'allrelationship.txt'
    json_file = '02 visual/relations.json'
    # rel.allrealation_toText_Twitter(file_name)
    rel.allrealation_toText_Instagram(file_name)


    nameid, edge = rel.relations_to_json(file_name,
                                         json_file)

    idname = dict()
    target = []
    source = []
    for u1, u2 in edge:
        u1id = nameid[u1]
        u2id = nameid[u2]
        source.append(u1id)
        target.append(u2id)

    for k, v in nameid.items():
        idname[v] = k

    ig = create_igraph(source, target, range(len(nameid)))


    degree_output = finding_influencer_degree(ig, 0.1, 2)
    print("degree output: " + str(degree_output[0]))
    pagerank_output = finding_influencer_pagerank(ig, 0.1, 2)
    print("pagerank output:   " + str(pagerank_output[0]))
    between_output = finding_influencer_betweeness(ig, 0.1, 2)
    print("betweeness output:   " + str(between_output[0]))



    # Plot settings
    plt.rcParams['figure.figsize'] = (9, 6)
    plt.rcParams['lines.linewidth'] = 4
    plt.rcParams['xtick.bottom'] = False
    plt.rcParams['ytick.left'] = False

    # Plot Computation Time
    plt.plot(range(1, len(degree_output[2]) + 1), degree_output[2], label="Degree", color="#FBB4AE")
    plt.plot(range(1, len(pagerank_output[2]) + 1), pagerank_output[2], label="PageRank", color="#B3CDE3")
    plt.plot(range(1, len(between_output[2]) + 1), between_output[2], label="betweeness", color="#f5abc5")

    plt.ylabel('Computation Time (Seconds)');
    plt.xlabel('Size of Seed Set')
    plt.title('Computation Time');
    plt.legend(loc=2);

    plt.show()

    # Plot Expected Spread by Seed Set Size
    plt.plot(range(1, len(degree_output[1]) + 1), degree_output[1], label="Degree", color="#FBB4AE")
    plt.plot(range(1, len(pagerank_output[1]) + 1), pagerank_output[1], label="PageRank", color="#B3CDE3")
    plt.plot(range(1, len(between_output[1]) + 1), between_output[1], label="betweeness", color="#f5abc5")

    plt.xlabel('Size of Seed Set');
    plt.ylabel('Expected Spread')
    plt.title('Expected Spread');
    plt.legend(loc=2);

    plt.show()

