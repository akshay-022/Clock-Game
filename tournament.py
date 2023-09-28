import time
import numpy as np
from functools import reduce
from clock_gui import gui
import string
import constants
from players.default_player import Player as Default_Player
#have to change inheritance for all of these
from players.team_1 import Player as p1
from players.team_2 import Player as p2
from players.team_3 import Player as p3
from players.team_4 import Player as p4
from players.team_5 import Player as p5
from players.team_6 import Player as p6
from players.team_7 import Player as p7
from players.team_8 import Player as p8
from players.default_player import Player as p9
from players.default_player import Player as p10
from players.default_player import Player as p11
import time
import pickle as pkl
import copy
import argparse
from clock_game import clockGame
from copy import deepcopy

def initialise_player(rng, player_px):
    player_instance = None
    if player_px == 0:
        player_instance = Default_Player(rng)
    elif player_px == 1:
        player_instance = p1(rng)
    elif player_px == 2:
        player_instance = p2(rng)
    elif player_px == 3:
        player_instance = p3(rng)
    elif player_px == 4:
        player_instance = p4(rng)
    elif player_px == 5:
        player_instance = p5(rng)
    elif player_px == 6:
        player_instance = p6(rng)
    elif player_px == 7:
        player_instance = p7(rng)
    elif player_px == 8:
        player_instance = p8(rng)
    elif player_px == 9:
        player_instance = p9(rng)
    elif player_px == 10:
        player_instance = p10(rng)
    elif player_px == 11:
        player_instance = p11(rng)
    else:
        player_instance = None
    return player_instance

def init_assignments(rng):
    shuffled_letters = list(rng.choice(list(string.ascii_uppercase)[:24], 24, replace = False))
    options_letter = [shuffled_letters[:8],shuffled_letters[8:16],shuffled_letters[16:24]]
    constraints = [[],[],[]]
    for j in range(3):
        constraint_counter = 0
        const_exceeded = False
        while True:
            for i in range(2,6):            
                constraints_choice = rng.choice(list(string.ascii_uppercase)[:24], i, replace = False)     #I am preventing repetition of letters here since it makes some constraints impossible
                delim = "<"
                res = reduce(lambda x, y: str(x) + delim + str(y), constraints_choice)
                constraint_string = str(res)
                constraint_counter = constraint_counter + 1
                if constraint_counter <= constants.number_of_constraints_pp:
                    constraints[j].append(constraint_string)
                else:
                    const_exceeded = True
            if const_exceeded == True:
                break
    return options_letter, constraints


if __name__ == '__main__':
    tournament_results = []
    with open("tournament_results_"+ str(constants.number_of_constraints_pp) +".pkl","wb" ) as f:
        pkl.dump(tournament_results, f)
    combs = []
    x = [1,2,3,4,5,6,7,8]
    for i in x:
        for j in x:
            for k in x:
                if i!=j and j!=k and i!=k:
                    combs.append([i,j,k])

    print(len(combs))
    parser = argparse.ArgumentParser()
    parser.add_argument("--no_gui", "-ng", default = False, help="Disable GUI")
    parser.add_argument("--seed", "-s", default = 5, help="Choose seed number")
    args = parser.parse_args()
    args.no_gui = True
    for seed in range(3):
        player_instance = None
        #The below code is to prevent constraint choosing computation again and again for the same seeds and players. Makes tournament much faster.
        players_init_grid = []
        for player_number in range(1,9):
            rng = np.random.default_rng(seed)
            options_letter, constraints = init_assignments(rng)
            player_instance_1 = initialise_player(rng, player_number)
            player_instance_2 = initialise_player(rng, player_number)
            player_instance_3 = initialise_player(rng, player_number)
            constraints[0] = player_instance_1.choose_discard(options_letter[0],constraints[0])
            constraints[1] = player_instance_2.choose_discard(options_letter[1],constraints[1])
            constraints[2] = player_instance_3.choose_discard(options_letter[2],constraints[2])
            players_init_grid.append([options_letter, constraints, player_instance_1, player_instance_2, player_instance_3])
        print(players_init_grid)
        for comb in combs:
            args.seed = seed
            player_0_letters = deepcopy(players_init_grid[comb[0]-1][0][0])
            player_0_constraints = deepcopy(players_init_grid[comb[0]-1][1][0])
            player_1_letters = deepcopy(players_init_grid[comb[1]-1][0][1])
            player_1_constraints = deepcopy(players_init_grid[comb[1]-1][1][1])
            player_2_letters = deepcopy(players_init_grid[comb[2]-1][0][2])
            player_2_constraints = deepcopy(players_init_grid[comb[2]-1][1][2])
            player_instances = deepcopy([players_init_grid[comb[0]-1][2],players_init_grid[comb[1]-1][3],players_init_grid[comb[2]-1][4]])
            player_letters = [player_0_letters, player_1_letters, player_2_letters]
            player_constraints = [player_0_constraints, player_1_constraints, player_2_constraints]
            instance_clockgame = clockGame(args, is_tournament= True, player_0 = comb[0], player_1 = comb[1], player_2 = comb[2], options_letter = player_letters, constraints = player_constraints, player_instances = player_instances)
            instance_clockgame.use_gui = not args.no_gui
            instance_clockgame.run_game()
            print(constants.number_of_constraints_pp)
