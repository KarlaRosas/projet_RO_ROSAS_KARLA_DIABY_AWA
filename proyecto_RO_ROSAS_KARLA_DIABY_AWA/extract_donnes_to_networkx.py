# -*- coding=utf-8 -*-
#Salut
import networkx as nx




def extract_donnes(file_path):

    graph =nx.DiGraph()

    with open(file_path, 'r') as f_in:
        # Extract data from header
        header = f_in.readline()
        p, start, n_clientsuppr, n_depsuppr = ((str_num) for str_num in header.split())

        # Extract data from blocks

        block = ''
        for line in f_in:
            line_split = line.split()
            if block == '':
                block = line_split[0]
            elif line_split[0] == '}':
                block = ''
            elif block == 'ENTITIES':
                id, type, b_entity = line_split
                graph.add_node(id,type=type, entity=b_entity)

            elif block == 'ROADS':

                road_start = line_split[0]
                road_end = line_split[1]
                cap_road = int(line_split[2])
                alpha_r = int(line_split[3])
                beta_r = int(line_split[4])

                add_edge(graph,road_start,road_end,cap_road,alpha_r,beta_r)

            else:
                exit(f'ERROR: line = {line}')

    return graph,p, start, n_clientsuppr, n_depsuppr



#Création de edges et ses attributes
def add_edge(graph,start,end, cap_road, alpha_r, beta_r):
    graph.add_edge(start,end, cap=cap_road, essence=alpha_r, tauxdou = beta_r)


