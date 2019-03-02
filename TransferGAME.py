""""""

Vanilla version of the Discounted Utility Transfer Game.
The game is a meta-game that consists of two games ONE and TWO and one BROKER entity.
The mechanic of the game is the transfer of utilities from one game to the other.
The transfer goes through the broker, who applies a discount rate to the utilities. 

"""


import random
import numpy as np
import nashpy as nash
from numpy.random import choice
from tabulate import tabulate
from beautifultable import BeautifulTable

# The code is divided into pre-loop and main loop.

###########

# Pre-loop

###########

# Storage for ONE and TWO for utilities, equilibrium choice and utility transferred
ONE_P1_EQ_utilities_storage = []
ONE_P2_EQ_utilities_storage = []
ONE_P1_EQ_choice_storage = []
ONE_P2_EQ_choice_storage = []
ONE_P1_transfer_storage = []
ONE_P1_transfer_discounted_storage = []
ONE_P2_transfer_storage = []
ONE_P2_transfer_discounted_storage = []
ONE_P1_destination_storage = []
ONE_P2_destination_storage = []

TWO_P1_EQ_utilities_storage = []
TWO_P2_EQ_utilities_storage = []
TWO_P1_EQ_choice_storage = []
TWO_P2_EQ_choice_storage = []
TWO_P1_transfer_storage = []
TWO_P1_transfer_discounted_storage = []
TWO_P2_transfer_storage = []
TWO_P2_transfer_discounted_storage = []
TWO_P1_destination_storage = []
TWO_P2_destination_storage = []

ONE_game_storage = []
TWO_game_storage = []

# Storage for EQ_ID and equilibrium strategy selected
ONE_EQ_ID_storage = []
TWO_EQ_ID_storage = []
ONE_EQ_selected_storage = []
TWO_EQ_selected_storage = []

# Storage for BROKER for level of discount rate, utilities transferred and target of utility transfer
BROKER_rate_storage = []
BROKER_transfer_storage = []
BROKER_target_storage = []
BROKER_utility_reserve_storage = []

# Utilities for ONE and TWO
ONE_P1_cc = 2
ONE_P1_cd = 0
ONE_P1_dc = 1
ONE_P1_dd = 1

ONE_P2_cc = 2
ONE_P2_dc = 1
ONE_P2_cd = 0
ONE_P2_dd = 1

TWO_P1_cc = 3
TWO_P1_cd = 0
TWO_P1_dc = 5
TWO_P1_dd = 1

TWO_P2_cc = 3
TWO_P2_dc = 5
TWO_P2_cd = 0
TWO_P2_dd = 1

# Choice alignment between ONE_P1 - TWO_P1 and ONE_P2 - TWO_P2
P1s_choice_alignment = []
P2s_choice_alignment = []

# Memory factors MF1 and MF2 determining the utility transferred by a player based on memory of interaction with partner
MF1 = 0
MF2 = 0

# Storage of MF1 and MF2
MF1_storage = []
MF2_storage = []

# BROKER utility reserve
# Cumulative amount of utilities gained through discounting the transfer between ONE and TWO
BROKER_utility_reserve = 0

# Equilibrium ID to track which EQ is active
ONE_EQ_ID = None
TWO_EQ_ID = None

# Transfer Active ID to check whether transfer has occurred
Transfer_status = "Negative"

# Allocation_frequency to calculate amount transferred by BROKER

Allocation_frequency = 0

# Binary version of equilibrium IDs

ONE_cc_eq, ONE_cd_eq, ONE_dc_eq, ONE_dd_eq = 0, 0, 0, 0
TWO_cc_eq, TWO_cd_eq, TWO_dc_eq, TWO_dd_eq = 0, 0, 0, 0

# Equilibrium strategy profile binary
ONE_eq_strat, TWO_eq_strat = [], []

# Destinations
ONE_P1_destination, ONE_P2_destination, TWO_P1_destination, TWO_P2_destination = None, None, None, None

# BROKER SUPPORT REQUEST
ONE_P1_request, ONE_P2_request, TWO_P1_request, TWO_P2_request = None, None, None, None

# Transfer initialize as zero
ONE_P1_transfer, ONE_P2_transfer, TWO_P1_transfer, TWO_P2_transfer = 0, 0, 0, 0
ONE_P1_transfer_discounted, ONE_P2_transfer_discounted = 0, 0
TWO_P1_transfer_discounted, TWO_P2_transfer_discounted = 0, 0

# BROKER support initialize as zero
ONE_P1_broker_support, ONE_P2_broker_support, TWO_P1_broker_support, TWO_P2_broker_support = 0, 0, 0, 0

# BROKER discount rate initalize as zero
BROKER_discount_rate = 0

# BROKER transfer amount initialize as zero
BROKER_transfer_amount = 0

# BROKER allocation rate
BROKER_allocation_rate = 0

# Additional stacked variables
ONE_P1_total_requests = 0
ONE_P2_total_requests = 0
TWO_P1_total_requests = 0
TWO_P2_total_requests = 0

ONE_P1_allocation_num = 0
ONE_P2_allocation_num = 0
TWO_P1_allocation_num = 0
TWO_P2_allocation_num = 0

ONE_P1_allocated_amount = 0
ONE_P2_allocated_amount = 0
TWO_P1_allocated_amount = 0
TWO_P2_allocated_amount = 0

###########

# Main loop

###########

for i in range(50):

    ##########################

    # BASIC GAME COMPUTATIONS

    #########################

    # Load utilities
    ONE_P1_utilities = np.array([[ONE_P1_cc, ONE_P1_cd], [ONE_P1_dc, ONE_P1_dd]])
    ONE_P2_utilities = np.array([[ONE_P2_cc, ONE_P2_dc], [ONE_P2_cd, ONE_P2_dd]])
    TWO_P1_utilities = np.array([[TWO_P1_cc, TWO_P1_cd], [TWO_P1_dc, TWO_P1_dd]])
    TWO_P2_utilities = np.array([[TWO_P2_cc, TWO_P2_dc], [TWO_P2_cd, TWO_P2_dd]])

    # Build games
    ONE = nash.Game(ONE_P1_utilities, ONE_P2_utilities)
    TWO = nash.Game(TWO_P1_utilities, TWO_P2_utilities)

    # Find equilibria for each game
    ONE_EQ = ONE.vertex_enumeration()
    TWO_EQ = TWO.vertex_enumeration()

    # Transform ONE_EQ and TWO_EQ to list
    ONE_EQ_list = [eq for eq in ONE_EQ]
    TWO_EQ_list = [eq for eq in TWO_EQ]

    # Equilibrium selection
    # Note, that equilibrium selection is non-trivial, here selection is a random choice from a game's equilibria
    ONE_EQ_selected = random.choice(ONE_EQ_list)
    TWO_EQ_selected = random.choice(TWO_EQ_list)

    # Parse equilibrium choice probabilities for each player
    ONE_P1_choice_probabilities = [abs(k) for k in ONE_EQ_selected[0].tolist()]
    ONE_P2_choice_probabilities = [abs(k) for k in ONE_EQ_selected[1].tolist()]

    TWO_P1_choice_probabilities = [abs(k) for k in TWO_EQ_selected[0].tolist()]
    TWO_P2_choice_probabilities = [abs(k) for k in TWO_EQ_selected[1].tolist()]

    # Transform choice probabilities into actions
    choice_categories = ["c", "d"]

    ONE_P1_choice = choice(choice_categories, 1, p=ONE_P1_choice_probabilities).tolist()
    ONE_P2_choice = choice(choice_categories, 1, p=ONE_P2_choice_probabilities).tolist()

    TWO_P1_choice = choice(choice_categories, 1, p=TWO_P1_choice_probabilities).tolist()
    TWO_P2_choice = choice(choice_categories, 1, p=TWO_P2_choice_probabilities).tolist()

    # Compute equilibrium utilities and identify EQ

    if ONE_P1_choice == ONE_P2_choice:
        if ONE_P1_choice == ["c"]:
            ONE_P1_EQ_utility = ONE_P1_cc
            ONE_P2_EQ_utility = ONE_P2_cc
            ONE_EQ_ID = "cc"
        else:
            ONE_P1_EQ_utility = ONE_P1_dd
            ONE_P2_EQ_utility = ONE_P2_dd
            ONE_EQ_ID = "dd"
    else:
        if ONE_P1_choice == ["c"]:
            ONE_P1_EQ_utility = ONE_P1_cd
            ONE_P2_EQ_utility = ONE_P2_dc
            ONE_EQ_ID = "cd"
        else:
            ONE_P1_EQ_utility = ONE_P1_dc
            ONE_P2_EQ_utility = ONE_P2_cd
            ONE_EQ_ID = "dc"

    if TWO_P1_choice == TWO_P2_choice:
        if TWO_P1_choice == ["c"]:
            TWO_P1_EQ_utility = TWO_P1_cc
            TWO_P2_EQ_utility = TWO_P2_cc
            TWO_EQ_ID = "cc"
        else:
            TWO_P1_EQ_utility = TWO_P1_dd
            TWO_P2_EQ_utility = TWO_P2_dd
            TWO_EQ_ID = "dd"
    else:
        if TWO_P1_choice == ["c"]:
            TWO_P1_EQ_utility = TWO_P1_cd
            TWO_P2_EQ_utility = TWO_P2_dc
            TWO_EQ_ID = "cd"
        else:
            TWO_P1_EQ_utility = TWO_P1_dc
            TWO_P2_EQ_utility = TWO_P2_cd
            TWO_EQ_ID = "dc"

    ##################################################################

    # UPDATE STORAGE OF CHOICE, EQ UTILITIES, GAME, EQ_ID, EQ_SELECTED

    ##################################################################

    # Update choice storage variables
    ONE_P1_EQ_choice_storage.append(ONE_P1_choice)
    ONE_P2_EQ_choice_storage.append(ONE_P2_choice)
    TWO_P1_EQ_choice_storage.append(TWO_P1_choice)
    TWO_P2_EQ_choice_storage.append(TWO_P2_choice)

    # Update EQ utilities storage variable
    ONE_P1_EQ_utilities_storage.append(ONE_P1_EQ_utility)
    ONE_P2_EQ_utilities_storage.append(ONE_P2_EQ_utility)
    TWO_P1_EQ_utilities_storage.append(TWO_P1_EQ_utility)
    TWO_P2_EQ_utilities_storage.append(TWO_P2_EQ_utility)

    # Update game storage variables
    ONE_game_storage.append(ONE)
    TWO_game_storage.append(TWO)

    # Update EQ_ID storage variables
    ONE_EQ_ID_storage.append(ONE_EQ_ID)
    TWO_EQ_ID_storage.append(TWO_EQ_ID)

    # Update EQ_selected storage variables
    ONE_EQ_selected_storage.append(ONE_EQ_selected)
    TWO_EQ_selected_storage.append(TWO_EQ_selected)

    #############################

    # PRE-PROCESSING FOR TRANSFER

    #############################

    # Choice alignment of each pair of players P1s and P2s
    # Constitutes a complete history and partially feeds into the players' memories

    if ONE_P1_EQ_choice_storage[-1] == TWO_P1_EQ_choice_storage[-1]:
        P1s_choice_alignment.append(1)
    else:
        P1s_choice_alignment.append(0)

    if ONE_P2_EQ_choice_storage[-1] == TWO_P2_EQ_choice_storage[-1]:
        P2s_choice_alignment.append(1)
    else:
        P2s_choice_alignment.append(0)

    # Memory of each pair of players P1s and P2s
    memory_depth = 10
    P1s_memory = P1s_choice_alignment[-memory_depth:]
    P2s_memory = P2s_choice_alignment[-memory_depth:]

    # Memory factors MF1 and MF2
    # Between 0 and 1 and weights the utility to be transferred
    for memory in P1s_memory:
        if memory == 1:
            MF1 += 0.1
        else:
            pass
    for memory in P2s_memory:
        if memory == 1:
            MF2 += 0.1
        else:
            pass
    # print("MF1", "i =", i, MF1, P1s_memory)
    # print("MF2", "i =", i, MF2, P2s_memory)

    # Check transfer status
    # Transfer starts only after five iterations of the game have taken place
    if len(ONE_P1_EQ_choice_storage[-5:]) >= 5:
        Transfer_status = "Positive"
    else:
        pass
    if Transfer_status == "Positive":
        # Calculate utility to be transferred
        # For now, the calculation is a random sample from a player's equilibrium utility weighted by the memory factor
        ONE_P1_transfer = random.uniform(0, ONE_P1_EQ_utility) * MF1
        ONE_P2_transfer = random.uniform(0, ONE_P2_EQ_utility) * MF1
        TWO_P1_transfer = random.uniform(0, TWO_P1_EQ_utility) * MF2
        TWO_P2_transfer = random.uniform(0, TWO_P2_EQ_utility) * MF2

        ##########################

        # UPDATE TRANSFER STORAGE

        ##########################
        ONE_P1_transfer_storage.append(ONE_P1_transfer)
        ONE_P2_transfer_storage.append(ONE_P2_transfer)
        TWO_P1_transfer_storage.append(TWO_P1_transfer)
        TWO_P2_transfer_storage.append(TWO_P2_transfer)


    ###############################

    # UPDATE STORAGE OF MF1 and MF2

    ###############################

    MF1_storage.append(MF1)
    MF2_storage.append(MF2)

    #######################

    # PRE-PROCESSING BROKER

    #######################
    if Transfer_status == "Positive":

        # Discount rate
        BROKER_discount_rate = random.uniform(0, 1)

        # Application of discount rate to utility to be be transferred
        ONE_P1_transfer_discounted = ONE_P1_transfer * BROKER_discount_rate
        ONE_P2_transfer_discounted = ONE_P2_transfer * BROKER_discount_rate
        TWO_P1_transfer_discounted = TWO_P1_transfer * BROKER_discount_rate
        TWO_P2_transfer_discounted = TWO_P2_transfer * BROKER_discount_rate

        #######################

        # UPDATE DISCOUNTED TRANSFER STORAGE

        #######################

        ONE_P1_transfer_discounted_storage.append(ONE_P1_transfer_discounted)
        ONE_P2_transfer_discounted_storage.append(ONE_P2_transfer_discounted)
        TWO_P1_transfer_discounted_storage.append(TWO_P1_transfer_discounted)
        TWO_P2_transfer_discounted_storage.append(TWO_P2_transfer_discounted)

    if Transfer_status == "Positive":
        # BROKER utility accumulation as subtraction of transfer_discounted from transfer
        BROKER_utility_reserve += ONE_P1_transfer - ONE_P1_transfer_discounted
        BROKER_utility_reserve += ONE_P2_transfer - ONE_P2_transfer_discounted
        BROKER_utility_reserve += TWO_P1_transfer - TWO_P1_transfer_discounted
        BROKER_utility_reserve += TWO_P2_transfer - TWO_P2_transfer_discounted

        ###########################################

        # UPDATE STORAGE OF BROKER RATE AND RESERVE

        ###########################################

        BROKER_rate_storage.append(BROKER_discount_rate)

    ########################

    # TRANSFER GAME TO GAME

    ########################

    # Point of origin computations = subtract utility to be transferred from equilibrium utility for each player
    # Transfer starts only after five iterations of the game have taken place
    # ONE
    if Transfer_status == "Positive":
        if ONE_EQ_ID == "cc":
            ONE_P1_cc -= ONE_P1_transfer_discounted
            ONE_P2_cc -= ONE_P2_transfer_discounted
        elif ONE_EQ_ID == "dd":
            ONE_P1_dd -= ONE_P1_transfer_discounted
            ONE_P2_dd -= ONE_P2_transfer_discounted
        elif ONE_EQ_ID == "cd":
            ONE_P1_cd -= ONE_P1_transfer_discounted
            ONE_P2_dc -= ONE_P2_transfer_discounted
        else:
            ONE_P1_dc -= ONE_P1_transfer_discounted
            ONE_P2_cd -= ONE_P2_transfer_discounted

        # TWO
        if TWO_EQ_ID == "cc":
            TWO_P1_cc -= TWO_P1_transfer_discounted
            TWO_P2_cc -= TWO_P2_transfer_discounted
        elif TWO_EQ_ID == "dd":
            TWO_P1_dd -= TWO_P1_transfer_discounted
            TWO_P2_dd -= TWO_P2_transfer_discounted
        elif TWO_EQ_ID == "cd":
            TWO_P1_cd -= TWO_P1_transfer_discounted
            TWO_P2_dc -= TWO_P2_transfer_discounted
        else:
            TWO_P1_dc -= TWO_P1_transfer_discounted
            TWO_P2_cd -= TWO_P2_transfer_discounted

    # Point of destination
    # (1) Define strategy to which utility is transferred based on senders last five choices
    # (2) Divide utility transferred over the outcomes associated with the selected strategy

    # (1)
    # Transfer starts only after five iterations of the game have taken place
    # ONE_P1

    if Transfer_status == "Positive":
        if len([k for k in ONE_P1_EQ_choice_storage[-5:] if k == ["c"]]) > 2:
            ONE_P1_destination = "c"
        else:
            ONE_P1_destination = "d"

        # ONE_P2
        if len([k for k in ONE_P2_EQ_choice_storage[-5:] if k == ["c"]]) > 2:
            ONE_P2_destination = "c"
        else:
            ONE_P2_destination = "d"

        # TWO_P1
        if len([k for k in TWO_P1_EQ_choice_storage[-5:] if k == ["c"]]) > 2:
            TWO_P1_destination = "c"
        else:
            TWO_P1_destination = "d"

        # TWO_P2
        if len([k for k in TWO_P2_EQ_choice_storage[-5:] if k == ["c"]]) > 2:
            TWO_P2_destination = "c"
        else:
            TWO_P2_destination = "d"
    else:
        pass

    # Update destination storage variables
    #     ONE_P1_destination_storage.append(ONE_P1_destination)
    #     ONE_P2_destination_storage.append(ONE_P2_destination)
    #     TWO_P1_destination_storage.append(TWO_P1_destination)
    #     TWO_P2_destination_storage.append(TWO_P2_destination)

    # (2)
    # Allocation of transfers as even split of transfer across both outcomes aligned with strategy
    if Transfer_status == "Positive":
        # ONE
        # Transfer from ONE_P1 to TWO_P1
        if ONE_P1_destination == "c":
            TWO_P1_cc += ONE_P1_transfer_discounted / 2
            TWO_P1_cd += ONE_P1_transfer_discounted / 2
        else:
            TWO_P1_cc += ONE_P1_transfer_discounted / 2
            TWO_P1_cd += ONE_P1_transfer_discounted / 2

        # Transfer from ONE_P2 to TWO_P2
        if ONE_P2_destination == "c":
            TWO_P2_cc += ONE_P2_transfer_discounted / 2
            TWO_P2_cd += ONE_P2_transfer_discounted / 2
        else:
            TWO_P2_cc += ONE_P2_transfer_discounted / 2
            TWO_P2_cd += ONE_P2_transfer_discounted / 2

        # TWO
        # Transfer from TWO_P1 to ONE_P1
        if TWO_P1_destination == "c":
            ONE_P1_cc += TWO_P1_transfer_discounted / 2
            ONE_P1_cd += TWO_P1_transfer_discounted / 2
        else:
            ONE_P1_cc += TWO_P1_transfer_discounted / 2
            ONE_P1_cd += TWO_P1_transfer_discounted / 2

        # Transfer from TWO_P2 to OE_P2
        if TWO_P2_destination == "c":
            ONE_P2_cc += ONE_P2_transfer_discounted / 2
            ONE_P2_cd += ONE_P2_transfer_discounted / 2
        else:
            ONE_P2_cc += ONE_P2_transfer_discounted / 2
            ONE_P2_cd += ONE_P2_transfer_discounted / 2

        ##########################

        # TRANSFER BROKER TO GAME

        ##########################

    # Check who of the players needs mediation based on utility decreases in current period larger than the utility of
    # previous period divided by 2

    if Transfer_status == "Positive":
        if (ONE_P1_EQ_utilities_storage[-2] - ONE_P1_EQ_utilities_storage[-1]) > (ONE_P1_EQ_utilities_storage[-2] / 10):
            ONE_P1_request = "yes"
            ONE_P1_total_requests += 1
        else:
            ONE_P1_request = "no"

        if (ONE_P2_EQ_utilities_storage[-2] - ONE_P2_EQ_utilities_storage[-1]) > (ONE_P2_EQ_utilities_storage[-2] / 10):
            ONE_P2_request = "yes"
            ONE_P2_total_requests += 1
        else:
            ONE_P2_request = "no"

        if (TWO_P1_EQ_utilities_storage[-2] - TWO_P1_EQ_utilities_storage[-1]) > (TWO_P1_EQ_utilities_storage[-2] / 10):
            TWO_P1_request = "yes"
            TWO_P1_total_requests += 1
        else:
            TWO_P1_request = "no"

        if (TWO_P2_EQ_utilities_storage[-2] - TWO_P2_EQ_utilities_storage[-1]) > (TWO_P2_EQ_utilities_storage[-2] / 10):
            TWO_P2_request = "yes"
            TWO_P2_total_requests += 1
        else:
            TWO_P2_request = "no"

        # BROKER allocation rate, defining probability of allocating v. not allocating is request == need

        BROKER_allocation_rate = 0.5

        BROKER_choice_distribution = [BROKER_allocation_rate, (1 - BROKER_allocation_rate)]

        # BROKER transfer choice categories

        BROKER_choice_categories = ["allocate", "pass"]

        # BROKER Transfer amount

        BROKER_transfer_amount = random.uniform(0, BROKER_utility_reserve / 4)

        # BROKER transfer enhances equilibrium position

        if ONE_P1_request == "yes":
            BROKER_choice = choice(BROKER_choice_categories, p=BROKER_choice_distribution)
            if BROKER_choice == "allocate":
                if ONE_P1_EQ_choice_storage[-1] == "c" and ONE_P2_EQ_choice_storage[-1] == "c":
                    ONE_P1_cc += BROKER_transfer_amount
                elif ONE_P1_EQ_choice_storage[-1] == "c" and ONE_P2_EQ_choice_storage[-1] == "d":
                    ONE_P1_cd += BROKER_transfer_amount
                elif ONE_P1_EQ_choice_storage[-1] == "d" and ONE_P2_EQ_choice_storage[-1] == "c":
                    ONE_P1_dc += BROKER_transfer_amount
                elif ONE_P1_EQ_choice_storage[-1] == "d" and ONE_P2_EQ_choice_storage[-1] == "d":
                    ONE_P1_dd += BROKER_transfer_amount
                Allocation_frequency += 1
                ONE_P1_broker_support = BROKER_transfer_amount
                ONE_P1_allocation_num += 1
                ONE_P1_allocated_amount += BROKER_transfer_amount
            else:
                pass
                ONE_P1_broker_support = 0

        if ONE_P2_request == "yes":
            BROKER_choice = choice(BROKER_choice_categories, p=BROKER_choice_distribution)
            if BROKER_choice == "allocate":
                if ONE_P1_EQ_choice_storage[-1] == "c" and ONE_P2_EQ_choice_storage[-1] == "c":
                    ONE_P2_cc += BROKER_transfer_amount
                elif ONE_P1_EQ_choice_storage[-1] == "c" and ONE_P2_EQ_choice_storage[-1] == "d":
                    ONE_P2_cd += BROKER_transfer_amount
                elif ONE_P1_EQ_choice_storage[-1] == "d" and ONE_P2_EQ_choice_storage[-1] == "c":
                    ONE_P2_dc += BROKER_transfer_amount
                else:
                    ONE_P2_dd += BROKER_transfer_amount
                Allocation_frequency += 1
                ONE_P2_broker_support = BROKER_transfer_amount
                ONE_P2_allocation_num += 1
                ONE_P2_allocated_amount += BROKER_transfer_amount
            else:
                pass
                ONE_P2_broker_support = 0

        if TWO_P1_request == "yes":
            BROKER_choice = choice(BROKER_choice_categories, p=BROKER_choice_distribution)
            if BROKER_choice == "allocate":
                if TWO_P1_EQ_choice_storage[-1] == "c" and TWO_P2_EQ_choice_storage[-1] == "c":
                    TWO_P1_cc += BROKER_transfer_amount
                elif TWO_P1_EQ_choice_storage[-1] == "c" and TWO_P2_EQ_choice_storage[-1] == "d":
                    TWO_P1_cd += BROKER_transfer_amount
                elif TWO_P1_EQ_choice_storage[-1] == "d" and TWO_P2_EQ_choice_storage[-1] == "c":
                    TWO_P1_dc += BROKER_transfer_amount
                else:
                    TWO_P1_dd += BROKER_transfer_amount
                Allocation_frequency += 1
                TWO_P1_broker_support = BROKER_transfer_amount
                TWO_P1_allocation_num += 1
                TWO_P1_allocated_amount += BROKER_transfer_amount
            else:
                pass
                TWO_P1_broker_support = 0

        if TWO_P2_request == "yes":
            BROKER_choice = choice(BROKER_choice_categories, p=BROKER_choice_distribution)
            if BROKER_choice == "allocate":
                if TWO_P1_EQ_choice_storage[-1] == "c" and TWO_P2_EQ_choice_storage[-1] == "c":
                    TWO_P2_cc += BROKER_transfer_amount
                elif TWO_P1_EQ_choice_storage[-1] == "c" and TWO_P2_EQ_choice_storage[-1] == "d":
                    TWO_P2_cd += BROKER_transfer_amount
                elif TWO_P1_EQ_choice_storage[-1] == "d" and TWO_P2_EQ_choice_storage[-1] == "c":
                    TWO_P2_dc += BROKER_transfer_amount
                else:
                    TWO_P2_dd += BROKER_transfer_amount
                Allocation_frequency += 1
                TWO_P2_broker_support = BROKER_transfer_amount
                TWO_P2_allocation_num += 1
                TWO_P2_allocated_amount += BROKER_transfer_amount
            else:
                pass
                TWO_P2_broker_support = 0

        # Subtract allocated transfers from BROKER_utility_reserve

        BROKER_utility_reserve -= Allocation_frequency * BROKER_transfer_amount

        ###############################################

        # UPDATE STORAGE OF BROKER TRANSFER AND TARGET

        ###############################################

        # TODO: check indent

        # Update BROKER transfer storage

        BROKER_transfer_storage.append(Allocation_frequency * BROKER_transfer_amount)

        # Update BROKER utility reserve storage
        BROKER_utility_reserve_storage.append(BROKER_utility_reserve)
        # print(BROKER_utility_reserve_storage[-1])

    ##############

    # PRINT TABLES

    ##############


    # Pre-processing - binary transformation of equilibrium ID


    if ONE_EQ_selected[0][0] != 0 and ONE_EQ_selected[0][0] != 1:
        ONE_eq_strat.append("mixed")
    else:
        ONE_eq_strat.append("pure")
    if ONE_EQ_selected[1][0] != 0 and ONE_EQ_selected[1][0] != 1:
        ONE_eq_strat.append("mixed")
    else:
        ONE_eq_strat.append("pure")

    if TWO_EQ_selected[0][0] != 0 and TWO_EQ_selected[0][0] != 1:
        TWO_eq_strat.append("mixed")
    else:
        TWO_eq_strat.append("pure")
    if ONE_EQ_selected[1][0] != 0 and ONE_EQ_selected[1][0] != 1:
        TWO_eq_strat.append("mixed")
    else:
        TWO_eq_strat.append("pure")

    print("---------------------------------START EPISODE", i, "-------------------------------")

    # Game statistics

    game_table = BeautifulTable()
    game_table.column_headers = ["", "GAME ONE", "GAME TWO"]
    game_table.append_row(["cc", (round(ONE_P1_cc, 2), round(ONE_P2_cc, 2)),(round(TWO_P1_cc, 2), round(TWO_P2_cc, 2))])
    game_table.append_row(["cd", (round(ONE_P1_cd, 2), round(ONE_P2_dc, 2)),(round(TWO_P1_cd, 2), round(TWO_P2_dc, 2))])
    game_table.append_row(["dc", (round(ONE_P1_dc, 2), round(ONE_P2_cd, 2)),(round(TWO_P1_dc, 2), round(TWO_P2_cd, 2))])
    game_table.append_row(["dd", (round(ONE_P1_dd, 2), round(ONE_P2_dd, 2)),(round(TWO_P1_dd, 2), round(TWO_P2_dd, 2))])
    game_table.append_row(["Nash EQ", ONE_EQ_ID, TWO_EQ_ID])
    game_table.append_row(["EQ strategies", (ONE_eq_strat), TWO_eq_strat])
    print(game_table)

    print("")

    # Player statistics

    player_table = BeautifulTable()
    player_table.column_headers = ["", "ONE PLAYER 1", "ONE PLAYER 2", "TWO PLAYER 1", "TWO PLAYER 2"]
    player_table.append_row(["Memory factor", MF1, MF2, MF1, MF2])
    player_table.append_row(["Transfer outflow", -round(ONE_P1_transfer, 2), -round(ONE_P2_transfer, 2),
                             -round(TWO_P1_transfer, 2), -round(TWO_P2_transfer, 2)])
    player_table.append_row(["Outflow target", ONE_P1_destination, ONE_P2_destination, TWO_P1_destination,
                             TWO_P2_destination])
    player_table.append_row(["Transfer inflow", round(TWO_P1_transfer_discounted, 2), round(TWO_P2_transfer_discounted, 2),
                             round(ONE_P1_transfer_discounted, 2), round(ONE_P2_transfer_discounted, 2)])
    player_table.append_row(["Transfer balance", round(TWO_P1_transfer_discounted - ONE_P1_transfer, 2),
                             round(TWO_P2_transfer_discounted - ONE_P2_transfer, 2),
                             round(ONE_P1_transfer_discounted - TWO_P1_transfer, 2),
                             round(ONE_P2_transfer_discounted - TWO_P2_transfer, 2)])
    player_table.append_row(["Support request", ONE_P1_request, ONE_P2_request, TWO_P1_request, TWO_P2_request])
    player_table.append_row(["Support amount", round(ONE_P1_broker_support, 2), round(ONE_P2_broker_support, 2),
                             round(TWO_P1_broker_support, 2), round(TWO_P2_broker_support, 2)])
    print(player_table)

    # Broker statistics

    num_requests = len([k for k in [ONE_P1_request, ONE_P2_request, TWO_P1_request, TWO_P1_request] if k == "yes"])
    num_responses = len([k for k in [ONE_P1_broker_support, ONE_P2_broker_support, TWO_P1_broker_support, TWO_P2_broker_support]
                         if k > 0])
    if num_requests > 0:
        support_ratio = (num_responses / num_requests)
    else:
        support_ratio = 0

    broker_inflows = ONE_P1_transfer - ONE_P1_transfer_discounted + ONE_P2_transfer - ONE_P2_transfer_discounted + \
                     TWO_P1_transfer - TWO_P1_transfer_discounted + TWO_P2_transfer - TWO_P2_transfer_discounted


    broker_table = BeautifulTable()
    broker_table.column_headers = ["", "BROKER"]
    broker_table.append_row(["Allocation inflow", round(broker_inflows, 2)])
    broker_table.append_row(["Discount rate", round(BROKER_discount_rate, 2)])
    broker_table.append_row(["Allocation outflow", round(-Allocation_frequency * BROKER_transfer_amount, 2)])
    broker_table.append_row(["Support amount", round(BROKER_transfer_amount, 2)])
    broker_table.append_row(["Support requests", num_requests])
    broker_table.append_row(["Defined support rate", round(BROKER_allocation_rate, 2)])
    broker_table.append_row(["Actual support rate", support_ratio])
    broker_table.append_row(["Allocation balance", round(broker_inflows - (Allocation_frequency * BROKER_transfer_amount), 2)])
    broker_table.append_row(["Reserve", round(BROKER_utility_reserve, 2)])
    print(broker_table)

    print("----------------------------------END EPISODE", i, "--------------------------------")
    print("")


    #############################################################################################################

    # RESET MF1 AND MF2, ALLOCATION FREQUENCY, BINARY EQ IDS, BINARY EQ STRATEGIES AND BROKER SUPPORT FOR PLAYERS

    #############################################################################################################

    MF1 = 0
    MF2 = 0
    Allocation_frequency = 0
    ONE_cc_eq, ONE_cd_eq, ONE_dc_eq, ONE_dd_eq = 0, 0, 0, 0
    TWO_cc_eq, TWO_cd_eq, TWO_dc_eq, TWO_dd_eq = 0, 0, 0, 0
    ONE_eq_strat, TWO_eq_strat = [], []
    ONE_P1_broker_support, ONE_P2_broker_support, TWO_P1_broker_support, TWO_P2_broker_support = 0, 0, 0, 0

print("TRANSFER GAME COMPLETED. NUMBER OF EPISODES:", i)

ONE_P1_transfer_balance = round((sum(TWO_P1_transfer_discounted_storage) - sum(ONE_P1_transfer_storage)), 2)
ONE_P2_transfer_balance = round((sum(TWO_P2_transfer_discounted_storage) - sum(ONE_P2_transfer_storage)), 2)
TWO_P1_transfer_balance = round((sum(ONE_P1_transfer_discounted_storage) - sum(TWO_P1_transfer_storage)), 2)
TWO_P2_transfer_balance = round((sum(ONE_P2_transfer_discounted_storage) - sum(TWO_P2_transfer_storage)), 2)

print("")
final_table = BeautifulTable()
final_table.column_headers = ["CUMULATIVE", "UTILITIES", "BALANCE", "REQS", "ALLOCATIONS", "AMOUNT"]
final_table.append_row(["ONE P1", round(sum(ONE_P1_EQ_utilities_storage), 2), ONE_P1_transfer_balance,
                        ONE_P1_total_requests, ONE_P1_allocation_num, ONE_P1_allocated_amount])
final_table.append_row(["ONE P2", round(sum(ONE_P2_EQ_utilities_storage), 2), ONE_P2_transfer_balance,
                        ONE_P2_total_requests, ONE_P2_allocation_num, ONE_P2_allocated_amount])
final_table.append_row(["TWO P1", round(sum(TWO_P1_EQ_utilities_storage), 2), TWO_P1_transfer_balance,
                        TWO_P1_total_requests, TWO_P1_allocation_num, TWO_P1_allocated_amount])
final_table.append_row(["TWO P2", round(sum(TWO_P2_EQ_utilities_storage), 2), TWO_P2_transfer_balance,
                        TWO_P2_total_requests, TWO_P2_allocation_num, TWO_P2_allocated_amount])
print(final_table)

average_discount_rate = (sum(BROKER_rate_storage) / len(BROKER_rate_storage))

print("")
broker_final_table = BeautifulTable()
broker_final_table.column_headers = ["", "AVG. DIS. RATE"]
broker_final_table.append_row(["BROKER", average_discount_rate])
print(broker_final_table)



