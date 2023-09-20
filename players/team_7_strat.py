from tokenize import String
import numpy as np
from typing import Tuple, List
import random
import math
import time
import numpy
import sys
import string

letters = list(string.ascii_uppercase)
#print(sys.getrecursionlimit())
class Player:
    def __init__(self, rng: np.random.Generator) -> None:
        self.rng = rng

    #def choose_discard(self, cards: list[str], constraints: list[str]):
    def choose_discard(self, cards, constraints):
       
        final_constraints = []

        for i in range(len(constraints)):
            list_of_letters = constraints[i].split("<")
            for j in cards:
                if j in list_of_letters:
                    final_constraints.append(constraints[i])
                    break
        #print(cards)
        #print(final_constraints)
        return final_constraints



    #def play(self, cards: list[str], constraints: list[str], state: list[str], territory: list[int]) -> Tuple[int, str]:
    def play(self, cards, constraints, state, territory):
       
        #Do we want intermediate scores also available? Confirm pls

        self.level = 0
        self.time = time.process_time()
        #print(self.time)
        global mx
        state_array = np.array(state)
        duplicate_cards = cards.copy()
        duplicate_state =  state.copy()
        duplicate_territory = territory.copy()
        duplicate_constraints = constraints.copy()
        score = self.getCurrentScore(constraints, state_array, territory)
        child, util = self.maximize(duplicate_cards, duplicate_state,
                                    duplicate_territory, duplicate_constraints, -10000, 10000)
        ##print(self.current_score_calculator(constraints, state, territory))
        
        #print(cards)
        letter = child[0]
        hour = child[1]
        hour = hour%12 if hour%12!=0 else 12
        #print(letter)

        return hour, letter
    
    
    def minimize(self, cards, state, territory, constraints, alpha, beta):
        self.level = self.level + 1
        #print(self.level)
        curr_time = time.process_time() - self.time
        availableMoves = self.getAvailableMoves(cards, territory)
        territory_array = np.array(territory)
        available_hours = np.where(territory_array == 4)
        available_hours =  np.array(available_hours)
        
        availableLetters = list(set(letters) - set(state) - set(cards))

        minChild, minUtil = 0, 10000
     
        for i in range(2):
            for j in range(len(territory_array)):
                if state[j] == 'Z' and self.rng.random()<=(1/float(len(available_hours[0]))):
                    availableLetters = list(set(letters) - set(state) - set(cards))
                    state[j] = 'A' #random letter for now
                    territory[j] = 0 if i == 0 else 2 #HARDCODED. NEEDS TO BE CHANGED TO OTHER PLAYER #

                    other, util = self.maximize(cards, state, territory, constraints, alpha, beta)
                    
                    util = util + self.getCurrentScore(constraints, cards, territory)

                    if util < minUtil:
                        minChild , minUtil = ['A', j], util
                    
                    if minUtil <= alpha:
                        break
                    
                    if minUtil <= beta:
                        beta = minUtil
                    
        return minChild, minUtil
        

    def maximize(self, cards, state, territory, constraints, alpha, beta):
        self.level = self.level + 1
        curr_time = time.process_time() - self.time
        territory_array = np.array(territory)
        available_hours = np.where(territory_array == 4)
        availableMoves = self.getAvailableMoves(cards, territory)
        if availableMoves == {} or curr_time >= 1:
            return [state, territory], self.getCurrentScore(constraints, cards, territory)
        
        maxChild, maxUtil = 0, -10000
        for child in availableMoves:
            currLetter = child
            for currLocation in availableMoves[child]:
                state[currLocation] = currLetter
                territory[currLocation] = 2 #HARDCODED. NEEDS TO BE CHANGED TO CURRENT PLAYER #
                other, util = self.minimize(cards, state, territory, constraints, alpha, beta)  
                util = util + self.getCurrentScore(constraints, state, territory)
                if util > maxUtil:
                    maxChild, maxUtil = [currLetter, currLocation], util
                    
                if maxUtil >= beta:
                    break
                
                if maxUtil >= alpha:
                    alpha = maxUtil
            
        return maxChild, maxUtil

    def getAvailableMoves(self, cards, territory):
        availableMoves = {}
        territory_array = np.array(territory)
        available_hours = np.where(territory_array == 4)
        for i in cards:
            for j in available_hours:
                availableMoves[i] = j
        return availableMoves

    def getCurrentScore(self, constraints, state, territory):
        letter_position = {}
        for i in range(len(state)):
            letter_position[state[i]] = i
        score = 0
        score_value_list = [1,3,12,24]  #points for satisfying constraints on different lengths
        for j in range(len(constraints)):
            list_of_letters = constraints[j].split("<")
            constraint_true_indic = True
            for i2 in range(len(list_of_letters)-1):
                #Also include intermediate score functionality
                if list_of_letters[i2+1] in letter_position and list_of_letters[i2] in letter_position:
                    distance_difference = (letter_position[list_of_letters[i2+1]]%12) - (letter_position[list_of_letters[i2]]%12)
                    if distance_difference < 0:
                        distance_difference = distance_difference + 12
                    if not (distance_difference <=5 and distance_difference > 0):
                        constraint_true_indic = False
                else:
                    constraint_true_indic = False
                if constraint_true_indic == False:
                    score = score - 10
                if constraint_true_indic:
                    score = score + score_value_list[len(list_of_letters) - 2]
        return score*10