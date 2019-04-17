### Discounted Transfer Game

The transfer game (DTG) is a game theoretical model of negotiations, specifically in their mediated form, where agents aim to find an optimal manner of conceding to their counterpart.


**Objective:** The problem that the DTG models is an optimization problem. How can I make an optimal concession to a global counterpart whose utilities I do not know and whose strategy I want to align with my own strategy, while considering that the size of concessions I can make is limited by my need to maintain a robust standing in the interaction with my local counterpart?

**Components of the DTG:** 

• Two 2x2 normal form games, ONE and TWO, with two players and two strategies

• A broker that is modeled as a mediating entity between the two games

In the DTG, each player is part of two interactions:

• A local interaction that differs by player type. This interaction is modeled as the conventional game play between a player 1 and player 2 inside each of the two games.

• A global interaction that differs by game type. This interaction is modeled inside pairs of players, where a pair compromises two players, one from each game.

### Output 

Output for the first episode of the DTG.

![](https://github.com/LeoQK/TransferGame/blob/master/docs/DTG_out_e0.JPG)

Output for the last episode of the DTG, ending after 50 runs.

![](https://github.com/LeoQK/TransferGame/blob/master/docs/final02.JPG)

### Visualization

![](https://github.com/LeoQK/TransferGame/blob/master/docs/Vis01.JPG)

![](https://github.com/LeoQK/TransferGame/blob/master/docs/Vis02.JPG)

![](https://github.com/LeoQK/TransferGame/blob/master/docs/Vis03.JPG)

![](https://github.com/LeoQK/TransferGame/blob/master/docs/Vis05.JPG)

![](https://github.com/LeoQK/TransferGame/blob/master/docs/Vis06.JPG)

![](https://github.com/LeoQK/TransferGame/blob/master/docs/Vis07.JPG)

### Specification

#### Concession/ making

The global interaction is central to the TG as it contains the transfer of utilities across games, which represents concession making.
In the TG, each player A can transfer utility to her global counterpart B in the other game to incentivize B to adopt the same strategy as A. The transfer of utilities takes place in each episode and is bidirectional for each pair of players, totaling four utility transfers per episode.

#### Concession size

The utility t that A can transfer in a given episode, or the size of her concession, is limited by the current equilibrium utility u* of A given the strategy of her local counterpart A’. Therefore, the current u* represents the player’s account.
• Example: Given the strategy a’ of A’, assume that u*(A | a’) = 3. As max(t) = u*, A can transfer no more than 3 utility to B. If A has transferred 3 and the current equilibrium does not change, she no longer has any utility to transfer to B, although she will in turn receive a utility transfer from B.
In the current specification of the TG, t is a uniform random sample from the range [0, u*].

#### Memory

In the current specification of the TG, each pair of players has a shared, binary memory that contains whether the pair’s strategies were matched (represented as a 1 in the memory) or not matched (represented as a 0 in the memory).
In the current specification, the memories of the two players in a pair is identical and extends over the past ten episodes of the game.
The memory is translated into a factor that adds an additional weight to the utility to be transferred. The factor is determined as the sum of the memory divided by the memories depth.
• Example: If, for a given episode, A in game ONE chooses <cooperate> as her equilibrium strategy a and her counterpart A’ in game TWO chooses <defect> as her equilibrium strategy a’, then as a’ != a the memory of A and A’ for this episode is represented by a 0. Over ten episodes, the memory M( A, A’) might be defined as M = [0, 1, 1, 0, 1, 0, 0, 0, 1, 0]. The memory factor then is 4/10 and hence t for (A, A’) gets multiplied by a factor of 0.4.
In the current specification of the TG, the memory is updated every episode and all the entries in the memory are weighted equally.

#### Transfer target

In the current specifications of the TG, while the concession is taken out of a specific equilibrium utility, it is assigned only to a strategy. The strategy that concessions are made on is determined by the majority strategy in the past five choices of equilibrium strategies of the player that makes the concession.

• Example: Given that the history of equilibrium choices of A over the past five rounds is <cooperate, defect, cooperate, cooperate, defect>, as n(<cooperate>) = 3 and n(<defect>) = 2, A will transfer her utility to the <cooperate> strategy of A’. The transferred utility will be divided up equally between the associated equilibria of A’ <cooperate, cooperate> and <cooperate, defect>.
In the current specification of the TG, the concessions are divided up equally between the associated equilibria and the number of past equilibrium strategies for determing the strategy on which to concede is five.
  
#### Broker

All concessions are made through a broker, who represents the mediator. The broker contains the following parameters:
• Discount rate: The broker applies a fee to each utility transfer in the form of a discount rate modeled as a uniform random sample from the range [0, 1] and through discounting the transferred utility builds up her own utility reserve. A discount rate of 0 means all the transferred utility gets routed to the broker’s reserve, a discount rate of 1 means none of the transferred utility gets routed to the reserve.

• Support requests: The broker receives requests for support in the form of utility allocation from the players. In the current setup of the TG, a request can be received if a player’s current equilibrium utility is 10% smaller than the player’s previous equilibrium utility. Once the request is received, the broker decides for each player based on a defined support rate, whether to allocate utility to the player or not. In the current specification of the TG, the support rate is 0.5. The allocation amount in each episode is determined as random sample s * 0.25 from the range [0, R], wherea R is the broker’s utility reserve in that episode and 0.25 is applied as a factor to ensure that a maximum number of four requessts can be fulfilled if s = R.
