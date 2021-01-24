# -*- coding=utf-8 -*-

import networkx as nx

SOURCE = 'S'
TARGET = 'T'


def extract_donnes(file_path):
    Entity = []
    graph =nx.DiGraph()

    graph.add_node(SOURCE)
    graph.add_node(TARGET)
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
                objet = creationEntity(id, type, b_entity)
                Entity.append(objet)
            elif block == 'ROADS':
                road_start, road_end, cap_road, alpha_r, beta_r = line_split
                print("road_start, road_end, cap_road, alpha_r, beta_r: ",road_start, road_end, cap_road, alpha_r, beta_r)


        print("Block",block)
        print("Taille liste", len(Entity))
        print("En la liste", Entity[2].id)
        print("  Test d'exportation des données...")

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






