
from mcts_node import MCTSNode
from p2_t3 import Board
from random import choice
from math import sqrt, log

num_nodes = 100
explore_faction = 2.

def traverse_nodes(node: MCTSNode, board: Board, state, bot_identity: int):
    """ Traverses the tree until the end criterion are met.
    e.g. find the best expandable node (node with untried action) if it exist,
    or else a terminal node

    Args:
        node:       A tree node from which the search is traversing.
        board:      The game setup.
        state:      The state of the game.
        identity:   The bot's identity, either 1 or 2

    Returns:
        node: A node from which the next stage of the search can proceed.
        state: The state associated with that node

    """
    while not board.is_ended(state) and node.untried_actions == []:
        if node.child_nodes == {} or all(child.visits == 0 for child in node.child_nodes.values()):
            return node, state
        else:
            # Select the child node with the highest UCB value
            node = max(node.child_nodes.values(), key=lambda x: ucb(x, bot_identity))
            action = node.parent_action
            state = board.next_state(state, action)

    return node, state



def expand_leaf(node: MCTSNode, board: Board, state):
    """ Adds a new leaf to the tree by creating a new child node for the given node (if it is non-terminal).

    Args:
        node:   The node for which a child will be added.
        board:  The game setup.
        state:  The state of the game.

    Returns:
        node:  The added child node.
        state: The state associated with that node.

    """
    if node.untried_actions:
        # Choose an untried action
        action = choice(node.untried_actions)
        node.untried_actions.remove(action)
        
        # Apply the action to the current state
        new_state = board.next_state(state, action)
        
        # Create a new child node
        child_node = MCTSNode(parent=node, parent_action=action, action_list=board.legal_actions(new_state))
        
        # Update the tree
        node.child_nodes[action] = child_node
        
        return child_node, new_state

    return node, state


def rollout(board: Board, state):
    """ Given the state of the game, the rollout plays out the remainder randomly.

    Args:
        board: The game setup.
        state: The state of the game.
    
    Returns:
        state: The terminal game state.

    """
    while not board.is_ended(state):
        legal_actions = board.legal_actions(state)
        action = choice(legal_actions)
        state = board.next_state(state, action)

    return state

def backpropagate(node: MCTSNode, won: bool):
    """ Navigates the tree from a leaf node to the root, updating the win and visit count of each node along the path.

    Args:
        node: A leaf node.
        won:  An indicator of whether the bot won or lost the game.

    """
    while node is not None:
        node.visits += 1
        if won:
            node.wins += 1
        node = node.parent

def ucb(node: MCTSNode, bot_identity: int):
    """ Calculates the UCB value for the given node from the perspective of the bot.

    Args:
        node:         A node.
        bot_identity: The bot's identity, either 1 or 2.

    Returns:
        The value of the UCB function for the given node.
    """
    if node.visits == 0:
        return float('inf')
    exploitation = node.wins / node.visits
    exploration = explore_faction * sqrt(log(node.parent.visits) / node.visits)
    return exploitation + exploration if bot_identity == 1 else -exploitation + exploration


def get_best_action(root_node: MCTSNode):
    """ Selects the best action from the root node in the MCTS tree.

    Args:
        root_node: The root node.

    Returns:
        action: The best action from the root node.
    
    """
    if not root_node.child_nodes:
        return None
    return max(root_node.child_nodes.keys(), key=lambda x: root_node.child_nodes[x].visits)


def is_win(board: Board, state, identity_of_bot: int):
    # checks if state is a win state for identity_of_bot
    outcome = board.points_values(state)
    assert outcome is not None, "is_win was called on a non-terminal state"
    return outcome[identity_of_bot] == 1

def think(board: Board, current_state):
    """ Performs MCTS by sampling games and calling the appropriate functions to construct the game tree.

    Args:
        board:  The game setup.
        current_state:  The current state of the game.

    Returns:    The action to be taken from the current state

    """
    bot_identity = board.current_player(current_state) # 1 or 2
    root_node = MCTSNode(parent=None, parent_action=None, action_list=board.legal_actions(current_state))

    for _ in range(num_nodes):
        state = current_state
        node = root_node

        # Do MCTS - This is all you!
        # Traverse nodes until a leaf node is reached
        node, state = traverse_nodes(node, board, state, bot_identity)

        # Expand the leaf node if it is non-terminal
        node, state = expand_leaf(node, board, state)

        # Perform a rollout from the leaf node
        result_state = rollout(board, state)

        # Determine if the bot won the game
        won = is_win(board, result_state, bot_identity)

        # Backpropagate the result
        backpropagate(node, won)


    # Return an action, typically the most frequently used action (from the root) or the action with the best
    # estimated win rate.
    best_action = get_best_action(root_node)
    
    print(f"Action chosen: {best_action}")
    return best_action
