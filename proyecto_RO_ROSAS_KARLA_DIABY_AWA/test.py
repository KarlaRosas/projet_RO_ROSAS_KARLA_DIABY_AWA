from pathlib import Path
import pulp as pl
import networkx as nx
from pulp import *

from proyecto_RO_ROSAS_KARLA_DIABY_AWA.extract_donnes_to_networkx import extract_donnes
from proyecto_RO_ROSAS_KARLA_DIABY_AWA.truck_pulp import set_model_cout_net

if __name__ == '__main__':

        file_path = '../data/truck_instance_base.data'
        graph, p, start, n_clientsuppr, n_depsuppr, Entity = extract_donnes(file_path)
        file_path = '../data/truck_instance_base.data'
        graph, p, start, n_clientsuppr, n_depsuppr, Entity = extract_donnes(file_path)

        prob,COUTSTAUXDOU = set_model_cout_net(graph, p, start, n_clientsuppr, n_depsuppr,Entity)

        prob.solve(pl.PULP_CBC_CMD(logPath='./output_file/CBC_max_flow.log'))
        prob.solve(pl.PULP_CBC_CMD())

        gpu = pl.LpVariable("gpi", LpInteger)
        Benefice = pl.LpVariable("Benefice", LpInteger)

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

        # The optimised objective function value is printed to the screen
        print("GPU VENDUS", prob.variables()[0].varValue + prob.variables()[1].varValue + prob.variables()[2].varValue +
              prob.variables()[3].varValue + prob.variables()[4].varValue)
        print("Benefice max net GPU (VENDU*1000)-(COUTS)=", (
                    prob.variables()[0].varValue + prob.variables()[1].varValue + prob.variables()[2].varValue +
                    prob.variables()[3].varValue + prob.variables()[4].varValue) * 1000 - value(prob.objective))
