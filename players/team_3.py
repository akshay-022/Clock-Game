from tokenize import String
import numpy as np
from typing import Tuple, List

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
        print("CONSTRAINTS")
        print(constraints)

        print("CARDS")
        print(cards)

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
                            final_constraints.append(constraints[i])
                    case 3:
                        if(matches == 2):
                            final_constraints.append(constraints[i])
                    case 4:
                        if(matches == 3):
                            final_constraints.append(constraints[i])
                        elif((curr[0] in cards and curr[2] in cards) or (curr[1] in cards and curr[3] in cards)):
                            final_constraints.append(constraints[i])
                    case 5:
                        if(matches == 4):
                            final_constraints.append(constraints[i])
                        elif((curr[0] in cards and curr[2] in cards and curr[4] in cards)):
                            final_constraints.append(constraints[i]) 

            # if we don't have any letters in a constraint don't choose it 

            #if(len(final_constraints) == 0){
            #}
  
            #if self.rng.random()<=0.5:
            #   final_constraints.append(constraints[i])

        print("FINAL")
        print(final_constraints)
        return final_constraints
    
    

    def is_played(self, letter, state):
        for i in range(len(state)):
            if letter in state[i]:
                return (True, i)
        return (False, -1)
    
    def bestMove (self, available_hours, cards):
        bestScore = float('-inf')
        moves = [[]]
        bestMove = []
        for i in available_hours:
            for x in cards:
                hour = i
                letter = x
                score = self.minimax(clock, hour, letter, 0, true)
                if (score>bestScore):
                    bestScore = score
                    bestMove = [i,x]
        
        return bestMove


    def getScore(self, state, territory):
        pass
        
# state = [] array of one to 24, z is empty 
# territory = [] array of one to 24, # of player who's there 
# a

        
    def getAvailableMoves(self, cards, state):
        availableMoves = {}
        state_array = np.array(state)
        available_hours = np.where(state_array == 'Z')
        for i in available_hours:
            for x in cards:
                availableMoves.append(i,x)
        return availableMoves
    

    # function to get unplayed cards on the board 
    def getOtherCards(self, cards, state):
        letters = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X']
        for i in cards:
            if i in letters:
                letters.remove(i)
        for i in state: 
            if i in letters: 
                letters.remove(i)
        return letters 


    def minimax(state, hour, letter, cards, depth, isMaximizing):
        # check what the score is/ who the "winner" is 

        state_array = np.array(state)
        available_hours = np.where(state_array == 'Z')
        
        #maximizing
        if(isMaximizing): # anita 
            bestScore = float('-inf')
            for i in available_hours:
                for x in cards:
                    if i == hour and x == letter:
                        pass
                    hour = i
                    letter = x
                    #change available hours before passing 
                    score = self.minimax(state, hour, letter, cards, depth+1, False)
                  
                    if (score>bestScore):
                        bestScore = score
                        bestMove = [i,x]

        #minimizing 
        else:
            bestScore = float('inf')
            other_cards = self.getOtherCards(self, cards, state)
            for i in available_hours:
                for x in other_cards:
                    hour = i
                    letter = x
                    #change available hours before passing 
                    score = self.minimax(state, hour, letter, cards, depth+1, True)
                  
                    if (score<bestScore):
                        bestScore = score
                        bestMove = [i,x]
        
        return bestMove
            

    #def play(self, cards: list[str], constraints: list[str], state: list[str], territory: list[int]) -> Tuple[int, str]:
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

        letter = self.rng.choice(cards)
        territory_array = np.array(territory)
        available_hours = np.where(territory_array == 4)
        hour = self.rng.choice(available_hours[0])          #because np.where returns a tuple containing the array, not the array itself
        hour = hour%12 if hour%12!=0 else 12

        return hour, letter
