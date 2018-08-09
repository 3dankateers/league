############################################################################
## analyzes data from matches db and calculates winrates for each champ
## inserts winrates into db
############################################################################
from champ import Champ
from match import Match

class ChampWinrateCalculator:
    
    def __init__(self, prediction_target = Match.WIN):
        ##counts wins and losses for each champ
        self.losses = {}
        self.wins = {}
        self.prediction_target = prediction_target



    def run(self):
        ##reset winrates and then recalculate
        Champ.reset_winrates()
        self.initilize_champ_dicts()
        self.count_all_matches()
        self.update_winrates()
    
    ##populate losses and wins with the information from each match in db
    def count_all_matches(self): 
        matches = Match.get_training_set()
        print("Training champ winrates with training cases: ", len(matches))
        
        for m in matches:
            for c1 in m.champs1:
                if m.win == 100:
                    self.wins[c1] += 1
                else:
                    self.losses[c1] += 1
            for c2 in m.champs2:
                if m.win == 100:
                    self.losses[c2] += 1
                else:
                    self.wins[c2] += 1

    ## initilizes losses/wins to 0 for each champ in champ db
    def initilize_champ_dicts(self):
        champs = Champ.get_all_champs()
        for c in champs:
            self.losses[c.champID] = 0
            self.wins[c.champID] = 0

    

    ##update db champ with a new winrate and sample size fot that winrate
    def update_winrates(self):
        champs = Champ.get_all_champs()
        for c in champs:
            sample_size = self.wins[c.champID] + self.losses[c.champID]
            if sample_size > 0:
                winrate = float(self.wins[c.champID]) / sample_size
                c.winrate = winrate
                c.winrate_sample_size = sample_size
                c.update()
    

