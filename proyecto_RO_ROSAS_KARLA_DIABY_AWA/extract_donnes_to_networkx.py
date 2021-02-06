# -*- coding=utf-8 -*-
import networkx as nx




def extract_donnes(file_path):

    graph =nx.DiGraph()
    Entity =[]

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
                objet = creationEntity(id, type, b_entity)
                Entity.append(objet)
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


    return graph,p, start, n_clientsuppr, n_depsuppr,Entity



#Création de edges et ses attributes
def add_edge(graph,start,end, cap_road, alpha_r, beta_r):
    graph.add_edge(start,end, cap=cap_road, essence=alpha_r, tauxdou = beta_r)


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
    #print("Id, type, entity",entity1.id,entity1.type,entity1.b_entity)

    return entity1

#Main test
if __name__ == '__main__':
    file_path = './truck_instance_base.data'
    extract_donnes(file_path)