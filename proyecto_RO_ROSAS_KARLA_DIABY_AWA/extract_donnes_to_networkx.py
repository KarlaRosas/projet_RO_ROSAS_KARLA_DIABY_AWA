# -*- coding=utf-8 -*-
#Salut
import networkx as nx




def extract_donnes(file_path):
    Entity = []
    graph =nx.DiGraph()


    with open(file_path, 'r') as f_in:
        # Extract data from header
        header = f_in.readline()
        p, start, n_clientsuppr, n_depsuppr = ((str_num) for str_num in header.split())
        # Extract data from blocks

        print("P:", p, " start:",start, " Depôt Supr:", n_depsuppr," Clients Supr:", n_clientsuppr)
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
                #objet = creationEntity(id, type, b_entity)
                #Entity.append(objet)
            elif block == 'ROADS':
                #road_start, road_end, cap_road, alpha_r, beta_r = line_split
                road_start = line_split[0]
                road_end = line_split[1]
                cap_road = int(line_split[2])
                alpha_r = int(line_split[3])
                beta_r = int(line_split[4])
                #add_nodes(graph, road_start, road_end, cap_road, alpha_r, beta_r)
                add_edge(graph,road_start,road_end,cap_road,alpha_r,beta_r)
                #print("road_start, road_end, cap_road, alpha_r, beta_r: ",road_start, road_end, cap_road, alpha_r, beta_r)
            else:
                exit(f'ERROR: line = {line}')

        #print("Block",block)
        #print("Taille liste", len(Entity))
        #print("En la liste", Entity[2].id)
        #print("  Test d'exportation des données...")

    return graph

#Creation d'objet Entity
class Entity:
    id = ''
    type = ''
    b_entity = ''

    def print_information(self,id,type,b_entity):
        print(self.id)
        print(self.type)
        print(self.b_entity)


#Instantiation d'objet Entity
def creationEntity(id, type, b_entity):
    entity1 = Entity()
    entity1.id = id
    entity1.type = type
    entity1.b_entity = b_entity
    print("Id, type, entity",entity1.id,entity1.type,entity1.b_entity)

    return entity1

def add_nodes(graph, road_start, road_end, cap_road, alpha_r, beta_r):

    graph.add_node(road_start, road_end, capacity = cap_road, essence = alpha_r, taux_adou = beta_r)

def add_edge(graph,start,end, cap_road, alpha_r, beta_r):
    graph.add_edge(start,end, cap=cap_road, essence=alpha_r, tauxdou = beta_r)


