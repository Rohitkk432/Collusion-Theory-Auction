import random

class CartelMember:
    def __init__(self,id,budget,k):
        self.cartel_member_id=id
        self.budget = budget
        self.k = k
        self.valuations = []
        self.bought_at = []
        self.kProfit=0

    def get_valuation_and_bid(self):
        self.budget+=self.k
        self.kProfit+=self.k
        valuation = random.uniform(50,75)
        bid = valuation-random.uniform(0,10)+(random.uniform(0,3)*self.k)
        self.valuations.append(valuation)

        if(self.budget>=bid):
            return bid
        else:
            return 0
    
    def payK(self,members):
        self.kProfit-=(self.k*members)

    def getProfit(self,profit):
        self.kProfit+=profit
        
    def checkWon(self,winner_id,second_price):
        if self.cartel_member_id==winner_id:
            self.bought_at.append(second_price)
            self.budget-=second_price
        else:
            self.bought_at.append(-1)
    
    def getUtility(self):
        utility=0
        for i in range(len(self.valuations)):
            if(self.bought_at[i]!=-1):
                utility+=(self.valuations[i]-self.bought_at[i])
        utility+=self.kProfit
        # print('Cartel Memeber ',self.cartel_member_id,': utility = ',utility)
        return utility

class Cartel:

    #initializer / constructor
    def __init__(self,members,id,k,budget):
        self.cartel_wins=0
        self.members=members
        self.k=k
        self.cartel_id=id

        self.highest_bidder_id = -1
        self.cartel_highest_bid = 0
        self.cartel_second_highest_bid = 0
        self.auction_second_highest_bid = 0

        self.least_bidder_id=0

        self.members_objects=[]
        for i in range(members):
            self.members_objects.append(CartelMember(i,budget,k))
    
    def getCartelBid(self):
        bids = []
        for i in range(self.members):
            member = self.members_objects[i]
            bid  = member.get_valuation_and_bid()
            bids.append(bid)
        
        least_bid = min(bids)
        self.least_bidder_id = bids.index(least_bid)
        self.members_objects[self.least_bidder_id].payK(self.members)

        self.cartel_highest_bid = max(bids)
        self.highest_bidder_id = bids.index(self.cartel_highest_bid)
        bids.remove(self.cartel_highest_bid)

        self.cartel_second_highest_bid = max(bids)

        return self.cartel_highest_bid

    def checkWon(self,winner_id,second_price):
        if self.cartel_id==winner_id:
            self.auction_second_highest_bid = second_price
        
            max_second_price = max(self.auction_second_highest_bid,self.cartel_second_highest_bid)

            profit = max_second_price - self.auction_second_highest_bid
            self.members_objects[self.least_bidder_id].getProfit(profit)
            
            for i in range(self.members):
                member = self.members_objects[i]
                member.checkWon(self.highest_bidder_id,max_second_price)

            self.cartel_wins+=1

        else:
            for i in range(self.members):
                member = self.members_objects[i]
                member.checkWon(-1,0)

    def getUtility(self):
        members_total_util=0
        for i in range(self.members):
                member = self.members_objects[i]
                members_total_util += member.getUtility()
        
        avg_members_util = members_total_util/self.members

        return avg_members_util

