from tokenize import String
import numpy as np
from typing import Tuple, List

class Node:
    state: list(str)
    parent: "Node"
    children: list("Node")
    hour: int
    letter: str
    score: int = 0
    N: int = 0
class Tree:
    def __init__(self, root: "Node"):
        self.nodes = {root.state.tobytes(): root}
        self.size = 1
    def add(self, node = "Node"):
        self.nodes[node.state.tobytes()] = node
        parent = tree.get(node.parent)
        parent.children.append(node)
        self.size += 1
    def get(self, state: list[str]):
        flat_state = state.tobytes()
        if flat_state not in self.nodes:
            return None
        return self.nodes[flat_state]

class Player:
    def __init__(self, rng: np.random.Generator) -> None:
        """Initialise the player with given skill.

        Args:
            skill (int): skill of your player
            rng (np.random.Generator): numpy random number generator, use this for same player behvior across run
            logger (logging.Logger): logger use this like logger.info("message")
            golf_map (sympy.Polygon): Golf Map polygon
            start (sympy.geometry.Point2D): Start location
            target (sympy.geometry.Point2D): Target location
            map_path (str): File path to map
            precomp_dir (str): Directory path to store/load precomputation
        """
        self.rng = rng

    # def choose_discard(self, cards: list[str], constraints: list[str]):
    def choose_discard(self, cards, constraints):
        """Function in which we choose which cards to discard, and it also inititalises the cards dealt to the player at the game beginning

        Args:
            cards(list): A list of letters you have been given at the beginning of the game.
            constraints(list(str)): The total constraints assigned to the given player in the format ["A<B<V","S<D","F<G<A"].

        Returns:
            list[int]: Return the list of constraint cards that you wish to keep. (can look at the default player logic to understand.)
        """
        final_constraints = []
        # print(constraints)

        for i in range(len(constraints)):
            if self.rng.random() <= 0.5:
                final_constraints.append(constraints[i])
        return final_constraints

    def risky_versus_safe():
        pass

    def MCTS(cards: list[str], constraints: list[str], state: list[str], territory: list[int], rollouts: int = 50000):
        # MCTS main loop: Execute MCTS steps rollouts number of times
        # Then return successor with highest number of rollouts
        tree = Tree(Node(state, None, children=[], 24, 'Z', 0, 1))
        tree = expand(tree, cards, state)
        available_letters = [] # append all the letters that have not been played yet
        
        for i range(rollouts):
            move = select(tree, state, alpha)
            tree = simulate(tree, move, constraints, available_letters)

        nxt = None
        plays = 0
        
        for succ in tree.root.children:
            if succ.N > plays:
                plays = succ.N
                nxt = succ
        return succ

    def select(tree: "Tree", state: list[str], alpha: float = 1):
    """Starting from state, move to child node with the
    highest UCT value.

    Args:
        tree ("Tree"): the search tree
        state (list[str]): the clock game state
        alpha (float): exploration parameter [PERHAPS THIS CAN BE DETERMINED IN RISKY_VS_SAFE()?]
    Returns:
        state: the clock game state after best UCT move
    """

    cur_node = tree.get(state)
    max_UCT = 0.0
    move = state

    for child_state in root.children:
        node_UCT = (child_state.score/child_state.N + alpha*numpy.sqrt(root.N/child_state.N))
        if node_UCT > max_UCT:
            max_UCT = node_UCT
            move = child_state
            
    return move
    
    def expand(tree: "Tree", cards: list[str], state: list[str]):
        """Add all children nodes of state into the tree and return
        tree.

        Args:
            tree ("Tree"): the search tree
            cards (list[str]): cards from our player
            state (list[str]): the clock game state
        Returns:
            "Tree": the tree after insertion
        """
        
        for letter in cards:
            # add our letters in every hour available
            for i in range (0,12):
                new_state = np.copy(state)
                if state[i] == 'Z':
                    new_state[i] = letter
                elif new_state[i+12] == 'Z':
                    # if hour already occupied, try index + 12
                    new_state[i+12] = letter
                else:
                    # if both slots of hour already occupied, continue
                    continue
            hour = 12 if i = 0 else i
            tree.add(Node(new_state, root, children=[], hour, letter, 0, 1))
        return tree

    
    def simulate(tree: "Tree", state: list[str], constraints: list[str], remaining_cards):
        """Run one game rollout from state to a terminal state using random
        playout policy and return the numerical utility of the result.

        Args:
            tree ("Tree): the search tree
            state (list[str]): the clock game state
            constraints (list[str]): constraints our player wants to satisfy
            remaining_cards (list[str]): cards from all players not yet played

        Returns:
            "Tree": the search tree with updated scores
        """
        new_state = np.copy(state)
        while len(remaining_cards):
            # follow random playout policy until the end
            # remaining_cards.pop(random.randint(len(remaining_cards) - 1))
        
        score = utility()
        
        cur_node = tree.get(state)
        cur_node.score += score
        cur_node.N += 1
        tree.root.score += score
        tree.root.N += 1
        
        return tree

    def utility(constraints: list[str], final_state: list[str]):
        pass

    # def play(self, cards: list[str], constraints: list[str], state: list[str], territory: list[int]) -> Tuple[int, str]:

    def play(self, cards, constraints, state, territory):
        """Function which based n current game state returns the distance and angle, the shot must be played

        Args:
            score (int): Your total score including current turn
            cards (list): A list of letters you have been given at the beginning of the game
            state (list(list)): The current letters at every hour of the 24 hour clock
            territory (list(int)): The current occupiers of every slot in the 24 hour clock. 1,2,3 for players 1,2 and 3. 4 if position unoccupied.
            constraints(list(str)): The constraints assigned to the given player

        Returns:
            Tuple[int, str]: Return a tuple of slot from 1-12 and letter to be played at that slot
        """
        
        # letter = self.rng.choice(cards)
        territory_array = np.array(territory)
        available_hours = np.where(territory_array == 4)
        # because np.where returns a tuple containing the array, not the array itself
        # hour = self.rng.choice(available_hours[0])
        # hour = hour % 12 if hour % 12 != 0 else 12
        move = MCST(cards, constraints, state, territory)
        return move.hour, move.letter
