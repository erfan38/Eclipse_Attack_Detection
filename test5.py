#! /usr/bin/env python3

from distutils.command.build import build
from hashlib import new
import igraph
import json
import argparse
from datetime import datetime
import os
import networkx as nx
import matplotlib.pyplot as p
import my_networkx as my_nx
from cdlib import algorithms
import leidenalg as la

def lookup_for_node(index, partition):
    count = 0
    for cluster in partition:
        if index in cluster:
            return count
        else: 
            count += 1
    return -1

drawing_layouts = [
    "bipartite_layout",
    "circular_layout",
    "kamada_kawai_layout",
    "random_layout",
    "rescale_layout",
    "rescale_layout_dict",
    "shell_layout",
    "spring_layout",
    "spectral_layout",
    "planar_layout",
    "fruchterman_reingold_layout",
    "spiral_layout",
    "multipartite_layout",
]

cmap = {
        0: 'pink',
        1: 'teal',
        2: 'black',
        3: 'orange',
        4: 'green',
        5: 'yellow',
        6: 'red',
        7: 'blue',
        8: 'purple',
        9: 'violet',
        10: 'brown',
        11: 'grey',
        12: 'tan',
        13: 'navy',
        14: 'cyan',
        15: 'palegreen',
        16: 'gold',
        17: 'lime',
        18: 'chocolate',
        19: 'blue3',
        20: 'lightcyan',
        21: 'darkred',
        22: 'salmon',
        23: 'orchid',
        24: 'indigo',
        25: 'olivedrab'
    }

global ip_table
ip_table = None


def draw_graph(G):
    # Find the total number of degree, in_degree and out_degree for each node
    for x in G.nodes():
        print(
            "Node: ", x, " has total #degree: ", G.degree(x),
            " , In_degree: ", G.out_degree(x),
            " and out_degree: ", G.in_degree(x)
        )

    # Find the weight for each node

    for u, v in G.edges():
        print("Weight of Edge (" + str(u) + "," + str(v) + ")", G.get_edge_data(u, v))


    #color_map = []
    #count = 0
    #for node in G:
    #    color_map.append(cmap[lookup_for_node(count, partition))
    #nx.draw(G, node_color=color_map, with_labels=True)
    #plt.show()

    fig, ax = p.subplots()
    pos = nx.circular_layout(G)

    nx.draw_networkx_nodes(G, pos, ax=ax, node_color='y')
    nx.draw_networkx_labels(G, pos, ax=ax)

    curved_edges = [edge for edge in G.edges() if reversed(edge) in G.edges()]
    straight_edges = list(set(G.edges()) - set(curved_edges))

    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=straight_edges)
    arc_rad = 0.25

    nx.draw_networkx_edges(G, pos, ax=ax, edgelist=curved_edges, connectionstyle=f'arc3, rad = {arc_rad}')

    edge_weights = nx.get_edge_attributes(G, 'weight')

    print(edge_weights)
    print(curved_edges)

    curved_edge_labels = {edge: edge_weights[edge] for edge in curved_edges}
    straight_edge_labels = {edge: edge_weights[edge] for edge in straight_edges}
    my_nx.my_draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=curved_edge_labels, rotate=False, rad=arc_rad)
    nx.draw_networkx_edge_labels(G, pos, ax=ax, edge_labels=straight_edge_labels, rotate=False)
    fig.savefig("3.png", bbox_inches='tight', pad_inches=0)

    fig.savefig("2.png", bbox_inches='tight', pad_inches=0)
    p.show()



def parse_layout(G, l):

    pos = None
    #print ("Trying layout {}".format(l))
    try:
        if l != "kamada_kawai_layout":
            if l == "bipartite_layout":
                pos = nx.bipartite_layout(G)
            elif l == "circular_layout":
                pos = nx.circular_layout(G)
            elif l == "random_layout":
                pos == nx.random_layout(G)
            elif l == "rescale_layout":
                pos == nx.rescale_layout(G)
            elif l == "rescale_layout_dict":
                pos = nx.rescale_layout_dict(G)
            elif l == "shell_layout":
                pos = nx.shell_layout(G)
            elif l == "spring_layout":
                pos = nx.spring_layout(G)
            elif l == "spectral_layout":
                pos = nx.spectral_layout(G)
            elif l == "planar_layout":
                pos = nx.planar_layout(G)
            elif l == "fruchterman_reingold_layout":
                pos = nx.fruchterman_reingold_layout(G)
            elif l == "spiral_layout":
                pos = nx.spiral_layout(G)
            elif l == "multipartite_layout":
                pos = nx.multipartite_layout(G)
        else:
            pos = nx.kamada_kawai_layout(G)
        print("Layout added: {}".format(l))
    except Exception as e:
        pos = nx.kamada_kawai_layout(G)
        print("Error with {}. Layout added: kamada_kawai_layout".format(l))
        #print(e)

    return pos



def build_ip_table(G, partitions):
    ip_table = list()
    for node in G:
        ip_table.append(node)
    return ip_table

def draw_cluster(args, G, partitions, filepath):

    print("Drawing Cluster...")
    color_map = []
    count = 0
    for node in G:
        color_map.append(cmap[lookup_for_node(count, partitions)])
     
        count += 1
        
    curr_layouts = list()
    if args.test_layouts:
        for layout in drawing_layouts:
            curr_layouts.append(parse_layout(G, layout))
    else:
        curr_layouts.append(parse_layout(G, args.drawing_layout))

    for layout in curr_layouts:
       try:
            nx.draw(G, pos = layout , node_color=color_map, with_labels=True)
            if args.save:
                filename = filepath.split(".txt")[0]+".png"
                print("Saving figure to {}".format(filename))
                p.savefig(filename)
            if args.show:
                p.show()
       except Exception as e:
            print(e)

def get_statistics(G): #, FileName, out_dirname):
    print('### Stats')
    stats = dict()
    for node in G:
        #print("Stats for node {}:, nb of edges: {}, in_degree: {}, out_degree: {}".format(node, G.number_of_edges(node), G.in_degree(node), G.out_degree(node)))
        stats[node] = (G.number_of_edges(node), G.in_degree(node), G.out_degree(node))

    return stats

def parse_stats(stats):
    #print(stats)
    most_sender = ['None', 0]
    most_receiver = ['None', 0]
    tmp = dict()
    for node in stats[0][0]:
        tmp[node] = dict()
        tmp[node]["send"] = 0
        tmp[node]["receive"] = 0

    for iteration in stats:
        for data_type in iteration:
            for node in data_type:
                if node != '[None]':
                    tmp[node]["send"] += int(node[1])
                    tmp[node]["receive"] += int(node[2])
    #print(tmp)
    for node in tmp:
        if tmp[node]["send"] > most_sender[1]:
            most_sender[0] = node
            most_sender[1] = tmp[node]["send"]
        if tmp[node]["receive"] > most_receiver[1]:
            most_receiver[0] = node
            most_receiver[1] = tmp[node]['receive']

    """
    print("### Results")
    print(most_sender)
    print(most_receiver)
    """


def convert_nodesID_to_IP(m_list, table):
    new_list = list()
    for community in range(0, len( m_list)):
        new_list.append(list())
        for nodes in m_list[community]:
            new_list[community].append(table[nodes])

    return new_list

def apply_leiden(args, FileName, out_dirname=None):

    #FileName="./samples/1659054653_GetDataMessage.txt"
    Graphtype=nx.DiGraph()   # use nx.Graph() for undirected graph

    # How to read from a file. Note: if your egde weights are int, 
    # change float to int.
    
    # Creating a directed Graph
    G = nx.DiGraph() #or G = nx.MultiDiGraph()

    # Updating the graph with values taken from file
    G = nx.read_edgelist(
        FileName, 
        create_using=Graphtype,
        nodetype=str,
        data=(('weight',int),)
    )
    #draw_graph(G)

    # Drawing graph without applying leiden
    if args.show:
        nx.draw(G, with_labels=True)
        p.show()

    ######## TODO: build IP TABLE

    G2 = igraph.Graph.from_networkx(G)

    # Applying partitionning
    partition = la.find_partition(G2, la.ModularityVertexPartition);

    ######## TODO: REPLACE / convert ID with IP TABLE
    if args.show_means:
        print("Clustering Results:")
        #print(partition)


    short_filename = FileName.split('/')[2]

    partition_list = str(partition).split('\n')
   
    data = {}
    data["infos"] = out_dirname+"/"+short_filename 
    data["comment"] = partition_list[0]
    clusters = {}
    count = 0
    for i in partition:
        clusters[str(count)] = str(i)
        count += 1
    data["clusters"] = clusters

    # Convert python dictionnary to json, with pretty print
    json_data = json.dumps(data, indent=4)
    
    if args.one_logfile:
        with open("{}/{}".format(out_dirname.split("iteration")[0], "infos.json"), "a+") as f:
            f.write(json_data)
            f.write(",\n")

    else:
        with open("{}/{}".format(out_dirname, "infos.json"), "a+") as f:
            f.write(json_data)
            f.write(",\n")


    stats = get_statistics(G)
    if args.show or args.save:
        draw_cluster(args, G, partition, out_dirname+"/"+short_filename)

    tmp_table = build_ip_table(G, partition)
    new_partition = convert_nodesID_to_IP(partition, tmp_table)
    #print(new_partition)

    return stats, new_partition, G, partition

    """
    global ip_table
    if ip_table is None:
        ip_table = tmp_table
    elif tmp_table  != ip_table:
        print(tmp_table)
        print(ip_table)
        print("##### IP TABLE CHANGEEED")
        exit()
    return stats, partition
    """
    #n: int = 20
    #i: int = 1
    #comm = []


    #H = nx.DiGraph() #if it's a DiGraph()
    #H=nx.Graph() #if it's a typical networkx Graph().

    #H.add_nodes_from(G.nodes(data=True))
    #H.add_edges_from(G.edges(data=True))
    #for v in G2.vs:
        #    print(v['_nx_name'])

        #print(H)
        #partitions = la.find_partition(H[i], la.ModularityVertexPartition)
        

#comm[i] = partition
# visualize communities:
# unique_coms = np.unique(list(partitions.values()))

def compute(args):

    communities = list()
    graph_list = list()
    partition_list = list()
    now = datetime.now()
    stats = list()

    for i in range(0, args.iteration):
        dirname = "./results/{}/iteration_{}".format(now.strftime("%Y_%m_%d_%H-%M-%S"), i)
        os.system("mkdir -p {}".format(dirname))
        print("Starting iteration {}/{}".format(i+1, args.iteration))
        for root, dirnames, filenames in os.walk("./samples/"):
            for file in filenames:
                try:
                    stats.append(list())
                    stat, community, graph, partition = apply_leiden(args, "./samples/"+file, dirname)
                    communities.append(community)

                    ## TO DEBUG
                    graph_list.append(graph)
                    partition_list.append(partition)
                    ##

                    stats[i].append(stat)
                except Exception as e:
                    print(e)

    if args.show_means:
        #print(stats)
        parse_stats(stats)
    

    return communities, graph_list, partition_list


def update_friends(friends:dict, node, community):
    for n in community:
        if n == node:
            break
        if friends.get(node) is not None:
            if friends.get(node).get(n) is None:
                friends[node][n] = 1
            friends[node][n] = friends[node][n] + 1
        else:
            friends[node] = dict()
            friends[node][n] = 1 #(n, 1))

    return friends

def get_best_friends(friends:dict, threshold):

    best = dict()
    #print(friends)
    for node in friends.keys():
        for node_friends in friends[node].keys():
            if int(friends[node][node_friends]) >= threshold:
                if best.get(node) is None:
                    best[node] = dict()
                best[node][node_friends] = friends[node][node_friends]

    return best

def convert_best_friends_to_ip(friends):
    global ip_table
    print(ip_table)
    new_dict = dict()
    for node in friends.keys():
        new_dict[ip_table[node]] = dict()
        for friend in friends[node]:
            new_dict[ip_table[node]][ip_table[friend]] = friends[node][friend]

    return new_dict  

def get_friends(partitions_list):
    print("########## GET FRIENDS")
    friends = dict()
    #print(partitions_list)
    for i in range (0, len(partitions_list)):
    # for i in range (0, len(partitions_list))):
        #print(partitions_list[i])
        communities = partitions_list[i]
        #print(communities)
        for community in communities: #range (0, len(communities)):
            #community = community[3:]
            com_list = community #.replace(' ', '').split(',')
            #print(com_list)
            #print("\n\n")
            for node in com_list:
               friends = update_friends(friends, node, com_list)

    #print(friends)
    return friends


            #for community in range (0, len(communities[communities])):
            #    print("Community" + community)


def compare_to_attacker(args, best_friends):
    victims = list()
    attackers = list()
    with open("file.json", 'r') as f:
        data = json.load(f)

        for i in data:
            if data[i].startswith('VICTIM'):
                victims.append(i)
            else:
                attackers.append(i)

    #print(victims)
    #print(attackers)
   
    # TODO: compute the average of occurences
    victim_stat = dict()
    #print(best_friends)
    for victim in victims:
        victim_stat[victim] = list()
        #if best_friends.get(victim):
        #    victim_stat.append(best_friends[victim])
        #else:
        for best_friend in best_friends:
            for friend in best_friends[best_friend]:
                if friend == "["+victim+"]":
                    victim_stat[victim].append([best_friend, best_friends[best_friend][friend]])

         
    """
    attacker_stat = dict()
    for attacker in attackers:
        #if best_friends.get(attacker):
        #    attacker_stat.append(best_friends[attacker])
        #else:
        for best_friend in best_friends:
            for friend in best_friends[best_friend]:
                if friend == "["+attacker+"]":
                    if not attacker_stat.get(attacker):
                        attacker_stat[attacker] = list()
                    attacker_stat[attacker].append([best_friend, best_friends[best_friend][friend]])
    """


    attacker_stat = dict()
    for attacker in attackers:
        for best_friend in best_friends:
            for friend in best_friends[best_friend]:
                if friend == "["+attacker+"]":
                    if not attacker_stat.get(attacker):
                        attacker_stat[attacker] = dict()
                    attacker_stat[attacker][best_friend] =  best_friends[best_friend][friend]
                    #else:
                    #    print("###### WEEEIRD")
                    #    attacker_stat[attacker][best_friend] +=  best_friends[best_friend][friend]


    for attacker in attacker_stat:
        for friend in attacker_stat[attacker]:
            attacker_stat[attacker][friend] = attacker_stat[attacker][friend] / args.iteration #[0]attacker[friend[1]/args.iteration]
    

    for victim in victim_stat:
        for friend in range (0, len(victim_stat[victim])):
            #for node in friend:
            victim_stat[victim][friend] = {victim_stat[victim][friend][0]: victim_stat[victim][friend][1] / args.iteration}

    golden_list = list()
    for attacker in attacker_stat:
        for friend in attacker_stat[attacker]:
            for victim in victims:
                if friend == "["+victim+"]":
                    golden_list.append([victim, attacker, attacker_stat[attacker][friend]])


    print("### GOLDEN LIST")
    print(golden_list)

    """
    for attacker in attacker_stat:
        for friend in range (0, len(attacker_stat[attacker])):
            attacker_stat[attacker][friend] = {attacker_stat[attacker][friend][0]: attacker_stat[attacker][friend][1] / args.iteration} #[0]attacker[friend[1]/args.iteration]
    
    for victim in victim_stat:
        for  in victim_stat[victim]:
            if 
    """
    return victim_stat, attacker_stat

def print_params(args):

    print("Running script with the following parameters:")
    print("iterations: {}\nshow: {}\nsave: {}\nshow-means: {}\nclear-results: {}\ndrawing_layout: {}\none-logfile: {}".format(args.iteration, args.show, args.save, args.show_means, args.clear_results, args.drawing_layout, args.one_logfile))
    print("Do you want to run with these parameters ? [Y/n]")
    res = input()
    if res == 'n' or res == 'N':
        exit()

def main():

    if not os.path.exists('./results'):
        os.system('mkdir ./results')
    
    parser = argparse.ArgumentParser(description='Community clustering based on leiden algorithm')
    parser.add_argument('iteration', type=int, help='Number of iteration to process')
    parser.add_argument('--show', default=False, action='store_true', help='Show foreach step the diagrams')
    parser.add_argument('--save', default=False, action='store_true', help="Save the pictures of clusters")
    parser.add_argument('--show-means', default=False, action='store_true', help='Display analytics information about clustering')
    parser.add_argument('--clear-results', default=False, action='store_true', help="**ON LINUX**, delete all files and directories in the results folder")
    parser.add_argument('--one-logfile', default=False, action='store_true', help = "Gathers all clusters information of all iterations in one file. Default behavior is to create a file for each iteration")
    parser.add_argument('--drawing-layout', default="kamada_kawai_layout", choices= drawing_layouts, help="Change the drawing layout algorithm")
    parser.add_argument('--test-layouts', default=False, action='store_true', help = "Print each graph with all available layouts. Time consuming, for tests only") 

    args = parser.parse_args()

    print_params(args)

    if args.clear_results:
        os.system("rm -rf ./results/*")

    communities, graph_list, partition_list  = compute(args)
    friends = get_friends(communities)
    #for i in communities:
    #    for j in i:
    #        print(j)
    best_friends = get_best_friends(friends, 2 * args.iteration)
    victim_stats, attacker_stats = compare_to_attacker(args, best_friends)
    #print(best_friends)

    print('# VICTIM')
    print(victim_stats)

    print('# ATTACKERS')
    print(attacker_stats)

    """
    args.show = True
    for i in range (0, len(partition_list)):
        try:
            draw_cluster(args, graph_list[i], partition_list[i], None)
        except Exception as e:
            print('error on drawing this graph')
    """
    
    #print(friends)
    #print(convert_best_friends_to_ip(best_friends))

if __name__ == "__main__":
    main()
