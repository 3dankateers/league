############################################################################ 
## populates db with pairs
## calculates win rates from match data
## updates db pair entries with winrates
############################################################################
from db_client import DbClient
from champ import Champ
from pair import Pair
from match import Match

PROMATCH_MULTIPLIER = 0 
MATCH_MULTIPLIER = 1 

##increment count in d for that specific pair
def increment_dict(d, pair_tuple):
    if pair_tuple in d:
        d[pair_tuple] += 1
    else:
        d[pair_tuple] = 1

class PairWinrateCalculator:

    def __init__(self):
        ##dicts used to count pair of enemies
        self.enemy_wins = {}
        self.enemy_losses = {}
        ##dicts used to count pair of enemies
        self.ally_wins = {}
        self.ally_losses = {}

    def run(self):
        ## drop everything at the start since everything is recalculated and inserted
        Pair.drop_all()
        self.count_matches()
        self.update_winrates(self.ally_wins, self.ally_losses, "ally")
        self.update_winrates(self.enemy_wins, self.enemy_losses, "enemy")
    
    
    ##update db pairs with a new winrate and sample size fot that winrate
    ## type = "ally" or "enemy", and d_wins and d_losses are the correponding dictionaries for ally or enemy
    def update_winrates(self, d_wins, d_losses, type):
        all_pairs_dicts = []
        p_tuples = []
        for key, value in d_wins.iteritems():
            ##print key,value
            if key in d_losses: ##make sure pair has wins an losses
                pair = Pair(key[0], key[1], type)
                winrate_sample_size = value + d_losses[key]
                winrate = value/float(winrate_sample_size) ##wins/wins+losses
                p_tuples.append((key[0], key[1], type, winrate, winrate_sample_size))
        Pair.insert_from_tuples(p_tuples)

    def count_matches(self):
        matches = Match.get_training_set()
        print "Training pairs with training cases: ", len(matches)
        for m in matches:
            champs1 = m.champs1
            champs2 = m.champs2
            ## 100 means team1 won, 200 means team2 won
            win = m.win
            ## count ally pairs in match
            if win  == 100:
                self.add_ally_pairs_to_dict(self.ally_wins, champs1)
                self.add_ally_pairs_to_dict(self.ally_losses, champs2)
            elif win == 200:
                self.add_ally_pairs_to_dict(self.ally_wins, champs2)
                self.add_ally_pairs_to_dict(self.ally_losses, champs1)
            

            ## count enemy pairs in match
            self.add_enemy_pairs_to_dict(win, champs1, champs2)

    
    ## generate all pairs from champs 
    ## increment the entries in the dictionary(d) that correspond to the pairs found in champs
    ## d is a dictionary with key = champ_pair and value = num wins or losses
    ## for each possible pair of champs in champs array, increment value of tuple array
    def add_ally_pairs_to_dict(self, d, champs):
        for c1 in champs:
            for c2 in champs:
                if c1 != c2:
                    pair_tuple = Pair.calc_pair_tuple(c1,c2)	
                    ##if pair was seen before
                    increment_dict(d, pair_tuple)

    ## generate all enemy pairs from champs1, champs2 
    ## increment the entries in the proper dictionaries that correspond to the pairs found in champs
    ## win = 100 means champs1 team won, win = 200 means champs2 team won
    def add_enemy_pairs_to_dict(self, win, champs1, champs2):
        for c1 in champs1:
            for c2 in champs2:
                if c1 != c2:
                    pair_tuple = Pair.calc_pair_tuple(c1,c2)	
                    if win == 100:
                        if pair_tuple[0] in champs1:
                            ##first champ in tuple is a winner
                            increment_dict(self.enemy_wins, pair_tuple)
                        else:
                            increment_dict(self.enemy_losses, pair_tuple)

                    elif win  == 200:
                        if pair_tuple[0] in champs1:
                            ##first champ in tuple is a loser
                            increment_dict(self.enemy_losses, pair_tuple)
                        else:
                            increment_dict(self.enemy_wins, pair_tuple)

                                    
