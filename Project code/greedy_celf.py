import matplotlib.pyplot as plt
import numpy as np
import time
from igraph import *
from tqdm import tqdm
import relation_to_json as rel

def IC(g, S, p=0.1, mc=1000):
    """
    Input:  graph object, set of seed nodes, propagation probability
            and the number of Monte-Carlo simulations
    Output: average number of nodes influenced by the seed nodes
    """

    # Loop over the Monte-Carlo Simulations
    spread = []
    for i in range(mc):

        # Simulate propagation process
        new_active, A = S[:], S[:]
        while new_active:

            # For each newly active node, find its neighbors that become activated
            new_ones = []
            for node in new_active:
                # Determine neighbors that become infected
                np.random.seed(i)
                success = np.random.uniform(0, 1, len(g.neighbors(node, mode="out"))) < p
                new_ones += list(np.extract(success, g.neighbors(node, mode="out")))

            new_active = list(set(new_ones) - set(A))

            # Add newly activated nodes to the set of activated nodes
            A += new_active

        spread.append(len(A))

    return (np.mean(spread))


def greedy(g, k, p=0.1, mc=1000):
    """
    Input:  graph object, number of seed nodes
    Output: optimal seed set, resulting spread, time for each iteration
    """

    S, spread, timelapse, start_time = [], [], [], time.time()

    # Find k nodes with largest marginal gain
    for _ in tqdm(range(k)):

        # Loop over nodes that are not yet in seed set to find biggest marginal gain
        best_spread = 0
        for j in tqdm(set(range(g.vcount())) - set(S)):

            # Get the spread
            s = IC(g, S + [j], p, mc)

            # Update the winning node and spread so far
            if s > best_spread:
                best_spread, node = s, j

        # Add the selected node to the seed set
        S.append(node)

        # Add estimated spread and elapsed time
        spread.append(best_spread)
        timelapse.append(time.time() - start_time)

    return (S, spread, timelapse)



def celf(g, k, p=0.1, mc=1000):
    """
    Input:  graph object, number of seed nodes
    Output: optimal seed set, resulting spread, time for each iteration
    """

    # --------------------
    # Find the first node with greedy algorithm
    # --------------------

    # Calculate the first iteration sorted list
    start_time = time.time()
    marg_gain = [IC(g, [node], p, mc) for node in tqdm(range(g.vcount()))]

    # Create the sorted list of nodes and their marginal gain
    Q = sorted(zip(range(g.vcount()), marg_gain), key=lambda x: x[1], reverse=True)

    # Select the first node and remove from candidate list
    S, spread, SPREAD = [Q[0][0]], Q[0][1], [Q[0][1]]
    Q, LOOKUPS, timelapse = Q[1:], [g.vcount()], [time.time() - start_time]

    # --------------------
    # Find the next k-1 nodes using the list-sorting procedure
    # --------------------

    for _ in tqdm(range(k - 1)):

        check, node_lookup = False, 0

        while not check:
            # Count the number of times the spread is computed
            node_lookup += 1

            # Recalculate spread of top node
            current = Q[0][0]

            # Evaluate the spread function and store the marginal gain in the list
            Q[0] = (current, IC(g, S + [current], p, mc) - spread)

            # Re-sort the list
            Q = sorted(Q, key=lambda x: x[1], reverse=True)

            # Check if previous top node stayed on top after the sort
            check = (Q[0][0] == current)

        # Select the next node
        spread += Q[0][1]
        S.append(Q[0][0])
        SPREAD.append(spread)
        LOOKUPS.append(node_lookup)
        timelapse.append(time.time() - start_time)

        # Remove the selected node from the list
        Q = Q[1:]

    return (S, SPREAD, timelapse, LOOKUPS)



def create_igraph(source, target, vertic):
    g = Graph(directed=True)
    g.add_vertices(vertic)
    g.add_edges(zip(source, target))
    return g




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

    # celf_out = gc.celf(ig, 1000, 0.1, 1)
    # activ = independent_cascade(ig, celf_out[0], 0.1)
    # data = read_json_file('relations.json')
    # activate_to_json(activ, data)

    celf_output = celf(ig, 2, p=0.1, mc=1)
    print("celf output:   " + str(celf_output[0]))
    greedy_output = greedy(ig, 2, p=0.1, mc=1)
    print("greedy output:   " + str(greedy_output[0]))

    # Plot settings
    plt.rcParams['figure.figsize'] = (9, 6)
    plt.rcParams['lines.linewidth'] = 4
    plt.rcParams['xtick.bottom'] = False
    plt.rcParams['ytick.left'] = False

    # Plot Computation Time
    plt.plot(range(1, len(greedy_output[2]) + 1), greedy_output[2], label="greedy", color="#FBB4AE")
    plt.plot(range(1, len(celf_output[2]) + 1), celf_output[2], label="celf", color="#B3CDE3")

    plt.ylabel('Computation Time (Seconds)');
    plt.xlabel('Size of Seed Set')
    plt.title('Computation Time');
    plt.legend(loc=2);

    plt.show()

    # Plot Expected Spread by Seed Set Size
    plt.plot(range(1, len(greedy_output[1]) + 1), greedy_output[1], label="greedy", color="#FBB4AE")
    plt.plot(range(1, len(celf_output[1]) + 1), celf_output[1], label="celf", color="#B3CDE3")

    plt.xlabel('Size of Seed Set');
    plt.ylabel('Expected Spread')
    plt.title('Expected Spread');
    plt.legend(loc=2);

    plt.show()