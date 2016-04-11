def exp_moving_avg(self, weight):
     ewma = EWMA_SEED

     for i in reversed(range(self.total_done)):
         ewma = weight * self.get_answer_at(i) + (1 - weight) * ewma

     return ewma