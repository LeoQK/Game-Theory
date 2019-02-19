"""

Vanilla version of the Discounted Utility Transfer Game.
The game is a meta-game that consists of two games ONE and TWO and one BROKER entity.
The mechanic of the game is the transfer of utilities from one game to the other.
The transfer goes through the broker, who applies a discount rate to the utilities. 

"""


import random
import numpy as np
from numpy.random import choice
import nashpy as nash

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
ONE_P2_transfer_storage = []

TWO_P1_EQ_utilities_storage = []
TWO_P2_EQ_utilities_storage = []
TWO_P1_EQ_choice_storage = []
TWO_P2_EQ_choice_storage = []
TWO_P1_transfer_storage = []
TWO_P2_transfer_storage = []

ONE_game_storage = []
TWO_game_storage = []

# Storage for BROKER for level of discount rate, utilities transferred and target of utility transfer
BROKER_rate_storage = []
BROKER_transfer_storage = []
BROKER_target_storage = []
Broker_utility_reserve_storage = []

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

# Memory factors MF1 and MF2 determining the utility transferred by a player based on memory of interaction with partner
MF1 = 0.1
MF2 = 0.1

# BROKER utility reserve
# Cumulative amount of utilities gained through discounting the transfer between ONE and TWO
BROKER_utility_reserve = 0

# Equilibrium ID to track which EQ is active
ONE_EQ_ID = None
TWO_EQ_ID = None

# Transfer Active ID to check whether transfer has occurred
Transfer_status = "Negative"

###########

# Main loop

###########

for i in range(10):

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
        if ONE_P1_choice == "c":
            ONE_P1_EQ_utility = ONE_P1_cc
            ONE_P2_EQ_utility = ONE_P2_cc
            ONE_EQ_ID = "cc"
        else:
            ONE_P1_EQ_utility = ONE_P1_dd
            ONE_P2_EQ_utility = ONE_P2_dd
            ONE_EQ_ID = "dd"
    else:
        if ONE_P1_choice == "c":
            ONE_P1_EQ_utility = ONE_P1_cd
            ONE_P2_EQ_utility = ONE_P2_dc
            ONE_EQ_ID = "cd"
        else:
            ONE_P1_EQ_utility = ONE_P1_dc
            ONE_P2_EQ_utility = ONE_P2_cd
            ONE_EQ_ID = "dc"

    if TWO_P1_choice == TWO_P2_choice:
        if TWO_P1_choice == "c":
            TWO_P1_EQ_utility = TWO_P1_cc
            TWO_P2_EQ_utility = TWO_P2_cc
            TWO_EQ_ID = "cc"
        else:
            TWO_P1_EQ_utility = TWO_P1_dd
            TWO_P2_EQ_utility = TWO_P2_dd
            TWO_EQ_ID = "dd"
    else:
        if TWO_P1_choice == "c":
            TWO_P1_EQ_utility = TWO_P1_cd
            TWO_P2_EQ_utility = TWO_P2_dc
            TWO_EQ_ID = "cd"
        else:
            TWO_P1_EQ_utility = TWO_P1_dc
            TWO_P2_EQ_utility = TWO_P2_cd
            TWO_EQ_ID = "dc"

    ##############################################

    # UPDATE STORAGE OF CHOICE, EQ UTILITIES, GAME

    ##############################################

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

    #############################

    # PRE-PROCESSING FOR TRANSFER

    #############################

    # Choice alignment of each pair of players P1s and P2s
    # Constitutes a complete history and partially feeds into the players' memories
    P1s_choice_alignment = []
    P2s_choice_alignment = []

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
    P1s_memory = [P1s_choice_alignment[-memory_depth:]]
    P2s_memory = [P2s_choice_alignment[-memory_depth:]]

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

    # TODO: set MF1 and MF2 back to 0 at the end of the loop

    # Calculate utility to be transferred
    # For now, the calculation is a random sample from a player's equilibrium utility weighted by the memory factor
    ONE_P1_transfer = random.uniform(0, ONE_P1_EQ_utility) * MF1
    ONE_P2_transfer = random.uniform(0, ONE_P2_EQ_utility) * MF1
    TWO_P1_transfer = random.uniform(0, TWO_P1_EQ_utility) * MF2
    TWO_P2_transfer = random.uniform(0, TWO_P2_EQ_utility) * MF2

    # Check transfer status
    # Transfer starts only after five iterations of the game have taken place
    if len(ONE_P1_EQ_choice_storage[-5:]) >= 5 is True:
        Transfer_status == "Positive"
    else:
        pass

    #######################

    # PRE-PROCESSING BROKER

    #######################

    # Discount rate
    BROKER_discount_rate = random.uniform(0, 1)

    # Application of discount rate to utility to be be transferred
    ONE_P1_transfer_discounted = ONE_P1_transfer * BROKER_discount_rate
    ONE_P2_transfer_discounted = ONE_P2_transfer * BROKER_discount_rate
    TWO_P1_transfer_discounted = TWO_P1_transfer * BROKER_discount_rate
    TWO_P2_transfer_discounted = TWO_P2_transfer * BROKER_discount_rate

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
    Broker_utility_reserve_storage.append(BROKER_utility_reserve)

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
        if len([k for k in ONE_P1_EQ_choice_storage[-5:] if k == 1]) > 2:
            ONE_P1_destination = "c"
        else:
            ONE_P1_destination = "d"

        # ONE_P2
        if len([k for k in ONE_P2_EQ_choice_storage[-5:] if k == 1]) > 2:
            ONE_P2_destination = "c"
        else:
            ONE_P2_destination = "d"

        # TWO_P1
        if len([k for k in TWO_P1_EQ_choice_storage[-5:] if k == 1]) > 2:
            TWO_P1_destination = "c"
        else:
            TWO_P1_destination = "d"

        # TWO_P2
        if len([k for k in TWO_P2_EQ_choice_storage[-5:] if k == 1]) > 2:
            TWO_P2_destination = "c"
        else:
            TWO_P2_destination = "d"
        Transfer_status = "Positive"
    else:
        pass

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

        #########################

        pass

        ###############################################

        # UPDATE STORAGE OF BROKER TRANSFER AND TARGET

        ###############################################

        pass

        ###################

        # RESET MF1 and MF2

        ###################

        MF1 = 0
        MF2 = 0
