
import re
import json
import os

def relations_to_json(input_txt_file, output_json_file):


    nodes = set()
    edges = set()
    dict = {}
    name_to_id = {}

    with open(input_txt_file, 'r') as f:
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
        dict["nodes"].append({"id": id_n, "name": account, "group": 1})
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

    with open(output_json_file, 'w') as outfile:
        json.dump(dict, outfile)

    print("json created")
    return (name_to_id, edges)


def allrealation_toText_Instagram(file_name):
    import instagramscraper as isp
    alluser = isp.read_alluser_fromFile()
    rela = []
    for username in alluser:
        lfollower = []
        lfollowing = []
        try:
            lfollower = isp.read_follower_fromFile(username)
            lfollowing = isp.read_following_fromFile(username)
        except:
            pass
        if len(lfollower) < 2 and len(lfollowing) < 2:
            continue
        for user1 in lfollower:
            rela.append((user1, username))

        for user2 in lfollowing:
            rela.append((username, user2))

    # Write list to file
    with open(file_name, 'w') as f:
        for (u1, u2) in rela:
            f.write(f'{u1} {u2}\n')


def allrealation_toText_Twitter(file_name):
    import twitterscrape as ts
    alluser = ts.read_alluser_fromFile()
    rela = []
    for username in alluser:
        lfollower = []
        lfollowing = []
        try:
            lfollower = ts.read_follower_fromFile(username)
            lfollowing = ts.read_following_fromFile(username)
        except:
            pass
        if len(lfollower) < 2 and len(lfollowing) < 2:
            continue
        for user1 in lfollower:
            rela.append((user1[1:], username))

        for user2 in lfollowing:
            rela.append((username, user2[1:]))

    # Write list to file
    with open(file_name, 'w') as f:
        for (u1, u2) in rela:
            f.write(f'{u1} {u2}\n')




import community_detection

if __name__ == '__main__':

    instagram_edges_text = 'InstagramRelationship.txt'
    twitter_edges_text = 'TwitterRelationship.txt'

    instagram_json_graph = '02 visual/instagram.json'
    twitter_json_graph = '02 visual/Twitter.json'

    instagram_communities_json = '02 visual/instagram_louvain.json'
    twitter_communities_json = '02 visual/twitter_louvain.json'

    allrealation_toText_Instagram(instagram_edges_text)
    relations_to_json(instagram_edges_text, instagram_json_graph)

    allrealation_toText_Twitter(twitter_edges_text)
    relations_to_json(twitter_edges_text, twitter_json_graph)

    community_detection.community_detection(instagram_edges_text,
                                            instagram_json_graph,
                                            instagram_communities_json)

    community_detection.community_detection(twitter_edges_text,
                                            twitter_json_graph,
                                            twitter_communities_json)
