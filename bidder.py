import random

class Bidder:
    def __init__(self,id,min_budget,max_budget,min_val,max_val,max_bid_below_val,highest):
        self.bidder_id=id
        self.highest=highest
        if self.highest:
            self.budget=max_budget
        else:
            self.budget = random.uniform(min_budget,max_budget)
        self.valuations = []
        self.bought_at = []
        self.min_val=min_val
        self.max_val=max_val
        self.max_bid_below_val=max_bid_below_val

    def get_valuation_and_bid(self):
        
        valuation = random.uniform(self.min_val,self.max_val)
        bid = valuation-random.uniform(0,self.max_bid_below_val)
        
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