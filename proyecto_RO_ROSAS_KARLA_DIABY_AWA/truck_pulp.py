from proyecto_RO_ROSAS_KARLA_DIABY_AWA.extract_donnes_to_networkx import extract_donnes
import pulp as pl
import networkx as nx
# ============================================================================ #
#                                  SET MODEL                                   #
# ============================================================================ #


def set_model_cout_net(graph,p, start, n_clientsuppr, n_depsuppr):
    """Set the coût net problem's model."""
    # ------------------------------------------------------------------------ #
    # Linear problem with maximisation
    # ------------------------------------------------------------------------ #
    prob = pl.LpProblem('The_benefice_max_net_problem', pl.LpMaximize)

    print("------------NODES------------")

    for k, v in graph.nodes(data=True):
        print(k, v["type"], v["entity"])

    print("Nodes", graph.nodes)
    print("Edge", graph.edges)

    print("------------CONSTANTS------------")
    print("P:", p, " start:", start, " Depôt Supr:", n_depsuppr, " Clients Supr:", n_clientsuppr)

    nx.write_graphml(graph, "test.graphml")





    # ------------------------------------------------------------------------ #
    # Constants
    # ------------------------------------------------------------------------ #


    # ------------------------------------------------------------------------ #
    # The variables
    # ------------------------------------------------------------------------ #


# ---------------------------------------------------------------------------- #
    # The objective function
    # ------------------------------------------------------------------------ #


    # ------------------------------------------------------------------------ #
    # The constraints
    # ------------------------------------------------------------------------ #




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

    set_model_cout_net(graph,p, start, n_clientsuppr, n_depsuppr)

