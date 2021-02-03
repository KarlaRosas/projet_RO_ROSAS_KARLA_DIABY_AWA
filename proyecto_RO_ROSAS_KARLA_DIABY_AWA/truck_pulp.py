from proyecto_RO_ROSAS_KARLA_DIABY_AWA.extract_donnes_to_networkx import extract_donnes
import pulp as pl
import networkx as nx
# ============================================================================ #
#                                  SET MODEL                                   #
# ============================================================================ #


def set_model_cout_net(graph,p, start, n_clientsuppr, n_depsuppr):
    """Set the coût net problem's model."""
    print("------------NODES------------")

    for k, v in graph.nodes(data=True):
        print(k, v["type"], v["entity"])

    print("Nodes", graph.nodes)
    print("Edge", graph.edges)

    print("------------CONSTANTS------------")
    print("P:", p, " start:", start, " Depôt Supr:", n_depsuppr, " Clients Supr:", n_clientsuppr)





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
    for (u, v) in graph.edges():

        # Add the edges binaries
        x_routes[(u, v)] = pl.LpVariable(f'route_{u}_{v}', cat=pl.LpBinary)

        if not nx.is_directed(graph):
            # because in undirected graph we can go from both directions
            x_routes[(v, u)] = pl.LpVariable(f'route_{v}_{u}', cat=pl.LpBinary)

    print("Variable routes----------------",x_routes)

    for (u, v) in graph.edges():
        flow = pl.LpVariable.dicts("Route",(u,v),0,None, pl.LpInteger )
    print("Flow", flow)


    ##FLOW - QUANTITE GPU
    gpu = pl.LpVariable('gpu', lowBound=0, cat=pl.LpInteger)



    # ---------------------------------------------------------------------------- #
    # The objective function
    # ------------------------------------------------------------------------ #

    #prob += gpu, 'maximize_quantité_de_GPU'   ##qr *1000 - COUT
    prob += pl.lpSum(x_routes[(u, v)] * (graph.edges()[u, v]['essence']+ graph.edges()[u, v]['tauxdou'])
                     for (u, v) in graph.edges()), 'minimize_the_cut'
    # ------------------------------------------------------------------------ #
    # The constraints")

    return prob




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

    file_path = 'truck_instance_base.data'
    graph,p, start, n_clientsuppr, n_depsuppr = extract_donnes(file_path)
    #solve_cout_net()
    prob= set_model_cout_net(graph,p, start, n_clientsuppr, n_depsuppr)
    #prob.solve(pl.PULP_CBC_CMD(logPath='./CBC_max_flow.log'))
    prob.solve(pl.PULP_CBC_CMD())

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





