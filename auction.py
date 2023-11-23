class Auction:
    #initializer / constructor
    def __init__(self,objects,participants):
        self.objects=objects
        self.participants = participants
        self.bids = [0 for _ in range(participants)]
    
    def startRound(self):
        self.bids = [0 for _ in range(self.participants)]


    def placeBid(self,bidder_id,bid_amount):
        self.bids[bidder_id] = bid_amount

    def getWinner(self):
        # print(self.bids)
        max_value = max(self.bids)
        max_index = self.bids.index(max_value)

        # Remove the maximum value from the list
        self.bids.remove(max_value)

        # Find the second maximum
        second_max_value = max(self.bids)

        self.objects-=1

        return max_index,second_max_value

