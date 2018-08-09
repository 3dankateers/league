############################################################################
## analyzes data from matches db and calculates winrates for each team to determine if Blue or Red team has advantage
############################################################################
from match import Match

class TeamWinrateCalculator:
    
    def __init__(self, prediction_target = Match.WIN):
        ##counts wins and losses for each champ
        self.redWins = 0
        self.blueWins = 0
        self.prediction_target = prediction_target



    def run(self):
        ##reset winrates and then recalculate
        self.count_all_matches()
        #self.update_winrates()
    
    ##populate losses and wins with the information from each match in db
    def count_all_matches(self): 
        matches = Match.get_training_set()
        print("Training team winrates with training cases: ", len(matches))
        
        for m in matches:
            if m.win == 100:
                self.blueWins += 1
            else:
                self.redWins += 1

        print ("# of Blue Team Wins: " + str(self.blueWins))
        print ("# of Red Team Wins: " + str(self.redWins))
        print ("Team blue wins / total games : " + str(float(self.blueWins)/(float(self.redWins)+float(self.blueWins))))

    #need to decide if the results of this would be in a DB or just calculate it when you need it    

