from pathlib import Path
import pulp as pl
import networkx as nx
from pulp import *

from proyecto_RO_ROSAS_KARLA_DIABY_AWA.extract_donnes_to_networkx import extract_donnes
from proyecto_RO_ROSAS_KARLA_DIABY_AWA.truck_pulp import set_model_cout_net

if __name__ == '__main__':

        file_path = '../data/truck_instance_base.data'
        graph, p, start, n_clientsuppr, n_depsuppr, Entity = extract_donnes(file_path)
        prob = set_model_cout_net(graph, p, start, n_clientsuppr, n_depsuppr,Entity)
        nx.write_graphml(graph, "graph_routes.graphml")
        #Minimisation de couts
        prob.solve()

        #Variables
        qr  = pl.LpVariable("qr", LpInteger)
        gpu = pl.LpVariable("QteGPU", LpInteger)
        coutsTotal = pl.LpVariable("coutsTotal", LpInteger)
        Benefice = pl.LpVariable("Benefice", LpInteger)
        Route_utilises=0


        # ------------------------------------------------------------------------ #
        # Print the solver output
        # ------------------------------------------------------------------------ #
        #Optimal
        print("Status:", pl.LpStatus[prob.status])

        print()
        print('-' * 40)
        print()

        # Each of the variables is printed with it's resolved optimum value

        for v in prob.variables():

            print(v.name, "=", v.varValue)
            gpu += int(v.varValue)
            if(v.varValue!=0):
                Route_utilises+=1


        #Presentation de resultats
        print("Total Costs = ", value(prob.objective))
        print("Route_utilises", Route_utilises)
        qr = pl.lpSum(prob.variables()[x].varValue for x in range(len(prob.variables())))
        print("GPU Vendus : ", qr)

        qrPrix = pl.lpSum(1000 * prob.variables()[x].varValue for x in range(len(prob.variables())))
        print("GPU Vendus * prix unitaire CH= ", qrPrix,"euros")

        # The optimised objective function value is printed to the screen
        print("Benefice max net GPU CH - Couts Totals=", qrPrix - (value(prob.objective)+Route_utilises*20), "euros")
