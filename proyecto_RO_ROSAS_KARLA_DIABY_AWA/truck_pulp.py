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

    # ------------------------------------------------------------------------ #
    # The variables
    # ------------------------------------------------------------------------ #


    gpu = pl.LpVariable('gpu', lowBound=0, cat=pl.LpInteger)
    d_edge_gpu = pl.LpVariable.dicts('flow_gpu', graph.edges(),
                                      lowBound=0, cat=pl.LpInteger)


    # ---------------------------------------------------------------------------- #
    # The objective function
    # ------------------------------------------------------------------------ #

    prob += gpu, 'maximize_quantité_de_GPU'

    # ------------------------------------------------------------------------ #
    # The constraints
    # ------------------------------------------------------------------------ #
    # C1: d x PHI_0 + A x PHI = 0 (the flow conservation for each vertex)
    for v in graph.nodes():
        prob += calcul_d_mult_PHI_0(v, gpu) \
            + calcul_A_mult_PHI(graph, v, d_edge_gpu) == 0, \
            f'flow_conservation_{v}'

    # C2: PHI <= C (capacity is the flow limit for each edge)
    for e in graph.edges():
        prob += d_edge_gpu[e] <= graph.edges()[e]['cap'], \
            f'gpu_limit_{e}'

    return prob, d_edge_gpu


def calcul_d_mult_PHI_0(v, gpu):
    """Return the equation part d_v x PHI_0."""
    equation = 0
    if v == start:
        equation -= gpu
        print("ECUATION SOURCE", equation)
    elif v == 'D2':
        equation += gpu
        print("ECUATION TARGET", equation)
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

    file_path = 'truck_instance_base.data'
    graph,p, start, n_clientsuppr, n_depsuppr = extract_donnes(file_path)
    #solve_cout_net()
    prob, d_edge_gpu = set_model_cout_net(graph,p, start, n_clientsuppr, n_depsuppr)
    prob.solve(pl.PULP_CBC_CMD(logPath='./CBC_max_flow.log'))

# ------------------------------------------------------------------------ #
    # Print the solver output
    # ------------------------------------------------------------------------ #
    print(f'Status:\n{pl.LpStatus[prob.status]}')

    print()
    print('-' * 40)
    print()

    # Each of the variables is printed with it's resolved optimum value
    for edge, variable in d_edge_gpu.items():
        edge_gpu = variable.varValue

        print(f'EDGE = {edge} : FLOW = {edge_gpu}')
        graph.edges()[edge]['flow'] = edge_gpu
        nx.write_graphml(graph, "test.graphml")



