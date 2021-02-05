# -*- coding=utf-8 -*-
from proyecto_RO_ROSAS_KARLA_DIABY_AWA.extract_donnes_to_networkx import extract_donnes
import pulp as pl
import networkx as nx
from pathlib import Path
# ============================================================================ #
#                                  SET MODEL                                   #
# ============================================================================ #


def set_model_cout_net(graph,p, start, n_clientsuppr, n_depsuppr):
    """Set the coût net problem's model."""

    p =int(p)
    n_clientsuppr = int(n_clientsuppr)
    n_depsuppr = int(n_depsuppr)
    # ------------------------------------------------------------------------ #
    # Linear problem with maximisation
    # ------------------------------------------------------------------------ #

    prob = pl.LpProblem(name='The_benefice_max_net_problem', sense=pl.LpMaximize)

    #minimiser le cout et maxime le benefice*

    # ------------------------------------------------------------------------ #
    # The variables
    # ------------------------------------------------------------------------ #
    #Variables pour les edge ROUTE
    x_routes = {}
    depots = []
    clients=[]


    flow = pl.LpVariable.dicts("Route", (depots, clients), 0, None, pl.LpInteger)




    #Depot
    for u in graph.nodes():
        if(graph.nodes()[u]['type']=='depot'):
            depots.append(graph.nodes()[u])
        else:
            clients.append(graph.nodes()[u])

    print("DEPOTS-------",depots)
    print("CLIENTS-------", clients)


    for (u, v) in graph.edges():

        # Add the edges binaries
        x_routes[(u, v)] = pl.LpVariable(f'route_{u}_{v}', cat=pl.LpBinary)

        if not nx.is_directed(graph):
            # because in undirected graph we can go from both directions
            x_routes[(v, u)] = pl.LpVariable(f'route_{v}_{u}', cat=pl.LpBinary)

    print("Variable routes----------------",x_routes)


    for u in graph.nodes():
        if(graph.nodes()[u]['type']=='depot'):
            print("Holis",graph.nodes()[u])
        else:
            print("Sad", graph.nodes()[u])


    ##FLOW - QUANTITE GPU
    #gpu = pl.LpVariable('gpu', lowBound=0, cat=pl.LpInteger)



    # ---------------------------------------------------------------------------- #
    # The objective function
    # ------------------------------------------------------------------------ #


    prob +=  pl.lpSum(x_routes[(u, v)] * (graph.edges()[u, v]['essence']+ graph.edges()[u, v]['tauxdou'])
                     for (u, v) in graph.edges() ) , 'minimize_the_cut'
    # ------------------------------------------------------------------------ #
    # The constraints")





    return prob

def calcul_d_mult_PHI_0(v, flow):
    """Return the equation part d_v x PHI_0."""
    equation = 0
    if v == 'D1':
        equation -= flow
    elif v == 'D2':
        equation += flow
    return equation


def calcul_A_mult_PHI(graph, v, d_edge_flow):
    """Return the equation part a_v x PHI_v."""
    equation = 0
    for u in graph.predecessors(v):
        equation -= d_edge_flow[u, v]
    for w in graph.successors(v):
        equation += d_edge_flow[v, w]
    return equation



def solve_cout_net():
    """Solve the simple example."""
    # ------------------------------------------------------------------------ #
    # Set data
    # ------------------------------------------------------------------------ #


    # ------------------------------------------------------------------------ #
    # Solve the problem using the model
    # ------------------------------------------------------------------------ #


    # ------------------------------------------------------------------------ #
    # Print the solver output
    # ------------------------------------------------------------------------ #


#Main test
if __name__ == '__main__':

    # Main test
    if __name__ == '__main__':

        file_path = 'truck_instance_base.data'
        graph, p, start, n_clientsuppr, n_depsuppr = extract_donnes(file_path)
        # solve_cout_net()
        prob = set_model_cout_net(graph, p, start, n_clientsuppr, n_depsuppr)
        prob.solve(pl.PULP_CBC_CMD(logPath='./output_file/CBC_max_flow.log'))
        prob.solve(pl.PULP_CBC_CMD())
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
            print(v.name, '=', v.varValue)
