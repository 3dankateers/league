############################################################################
## prints results of evaluating team comp based on winrates of each champ 
############################################################################
from champ import Champ
from evaluator import Evaluator
from champ_winrate_calculator import ChampWinrateCalculator

CONF_THRESHOLD = 0.01
ONE_CHAMP_SAMPLE_LIMIT = 10
CHAMPS_CONSIDERED_REQUIRED = 4

##stores information calculated in process()
class TeamInfo:
    def __init__(self, champ_ids):
        self.champ_ids = champ_ids
        self.winrates = [-1] * 5
        self.aggregate_winrate = 0
        self.total_winrate = 0
        self.num_champs_considered = 0

    def update_aggregate_winrate(self):
        for r in self.winrates:
            if r != -1:
                self.total_winrate += r
            if self.num_champs_considered > 3:
                self.aggregate_winrate = self.total_winrate/self.num_champs_considered

    def print_result(self):
        print "Normalized win rate = ", str(self.aggregate_winrate)


class OneChampEvaluator(Evaluator):

    def __init__(self, champs1_ids, champs2_ids):
        self.ti1 = TeamInfo(champs1_ids)
        self.ti2 = TeamInfo(champs2_ids)

    ## return 100 if team1 is favoured, else return 200
    def predict_winner(self):
        return self.winner

    ##return true if confident in predicted winner, otherwise false
    def is_confident(self):
        if abs(self.ti1.aggregate_winrate - self.ti2.aggregate_winrate) > CONF_THRESHOLD:
            if(self.ti1.num_champs_considered > CHAMPS_CONSIDERED_REQUIRED and self.ti2.num_champs_considered > CHAMPS_CONSIDERED_REQUIRED):
                return True
            else:
                return False

    @staticmethod
    def retrain():
        pass
        ##cwc = ChampWinrateCalculator()
        ##cwc.run()


    ## calculate winrates needed
    ## process each team independently
    def process(self):
        self.process_team(self.ti1)
        self.process_team(self.ti2)
        self.normalize_winrates()

        if self.ti1.aggregate_winrate > self.ti2.aggregate_winrate:
            self.winner = 100
        else:
            self.winner = 200

    def normalize_winrates(self):
        winrate1 = self.ti1.aggregate_winrate
        winrate2 = self.ti2.aggregate_winrate
        if (winrate1+winrate2) > 0:
            self.ti1.aggregate_winrate = winrate1/(winrate1 + winrate2)
            self.ti2.aggregate_winrate = winrate2/(winrate1 + winrate2)


    ##calculates all neccesary team info and updates ti (teaminfo)
    def process_team(self, ti):
        for i,champ_id in enumerate(ti.champ_ids):
            champ = Champ.get_champ_by_id(champ_id)
            if (champ.winrate != None) and (champ.winrate_sample_size > ONE_CHAMP_SAMPLE_LIMIT):
                ti.winrates[i] = champ.winrate
                ti.num_champs_considered += 1
            ti.update_aggregate_winrate()

    def print_results(self):
        print "#################################################################################"
        print "One Champ Evaluator Results: "
        print "Team1"
        self.ti1.print_result()
        print "#########################################################"
        print "Team2"
        self.ti2.print_result()
        print "Difference: ", self.ti2.aggregate_winrate - self.ti1.aggregate_winrate
        print "WINNER: ", self.winner
        print "#################################################################################"

    @staticmethod
    def print_class():
        print "One Champ Evaluator"
