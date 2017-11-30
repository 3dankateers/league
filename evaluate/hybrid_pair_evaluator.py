############################################################################
## evaluate 2 team comps based on enemy pairevaluator and ally pair evaluator results 
############################################################################

from pair import Pair
from evaluator import Evaluator
from pair_winrate_calculator import PairWinrateCalculator
from trainer import Trainer
from enemy_pair_evaluator import EnemyPairEvaluator
from ally_pair_evaluator import AllyPairEvaluator




class HybridPairEvaluator(Evaluator):

	def __init__(self, team1, team2):
            self.enemy_pair_evaluator = EnemyPairEvaluator(team1, team2)
            self.ally_pair_evaluator = AllyPairEvaluator(team1, team2)
	
	@staticmethod
	def print_class():
	    print "Hybrid Pair Evaluator"

	@staticmethod
	def retrain():
           pwc = PairWinrateCalculator()
           pwc.run()
	
	##processes each team comp in turn
	def process(self):
            self.enemy_pair_evaluator.process()
            self.ally_pair_evaluator.process()
            self.enemy_pair_winner = self.enemy_pair_evaluator.predict_winner()
            self.ally_pair_winner = self.ally_pair_evaluator.predict_winner()
            
            ##if predicted winner of enemy and ally pair evaluators agree return it, otherwise return 0 (don't predict)
            if self.enemy_pair_winner == self.ally_pair_winner:
                self.winner = self.enemy_pair_winner
            else:
                self.winner = 0

	## return 1 if team1 is favoured, else return 2
	def predict_winner(self):
	    return self.winner
	
	def is_confident(self):
            if abs(self.team1_enemy_info.aggregate_winrate - self.team2_enemy_info.aggregate_winrate) > CONF_THRESHOLD:
                ##if not enough relevantpairs return not confident	
                if(self.team1_enemy_info.num_relevant_pairs > RELEVANT_PAIRS_REQUIRED and self.team2_enemy_info.num_relevant_pairs > RELEVANT_PAIRS_REQUIRED):
                    return True
            else:
                return False
	
        def print_results(self):
            print "#################################################################################"
            print "Enemy Predicted winner:", self.enemy_pair_winner
            print "Ally Predicted winner:", self.ally_pair_winner
            print "WINNER: ", self.winner
            print "#################################################################################"
	


