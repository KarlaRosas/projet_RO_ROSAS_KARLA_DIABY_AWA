# -*- coding=utf-8 -*-
from proyecto_RO_ROSAS_KARLA_DIABY_AWA.extract_donnes_to_networkx import extract_donnes
import pulp as pl
import networkx as nx
from pulp import *
from pathlib import Path
# ============================================================================ #
#                                  SET MODEL                                   #
# ============================================================================ #


def set_model_cout_net(graph,p, start, n_clientsuppr, n_depsuppr, Entity):
    """Set the coût net problem's model."""

    # ------------------------------------------------------------------------ #
    # Linear problem with minimization
    # ------------------------------------------------------------------------ #

    # ------------------------------------------------------------------------ #
    # Constants
    # ------------------------------------------------------------------------ #
    p = int(p)
    n_clientsuppr = int(n_clientsuppr)
    n_depsuppr = int(n_depsuppr)



    # ------------------------------------------------------------------------ #
    # The variables
    # ------------------------------------------------------------------------ #
    #Listes - Dictionnaires
    DEPOT_OBJ, CLIENTS_OBJ= SeparetEntityObjet(Entity)  #Liste d'objet type entity
    DEPOT = ObtenirEntity(DEPOT_OBJ) #Depots
    CLIENT = ObtenirEntity(CLIENTS_OBJ) #Clients
    ListEnStock = ListeStock(DEPOT_OBJ)  #Qté de stock en Depot
    STOCK = ListaStockPrix(DEPOT, ListEnStock,0)   #Qté de stock en Depot, AutresCoutsDepot
    APROVIS = dict(zip(DEPOT, STOCK))
    DEMANDE = DictionaireDemande(CLIENTS_OBJ, CLIENT)
    COUTSTAUXDOU = [graph.edges()[p, s]['tauxdou'] for p in DEPOT for s in CLIENT] # COUTS DE ESSENCE PAR ROUTE



    #Creation de routes
    ROUTES = [(p, s) for p in DEPOT for s in CLIENT]

    #COUTS DE ESSENCE PAR ROUTE
    COUTS = [[graph.edges()[p, s]['essence'], graph.edges()[p, s]['essence']] for p in DEPOT for s in CLIENT]


    (supply, CoutFixe) = splitDict(APROVIS)
    COUTS = makeDict([DEPOT, CLIENT], COUTS, 0)

    print("ROUTES",ROUTES)
    print("CLIENTS", CLIENT)
    print("DEPOT", DEPOT)
    print("APROVISIONNEMENT", APROVIS)
    print("STOCK", STOCK)
    print("DEMANDE", DEMANDE)



    flow = pl.LpVariable.dicts("Route", (DEPOT, CLIENT), 0, None, pl.LpInteger)
    flowB = pl.LpVariable.dicts("Route", (DEPOT, CLIENT), 0, None, pl.LpBinary)

    #DepotActive = pl.LpVariable.dicts("DepotActive", DEPOT, 0, 1, LpInteger)

    prob = pl.LpProblem(name="Maximisation du benefice net en minimise le coût", sense=LpMinimize)


    # ---------------------------------------------------------------------------- #
    # The objective function - Minimiser les couts
    # ------------------------------------------------------------------------ #

    #prob += pl.lpSum([flow[d][c] * COUTS[d][c] for (d, c) in ROUTES]) , "Total Costs"


    prob += pl.lpSum([flow[d][c] * graph.edges()[d, c]['tauxdou']   for (d, c) in ROUTES]) , "Total Costs"
    # ------------------------------------------------------------------------ #
    # The constraints
    # ------------------------------------------------------------------------ #

    # qr-Client  <=  qr-Depot
    for d in DEPOT:
        prob += pl.lpSum([flow[d][c] for c in CLIENT]) <= supply[d], "Somme de produits dehors du DEPOT %s" % d
        #
    # qr Depot >= qr Demande
    for c in CLIENT:
        prob += pl.lpSum([flow[d][c] for d in DEPOT]) >= DEMANDE[c], "Somme de produits avec le CLIENT %s" % c



    # ------------------------------------------------------------------------ #


    return prob



def PrintList(list, atribut):
    for indice, valor in enumerate(list):
        id=atribut
        print(f'Position {indice} est {valor.id}')

def SeparetEntityObjet(list):
    DEPOT = []
    CLIENTS = []

    for indice, valor in enumerate(list):
        if(valor.type=='depot'):
            DEPOT.append(valor)

        else:
            CLIENTS.append(valor)
    return DEPOT,CLIENTS

def ObtenirEntity(list):
    EntityID = []
    for indice, valor in enumerate(list):
            id= str(valor.id)
            EntityID.append(id)

    return EntityID

def EntityDepotPrixU(list, indice,PrixGPU):
    LISTA=[]
    LISTA.append(list[indice])
    LISTA.append(PrixGPU)

    return LISTA

def ListeStock(list):
    ListeStock=[]
    for indice, valor in enumerate(list):
        #print(f'Position {indice} es {valor.b_entity}')
        quantite=int(valor.b_entity)
        ListeStock.append(abs(quantite))

    return ListeStock

def DictionaireDemande(listeObj, liste):

    ListeDemande=[]
    for indice, valor in enumerate(listeObj):
        #print(f'Position {indice} es {valor.b_entity}')
        quantite=int(valor.b_entity)
        ListeDemande.append(abs(quantite))

    demande= dict(zip(liste,ListeDemande))
    #print("Liste demande",demande)
    return demande

def ListaStockPrix(DEPOT, ListEnStock,AutresCosts):
    STOCK=[]
    for x in range(len(DEPOT)):
        LISTA = EntityDepotPrixU(ListEnStock, x, AutresCosts)
        STOCK.append(LISTA)
    return STOCK


if __name__ == '__main__':

        file_path = '../data/truck_instance_base.data'
        graph, p, start, n_clientsuppr, n_depsuppr, Entity = extract_donnes(file_path)
        file_path = '../data/truck_instance_base.data'
        graph, p, start, n_clientsuppr, n_depsuppr, Entity = extract_donnes(file_path)

        prob,COUTSTAUXDOU = set_model_cout_net(graph, p, start, n_clientsuppr, n_depsuppr,Entity)

        #prob.solve(pl.PULP_CBC_CMD(logPath='./output_file/CBC_max_flow.log'))
        prob.solve()

        qr  = pl.LpVariable("qr", LpInteger)
        gpu = pl.LpVariable("QteGPU", LpInteger)
        coutsTotal = pl.LpVariable("coutsTotal", LpInteger)
        Benefice = pl.LpVariable("Benefice", LpInteger)
        Route_utilises=0
        #Optimal
        print("Status:", pl.LpStatus[prob.status])



        nx.write_graphml(graph, "graph_routes.graphml")
        # ------------------------------------------------------------------------ #
        # Print the solver output
        # ------------------------------------------------------------------------ #
        print(f'Status:\n{pl.LpStatus[prob.status]}')

        print()
        print('-' * 40)
        print()

        # Each of the variables is printed with it's resolved optimum value

        for v in prob.variables():

            print(v.name, "=", v.varValue)
            gpu += int(v.varValue)
            if(v.varValue!=0):
                Route_utilises+=1

        print("Total Costs = ", value(prob.objective))
        print("Route_utilises",Route_utilises)
        qr = pl.lpSum(prob.variables()[x].varValue for x in range(len(prob.variables())))
        print("GPU Vendus : ", qr)

        qrPrix = pl.lpSum(1000 * prob.variables()[x].varValue for x in range(len(prob.variables())))
        print("GPU Vendus * prix unitaire CH= ", qrPrix,"euros")

        # The optimised objective function value is printed to the screen
        print("Benefice max net GPU CH - Couts Totals=", qrPrix - (value(prob.objective)+Route_utilises*20))
