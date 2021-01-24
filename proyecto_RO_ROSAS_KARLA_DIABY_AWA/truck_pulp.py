from proyecto_RO_ROSAS_KARLA_DIABY_AWA.extract_donnes_to_networkx import extract_donnes
import pulp as pl
# ============================================================================ #
#                                  SET MODEL                                   #
# ============================================================================ #


def set_model_cout_net(t_cost, t_ru, t_quantite_gpu, t_dc, t_sd):
    """Set the coût net problem's model."""
    # ------------------------------------------------------------------------ #
    # Linear problem with maximisation
    # ------------------------------------------------------------------------ #
    prob = pl.LpProblem('The_benefice_max_net_problem', pl.LpMaximize)

    # ------------------------------------------------------------------------ #
    # Constants
    # ------------------------------------------------------------------------ #
    ar_essence = 20
    br_taux_douaniere = 30
    capr = 10
    p = 10

    # ------------------------------------------------------------------------ #
    # The variables
    # ------------------------------------------------------------------------ #

    ru = pl.LpVariable('route_utilise', cat=pl.LpBinary)
    t_cost = pl.LpVariable('cout_route_cr', cat=pl.LpInteger)
    qr = pl.LpVariable('quantite_gpu', lowBound=0, cat=pl.LpInteger)
    dc = pl.LpVariable('demande_client', lowBound=0, cat=pl.LpInteger)
    sd = pl.LpVariable('stock_depot', lowBound=0, cat=pl.LpInteger)

    #t_cost = ar_essence+br_taux_douaniere * qr
# ---------------------------------------------------------------------------- #
    # The objective function
    # ------------------------------------------------------------------------ #
    # Somme de tous les GPU vendus * 1000 - somme de tous les couts de routes
    prob += pl.lpSum(qr * 1000 - (ar_essence+br_taux_douaniere * qr)),'Total_Benefice_Net'

    # ------------------------------------------------------------------------ #
    # The constraints
    # ------------------------------------------------------------------------ #

    prob += pl.lpSum(qr) >= 0
    print("Contraint1", prob)

    prob += pl.lpSum(qr) >= dc
    print("Contraint2", prob)

    prob += pl.lpSum(dc) >= 0
    print("Contraint3", prob)

    prob += pl.lpSum(qr) <= p
    print("Contraint4", prob)

    prob += pl.lpSum(qr) <= capr
    print("Contraint5", prob)









def solve_cout_net():
    """Solve the simple example."""
    # ------------------------------------------------------------------------ #
    # Set data
    # ------------------------------------------------------------------------ #

    t_cost=(20+30*10)  #essence + taux souaniere * quantite de GPU apres traverse
    t_ru=(1)
    t_quantite_gpu=(10)
    t_dc=(3)
    t_sd=(10)
    print("t_cost", t_cost)

    # ------------------------------------------------------------------------ #
    # Solve the problem using the model
    # ------------------------------------------------------------------------ #
    prob = set_model_cout_net(t_cost, t_ru, t_quantite_gpu, t_dc, t_sd)
    prob.solve(pl.PULP_CBC_CMD())

    # ------------------------------------------------------------------------ #
    # Print the solver output
    # ------------------------------------------------------------------------ #
    print(f'Status:\n{pl.LpStatus[prob.status]}')

    print()
    print('-' * 40)
    print()


#Main test
if __name__ == '__main__':

    #file_path = 'truck_instance_base.data'
    #extract_donnes(file_path)
    solve_cout_net()
