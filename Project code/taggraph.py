
import json
import twitterscrape as ts
from itertools import combinations
import relation_to_json as rel
import community_detection
import instagramscraper as isp

def read_tags_insta(name):
    # empty list to read list from a file
    names = []
    # open file and read the content in a list
    with open(f'instagramuser/{name}/tags.txt', 'r', encoding="utf-8") as fp:
        for line in fp:
            # remove linebreak from a current name
            # linebreak is the last character of each line
            x = line[:-1]

            # add current item to the list
            names.append(x)

    return names

def read_json_file(filename):
    with open(filename, 'r') as f:
        data = json.load(f)
    return data


def build_tag_graph(file_name):
    all = ts.read_alluser_fromFile()
    allrel = []

    for p in all:
        c = []
        try:
            c = ts.read_comments(p)
        except:
            pass
        for com in c:
            taga = ts.find_hashtags(com)
            res = []
            n = len(taga)
            for i in range(n):
                for j in range(n):
                    if i == j:
                        continue
                    res.append((ts.remove_hashtag(taga[i]), ts.remove_hashtag(taga[j])))

            if len(res) > 0:
                allrel += res


    with open(file_name, 'w', encoding='utf-8') as f:
        for (u1, u2) in allrel:
            f.write(f'{u1} {u2}\n')

def count_each_tag():
    commdic = {}
    all = ts.read_alluser_fromFile()
    for p in all:
        c = []
        try:
            c = ts.read_comments(p)
        except:
            pass

        commdic[p] = ts.find_hashtags_list(c)

    counttag = {}
    for p in commdic:
        tags = commdic[p]
        for t in tags:
            counttag[ts.remove_hashtag(t)] = 0

    for p in commdic:
        tags = commdic[p]
        for t in tags:
            counttag[ts.remove_hashtag(t)] += 1

    return counttag


def tags_relation_tojason(counttag, tag_edges, tag_graph_json):
    nodes = set()
    edges = set()
    dict = {}
    name_to_id = {}

    with open(tag_edges, 'r', encoding='utf-8') as f:
        for line in f:
            eachline = line[:-1]
            accounts = eachline.split(" ")
            account_1 = accounts[0]
            account_2 = accounts[1]

            nodes.add(account_1)
            nodes.add(account_2)
            edges.add((account_1, account_2))

    dict["nodes"] = []

    id_n = 0
    for account in nodes:
        dict["nodes"].append({"id": id_n, "name": account, "group": 1,
                              'freq': counttag[account]})
        name_to_id[account] = id_n
        id_n += 1

    dict["links"] = []
    bi_links = set()
    id_l = 0
    for accounts in edges:
        id_1 = name_to_id[accounts[0]]
        id_2 = name_to_id[accounts[1]]
        if (accounts[1], accounts[0]) in edges:
            bi_links.add((id_1, id_2))
            if (id_2, id_1) not in bi_links:
                dict["links"].append({"id": id_l, "source": id_1, "target": id_2, "value": 0.3, "bi_directional": True})
                id_l += 1
        else:
            dict["links"].append({"id": id_l, "source": id_1, "target": id_2, "value": 0.3, "bi_directional": False})
            id_l += 1

    with open(tag_graph_json, 'w') as outfile:
        json.dump(dict, outfile)

    print("json created")


if __name__ == '__main__':
    tag_edges_file = 'alltagrelationship.txt'
    tag_graph_json = '02 visual/tagGraph.json'
    tag_cluster_json = '02 visual/tagClusterGraph.json'

    build_tag_graph(tag_edges_file)
    tag_freq = count_each_tag()
    tags_relation_tojason(tag_freq, tag_edges_file, tag_graph_json)

    community_detection.community_detection(tag_edges_file,
                                            tag_graph_json,
                                            tag_cluster_json)
