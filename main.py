from cartel import Cartel
from bidder import Bidder
from auction import Auction

def run_an_auction(objects,min_budget,max_budget,total_participants,cartel_members,k):

    individual_bidders = total_participants-cartel_members

    auction = Auction(objects,individual_bidders)
    bidders = []
    cartel = Cartel(cartel_members,0,k,max_budget)

    bidders.append(cartel)
    for i in range(1,individual_bidders):
        bidder = Bidder(i,min_budget,max_budget)
        bidders.append(bidder)
    

    while(auction.objects>0):
        auction.startRound()

        cartelBid = cartel.getCartelBid()
        auction.placeBid(0,cartelBid)

        for i in range(1,individual_bidders):
            bidderBid = bidders[i].get_valuation_and_bid()
            auction.placeBid(i,bidderBid)

        winner_id,second_price = auction.getWinner()

        for i in range(1,individual_bidders):
            bidders[i].checkWon(winner_id,second_price)
        
        cartel.checkWon(winner_id,second_price)
    
    total_utility_individuals = 0

    for i in range(1,individual_bidders):
        total_utility_individuals += bidders[i].getUtility()

    avg_utility_individuals = total_utility_individuals/(individual_bidders-1) 

    avg_cartel_members_util,cartel_leader_util = cartel.getUtility()

    cartel_wins = cartel.cartel_wins

    return avg_utility_individuals,avg_cartel_members_util,cartel_leader_util,cartel_wins


if __name__ == "__main__":

    objects = 10
    min_budget = 200
    max_budget = 300
    total_participants=20
    cartel_members=5
    k=0.1

    runs=100


    total_avg_utils_individuals=0
    total_avg_cartel_utils=0
    total_leader_utils = 0
    total_cartel_wins_allruns = 0

    for i in range(runs):
        avg_utility_individuals,avg_cartel_members_util,cartel_leader_util,total_cartel_wins = run_an_auction(objects,min_budget,max_budget,total_participants,cartel_members,k)
        
        total_avg_utils_individuals +=  avg_utility_individuals
        total_avg_cartel_utils += avg_cartel_members_util
        total_leader_utils += cartel_leader_util
        total_cartel_wins_allruns +=total_cartel_wins

    avg_avg_utils_individuals=total_avg_utils_individuals/runs
    avg_avg_cartel_utils=total_avg_cartel_utils/runs
    avg_leader_utils=total_leader_utils/runs
    avg_cartel_wins=total_cartel_wins_allruns/runs

    print("============== ",runs," runs ==============")
    
    print("Avg of all runs (Avg utility of all non cartel members in a run) : ",avg_avg_utils_individuals)
    print("Avg of all runs (Avg utility of all cartel members in a run) : ",avg_avg_cartel_utils)
    print("Avg of cartel leader utility of all runs : ",avg_leader_utils)
    print("Avg of cartel wins of all runs : ",avg_cartel_wins)

