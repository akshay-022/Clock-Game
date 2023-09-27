import numpy as np
from typing import List, Tuple
import time 

class Player:
    def __init__(self, rng: np.random.Generator) -> None:
        self.rng = rng
        self.time = 0

    #def choose_discard(self, cards: list[str], constraints: list[str]):
    def choose_discard(self, cards, constraints):
        """Function in which we choose which cards to discard, and it also inititalises the cards dealt to the player at the game beginning

        Args:
            cards(list): A list of letters you have been given at the beginning of the game.
            constraints(list(str)): The total constraints assigned to the given player in the format ["A<B<V","S<D","F<G<A"].

        Returns:
            list[int]: Return the list of constraint cards that you wish to keep. (can look at the default player logic to understand.)
        """
        
        final_constraints = []
        stripped_constraints = []
        constraint_list = [] 

        largeValue = False

        if len(constraints) > 499:
            largeValue = True 

        for i in range(len(constraints)):
            # splits current constraint into array of letters and removes <'s 
            curr = constraints[i].split('<')
            while '<' in curr:
                curr.remove('<')
            numLetters = len(curr)
            
            # see how many letters in a constraint we have 
            matches = 0
            for letter in curr:
                if letter in cards:
                    matches += 1

            match numLetters:
                    case 2:
                        if(matches == 1) or (matches == 2):
                            if largeValue: 
                                if not self.check_contradiction(constraints[i], final_constraints):
                                    final_constraints.append(constraints[i])
                            else: 
                                final_constraints.append(constraints[i])
                    case 3:
                        if(matches == 2):
                            if largeValue: 
                                if not self.check_contradiction(constraints[i], final_constraints):
                                    final_constraints.append(constraints[i])
                            else: 
                                final_constraints.append(constraints[i])
                    case 4:
                        if(matches == 3): #was 2
                            if largeValue: 
                                if not self.check_contradiction(constraints[i], final_constraints):
                                    final_constraints.append(constraints[i])
                            else: 
                                final_constraints.append(constraints[i])
                        elif((curr[0] in cards and curr[2] in cards) or (curr[1] in cards and curr[3] in cards)):
                            if largeValue: 
                                if not self.check_contradiction(constraints[i], final_constraints):
                                    final_constraints.append(constraints[i])
                            else: 
                                final_constraints.append(constraints[i])
                    case 5:
                        if(matches == 4): #was 3
                            if largeValue: 
                                if not self.check_contradiction(constraints[i], final_constraints):
                                    final_constraints.append(constraints[i])
                            else: 
                                final_constraints.append(constraints[i])
                        elif((curr[0] in cards and curr[2] in cards and curr[4] in cards)):
                            if largeValue: 
                                if not self.check_contradiction(constraints[i], final_constraints):
                                    final_constraints.append(constraints[i])
                            else: 
                                final_constraints.append(constraints[i])

        return final_constraints
    
    def check_contradiction(self, constraint, final_constraints):
    
        """
        Check if a constraint contradicts with existing final constraints.

        Args:
            constraint (str): The constraint to check for contradiction.
            final_constraints (list[str]): List of existing constraints.

        Returns:
            bool: True if a contradiction is found, False otherwise.
        """

        if len(final_constraints)<=1: 
            return False
        
        constraint = constraint.split("<")

        for i in range(len(final_constraints)):
            if len(final_constraints[i]) == len(constraint):
                curr = final_constraints[i].split("<")
                # check if another constraint has 2 or more letters that this constraint has 
                matches = 0
                indicies = [] 
                for j in range(len(curr)):
                    if curr[j] in constraint:
                        matches += 1
                        indicies.append(j)
                if matches > 1: 
                    for k in range(len(indicies)-1):
                        if curr[indicies[k]] in constraint and curr[indicies[k+1]] in constraint: 
                            index1 = indicies[k]
                            index2 = indicies[k+1]
                            index3 = constraint.index(curr[indicies[k]])
                            index4 = constraint.index(curr[indicies[k+1]])

                            if index1 < index2:
                                if index3 > index4:
                                    return True
                            else: 
                                if index3 < index4:
                                    return True

        return False 
                

    def get_other_cards(self, cards: List[str], state: List[str]) -> List[str]:

        """Get the cards that are not in the player's hand or on the game board.

        Args:
            cards (List[str]): The player's cards.
            state (List[str]): The current state of the game.

        Returns:
            List[str]: List of cards that are not in the player's hand or on the board.
        """

        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X']
        return [letter for letter in letters if letter not in cards and all(letter not in hour for hour in state)]
   
    # Minimax is a decision-making algorithm often used in two-player games.
    # Returns a tuple containing the best possible move with the best possible hour.
    # Credit to team 7 for the idea
    def minimax(self, state: List[str], cards: List[str], constraints: List[str], depth: int, is_maximizing: bool, alpha, beta) -> Tuple[List, float]:

        """Implement the minimax algorithm for making decisions in the game.

        Args:
            state (List[str]): The current state of the game.
            cards (List[str]): The player's cards.
            constraints (List[str]): The constraints assigned to the player.
            depth (int): The current depth of the minimax tree.
            is_maximizing (bool): True if maximizing player's turn, False otherwise.
            alpha: Alpha value for alpha-beta pruning.
            beta: Beta value for alpha-beta pruning.

        Returns:
            Tuple[List, float]: A tuple containing the best move (hour, card) and its associated score.
        """

        best_move = None
        score = self.get_score(state, cards, constraints)
        curr_time = time.process_time() - self.time

        available_hours = [i for i, hour in enumerate(state) if 'Z' in hour]

        if len(available_hours)==0 or curr_time >= 0.1:
            score = self.get_score(state, cards, constraints)
            return state, score

        if is_maximizing:  
            best_score = -1000
            for i in available_hours:
                for x in cards:
                    if x not in state[i]:
                        state[i] = x
                        for j in range(2):
                            score = self.minimax(state, cards, constraints, depth+1, False, alpha, beta)[1]
                        state[i] = 'Z'
                        if score > best_score:
                            best_score = score
                            best_move = (i, x)
                        
                        if best_score >= beta:
                            return best_move, best_score

                        alpha = max(alpha, best_score)
        else:
            best_score = 1000
            other_cards = self.get_other_cards(cards, state)
            for i in available_hours:
                for x in other_cards:
                    if x not in state[i]:
                        state[i] = x
                        score = self.minimax(state, cards, constraints, depth+1, True, alpha, beta)[1]
                        state[i] = 'Z'

                        if score < best_score:
                            best_score = score
                            best_move = (i, x)

                        if best_score <= alpha:
                            return best_move, best_score
                        
                        beta = min(beta, best_score)


        if best_move is None:
            letter = self.rng.choice(cards)
            if not available_hours:
                
                # Handle the case where available_hours is empty (e.g., all hours are occupied)
                # You can choose a default action here, like choosing a random card and hour.
                # For example:
                hour = self.rng.choice(range(1, 13))  # Choose a random hour from 1 to 12
            else:
                hour = self.rng.choice(available_hours) % 12 or 12
            best_move = hour, letter

        return best_move, best_score
    
    # Calls minimax function and obtains the best move to returns.
    def play(self, cards: List[str], constraints: List[str], state: List[str], territory: List[int]) -> Tuple[int, str]:

        """Play a move in the game using the minimax algorithm.

        Args:
            cards (List[str]): The player's cards.
            constraints (List[str]): The constraints assigned to the player.
            state (List[str]): The current state of the game.
            territory (List[int]): Territory information.

        Returns:
            Tuple[int, str]: The selected move as (hour, card).
        """

        self.time = time.process_time()
        new_cards = cards.copy() 
        new_state = state.copy()
        new_constraints = constraints.copy()
        depth = 0

        best_move, bestScore = self.minimax(new_state, new_cards, new_constraints, depth, True, -10000, 10000)
        letter = best_move[1]
        hour = best_move[0] % 12 or 12
        return hour, letter

    # returns 
    def get_score(self, state: List[str], cards: List[str], constraints: List[str]) -> float:

        """Calculate the player's score based on the given game state and constraints.

        Args:
            state (List[str]): The current state of the game.
            cards (List[str]): The player's cards.
            constraints (List[str]): The constraints assigned to the player.

        Returns:
            float: The player's score.
        """
        
        total_score = 0
        score_arr = [0, 0, 1, 3, 6, 12] # array of possible scores based on each index as the number of letters in the constraint
        positions = {}

        for i, hour in enumerate(state):
            for j, letter in enumerate(hour):
                positions[letter] = i

        for constraint in constraints:
            curr = constraint.split('<')
            curr = [c for c in curr if c.isalpha()]

            for i in range(len(curr) - 1):
                if curr[i] in positions and curr[i+1] in positions:
                    position1 = positions[curr[i]]
                    position2 = positions[curr[i+1]]
                    difference = (position2 % 12) - (position1 % 12)

                    if difference < 0:
                        difference += 12

                    if difference <= 5:
                        total_score += float(score_arr[len(curr)] / len(curr))
                    else:
                        total_score -= 3
        return total_score