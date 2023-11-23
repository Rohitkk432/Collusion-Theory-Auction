import random

class Bidder:
    def __init__(self,id,min_budget,max_budget):
        self.bidder_id=id
        self.budget = random.uniform(min_budget,max_budget)
        self.valuations = []
        self.bought_at = []

    def get_valuation_and_bid(self):
        
        valuation = random.uniform(50,75)
        bid = valuation-random.uniform(0,10)
        
        self.valuations.append(valuation)

        if(self.budget>=bid):
            return bid
        else:
            return 0
        
    def checkWon(self,winner_id,second_price):

        if self.bidder_id==winner_id:
            self.bought_at.append(second_price)
            self.budget-=second_price
        else:
            self.bought_at.append(-1)
    
    def getUtility(self):
        utility=0

        for i in range(len(self.valuations)):
            if(self.bought_at[i]!=-1):
                utility+=(self.valuations[i]-self.bought_at[i])

        # print('Bidder ',self.bidder_id,': utility = ',utility)
        return utility