import numpy as np
from numpy import random
from numpy.random import choice
from collections import Counter

import nashpy as nash

# container variables to track changes across all iterations
container_M1 = []
container_M2 = []
container_P1 = []
container_P2 = []
container_choice_M1 = []
container_choice_M2 = []
container_choice_P1 = []
container_choice_P2 = []
container_max_master_one_utility = []
container_max_proxy_one_utility = []
container_stochastic_process = []
container_stochastic_suppression = []

# set utility variables
M1_cc = 2
M1_cd = 0
M1_dc = 1
M1_dd = 1

M2_cc = 2
M2_dc = 1
M2_cd = 0
M2_dd = 1

P1_cc = 3
P1_cd = 0
P1_dc = 5
P1_dd = 1

P2_cc = 3
P2_dc = 5
P2_cd = 0
P2_dd = 1

# min values for acceptable range of proxy payoffs for master. Determines strategy switch
MP1_depen_floor = min(P1_cc, P1_cd, P1_dc, P1_dd)
MP2_depen_floor = min(P2_cc, P2_dc, P2_cd, P2_dd)

# utility function variables
# determine interaction between the games

reward_step = 0  # proxy c or d payoffs get increased or decreased each t based on choice_M1 == choice_P1
exo_shock = 0  # exogenous shock, two random occurrences, one increase in M c payoffs one in M d payoffs
env_noise = "rw"  # random walk changes decreasing or increasing all variables
rel_stability = 0.3  # suppression of env_noise (range 0.3, 1). 0.3 is max stability
pm_dependence1 = 1
pm_dependence2 = 1  # dependence of proxy on master, decreases as penalties increase, weight on reward_step
# mp_dependence = "range"  # range in which proxy payoff at time t and pm_dependence have to fall, otherwise master change strategy for the next five iterations

reward_state1 = None
reward_state2 = None

for t in range(100):

    # define master_one game
    M1 = np.array([[M1_cc, M1_cd], [M1_dc, M1_dd]])
    M2 = np.array([[M2_cc, M2_dc], [M2_cd, M2_dd]])

    # define proxy_one game
    P1 = np.array([[P1_cc, P1_cd], [P1_dc, P1_dd]])
    P2 = np.array([[P2_cc, P2_dc], [P1_cd, P2_dd]])

    # build games
    game_master_one = nash.Game(M1, M2)
    game_proxy_one = nash.Game(P1, P2)

    # obtain equilibria through vertex enumeration
    eq_master_one = game_master_one.vertex_enumeration()
    list_eq_master_one = [e for e in eq_master_one]

    eq_proxy_one = game_proxy_one.vertex_enumeration()
    list_eq_proxy_one = [e for e in eq_proxy_one]

    # for each master_one equilibrium, separate the players' strategies
    eq_strategies_M1 = []
    eq_strategies_M2 = []

    for e in range(0, len(list_eq_master_one)):
        eq_strategies_M1.append(list_eq_master_one[e][0])
        eq_strategies_M2.append(list_eq_master_one[e][1])

    # for each proxy_one equilibrium, separate the players' strategies
    eq_strategies_P1 = []
    eq_strategies_P2 = []

    for e in range(0, len(list_eq_proxy_one)):
        eq_strategies_P1.append(list_eq_proxy_one[e][0])
        eq_strategies_P2.append(list_eq_proxy_one[e][1])

    # calculate utilities for master_one equilibria
    util_master_one = []

    for e in range(0, len(eq_strategies_M1)):
        util_master_one.append(game_master_one[eq_strategies_M1[e], eq_strategies_M2[e]].tolist())

    # calculate utilities for proxy_one equilibria
    util_proxy_one = []

    for e in range(0, len(eq_strategies_P1)):
        util_proxy_one.append(game_proxy_one[eq_strategies_P1[e], eq_strategies_P2[e]].tolist())


    # find master_one equilibrium with highest utility
    optimal_eq_M1 = eq_strategies_M1[util_master_one.index(max(util_master_one))].tolist()
    optimal_eq_M2 = eq_strategies_M2[util_master_one.index(max(util_master_one))].tolist()

    # find proxy_one equilibrium with highest utility
    optimal_eq_P1 = eq_strategies_P1[util_proxy_one.index(max(util_proxy_one))].tolist()
    optimal_eq_P2 = eq_strategies_P2[util_proxy_one.index(max(util_proxy_one))].tolist()

    # take absolute values of optimal_eq for probability calculation
    abs_optimal_eq_M1 = [abs(e) for e in optimal_eq_M1]
    abs_optimal_eq_M2 = [abs(e) for e in optimal_eq_M2]
    abs_optimal_eq_P1 = [abs(e) for e in optimal_eq_P1]
    abs_optimal_eq_P2 = [abs(e) for e in optimal_eq_P2]

    # translate strategies into cooperate or defect choices
    # probability-based choice to cover mixed strategies
    categories = ["c", "d"]

    # if proxy utility below minimum, master strategy reverts
    if len(container_max_proxy_one_utility) > 0:
        if container_max_proxy_one_utility[-1][1] > MP1_depen_floor and \
                container_max_proxy_one_utility[-1][1] > MP2_depen_floor:
            choice_M1 = choice(categories, 1, p=abs_optimal_eq_M1).tolist()
            choice_M2 = choice(categories, 1, p=abs_optimal_eq_M2).tolist()

        # if proxy1 util equal or below min, master1 choice reverses, master2 choice follows eq in master game
        elif container_max_proxy_one_utility[-1][1] <= MP1_depen_floor and \
                container_max_proxy_one_utility[-1][1] > MP2_depen_floor:
            if choice_M1 == ['c']:
                choice_M1 = ['d']
            else:
                choice_M1 = ['c']
            choice_M2 = choice(categories, 1, p=abs_optimal_eq_M2).tolist()

        # if proxy2 util equal or below min, master2 choice reverses, master1 choice follows eq in master game
        elif container_max_proxy_one_utility[-1][0] > MP1_depen_floor and \
                container_max_proxy_one_utility[-1][0] <= MP2_depen_floor:
            choice_M1 = choice(categories, 1, p=abs_optimal_eq_M1).tolist()
            if choice_M2 == ['c']:
                choice_M2 = ['d']
            else:
                choice_M2 = ['c']
        else:
            if choice_M1 == ['c']:
                choice_M1 = ['d']
            else:
                choice_M1 = ['c']
            if choice_M2 == ['c']:
                choice_M2 = ['d']
            else:
                choice_M2 = ['c']
    # if proxy utilities above minimum, master choice follows equilibrium in master game
    else:
         choice_M1 = choice(categories, 1, p=abs_optimal_eq_M1).tolist()
         choice_M2 = choice(categories, 1, p=abs_optimal_eq_M2).tolist()

    # proxy choice purely based on equilibrium in proxy game
    choice_P1 = choice(categories, 1, p=abs_optimal_eq_P1).tolist()
    choice_P2 = choice(categories, 1, p=abs_optimal_eq_P2).tolist()

    # reward step
    reward_step = 0.05

    # relative stability measured based on relative amount of overall cooperation
    flat_container_choice_M1 = [k for e in container_choice_M1 for k in e]
    flat_container_choice_M2 = [k for e in container_choice_M2 for k in e]
    flat_container_choice_P1 = [k for e in container_choice_P1 for k in e]
    flat_container_choice_P2 = [k for e in container_choice_P2 for k in e]
    aggregate_choices = flat_container_choice_M1 + flat_container_choice_M2 + flat_container_choice_P1 + flat_container_choice_P2

    if len(container_choice_M1) == 0:
        rel_stability = 1
    else:
        freq_aggr_choices = Counter(aggregate_choices)
        freq_aggr_cooperate = freq_aggr_choices['c'] / freq_aggr_choices['d']
        rel_stability = freq_aggr_cooperate

    # dependence of proxy on master, decreasing with negative rewards
    if reward_state1 is not None:
        if reward_state1 is "positive":
            if pm_dependence1 < 1:
                pm_dependence1 += 0.01
            else:
                pass
        else:
            if pm_dependence1 >= 0.01:
                pm_dependence1 -= 0.01
            else:
                pass

    if reward_state2 is not None:
        if reward_state2 is "positive":
            if pm_dependence2 < 1:
                pm_dependence2 += 0.01
            else:
                pass
        else:
            if pm_dependence2 >= 0.01:
                pm_dependence2 -= 0.01
            else:
                pass

    # env_noise
    env_noise_options = [((reward_step * pm_dependence) / env_noise), 1]
    env_noise = choice(env_noise_options, 1, p=[(1-rel_stability), rel_stability])


    # assign reward and factor in noise and stability suppression
    if choice_M1 == choice_P1:
        P1_cc += (reward_step * pm_dependence1) / env_noise
        P1_cd += (reward_step * pm_dependence1) / env_noise
        P1_dc += (reward_step * pm_dependence1) / env_noise
        P1_dd += (reward_step * pm_dependence1) / env_noise
        reward_state1 = "positive"
    else:
        P1_cc -= (reward_step * pm_dependence1) / env_noise
        P1_cd -= (reward_step * pm_dependence1) / env_noise
        P1_dc -= (reward_step * pm_dependence1) / env_noise
        P1_dd -= (reward_step * pm_dependence1) / env_noise
        reward_state1 = "negative"

    if choice_M2 == choice_P2:
        P2_cc += (reward_step * pm_dependence2) / env_noise
        P2_dc += (reward_step * pm_dependence2) / env_noise
        P2_cd += (reward_step * pm_dependence2) / env_noise
        P2_dd += (reward_step * pm_dependence2) / env_noise
        reward_state2 = "positive"

    else:
        P2_cc -= (reward_step * pm_dependence2) / env_noise
        P2_dc -= (reward_step * pm_dependence2) / env_noise
        P2_cd -= (reward_step * pm_dependence2) / env_noise
        P2_dd -= (reward_step * pm_dependence2) / env_noise
        reward_state2 = "negative"

    # update container variables
    container_M1.append(M1.tolist())
    container_M2.append(M2.tolist())
    container_P1.append(P1.tolist())
    container_P2.append(P2.tolist())
    container_choice_M1.append(choice_M1)
    container_choice_M2.append(choice_M2)
    container_choice_P1.append(choice_P1)
    container_choice_P2.append(choice_P2)
    container_max_master_one_utility.append(max(util_master_one))
    container_max_proxy_one_utility.append(max(util_proxy_one))
    container_stochastic_process = []  # append values generated by stochastic process
    container_stochastic_suppression = []  # append value of cooperation weight on stochastic process

