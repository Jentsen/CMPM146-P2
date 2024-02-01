# CMPM 146 P2: Monte Carlo Tree Search
# Team: Jentsen Maniti

### Requirements
●	Implement mcts_vanilla.py that uses MCTS with a full, random rollout. mcts_vanilla must beat rollout_bot most of the time. 
mcts_vanilla 1000 nodes vs rollout_bot:
The 1 bot wins this round! ({1: 1, 2: -1})

Final win counts: {'draw': 0, 1: 86, 2: 14}
723.977974599984  seconds

●	Using your existing implementation from mcts_vanilla.py as base code, implement mcts_modified.py with the addition of your own heuristic rollout strategy as an improvement over vanilla MCTS. Optional: You may also adjust other aspects of the tree search, by implementing the variations discussed in class (roulette selection, partial expansion, etc).

See below.

●	Perform the two experiments described below.

See experiment1.pdf and experiment2.pdf for details on the experiments.

### Modifications to mcts_modified.py:
In the modified version, I incorporated a heuristic rollout strategy and replaced the selection step with roulette wheel selection. 
These modifications aim to improve the efficiency and effectiveness of the MCTS algorithm.
