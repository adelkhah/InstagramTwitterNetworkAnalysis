import community.community_louvain as community_louvain
import json
from helper_functions import *

def community_detection(input_txt_file, input_json_file, output_json_file):


    G = create_undirected_graph_from_txt(input_txt_file)
    # LOUVAIN METHOD
    partition_louvain = community_louvain.best_partition(G)
    size = float(len(set(partition_louvain.values())))
    pos = nx.spring_layout(G)
    count = 0.
    communities_louvain = []
    for com in set(partition_louvain.values()):
        count = count + 1.
        list_nodes = [nodes for nodes in partition_louvain.keys()
                      if partition_louvain[nodes] == com]
        communities_louvain.append(list_nodes)
        nx.draw_networkx_nodes(G, pos, list_nodes, node_size=20,
                               node_color=str(count / size))

    #get new jsons
    with open(input_json_file) as f:
        input_dict = json.load(f)

    json_with_groups_louvain = add_cluster_to_json(input_dict, partition_louvain)
    with open(output_json_file, 'w+') as outfile:
        json.dump(json_with_groups_louvain, outfile)


