import matplotlib.pyplot as plt 

from cartel import Cartel
from bidder import Bidder
from auction import Auction

def run_an_auction(objects,min_budget,max_budget,total_participants,cartel_members,k,min_val,max_val,max_bid_below_val):

    individual_bidders = total_participants-cartel_members

    auction = Auction(objects,individual_bidders)
    bidders = []
    cartel = Cartel(cartel_members,0,k,max_budget,min_val,max_val,max_bid_below_val)

    bidders.append(cartel)
    for i in range(1,individual_bidders):
        bidder = Bidder(i,min_budget,max_budget,min_val,max_val,max_bid_below_val)
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

    avg_cartel_members_util,cartel_leader_util,theo_k = cartel.getUtility()

    cartel_wins = cartel.cartel_wins

    return avg_utility_individuals,avg_cartel_members_util,cartel_leader_util,cartel_wins,theo_k


if __name__ == "__main__":

    objects = 10
    min_budget = 200
    max_budget = 300
    total_participants=20
    # cartel_members=10
    k=0.07

    runs=500

    min_val=50
    max_val=75
    max_bid_below_val=10

    Y1=[]
    Y2=[]
    Y3=[]
    Y4=[]
    Y5=[]
    xAxis=[]

    # total_participants=10
    cartel_members=3
    while(cartel_members<16):
        cartel_members+=1
        # total_participants=cartel_members*2
        total_avg_utils_individuals=0
        total_avg_cartel_utils=0
        total_leader_utils = 0
        total_cartel_wins_allruns = 0

        k_lt_7=0
        k_nlt_7=0

        for i in range(runs):
            avg_utility_individuals,avg_cartel_members_util,cartel_leader_util,total_cartel_wins,theo_k = run_an_auction(objects,min_budget,max_budget,total_participants,cartel_members,k,min_val,max_val,max_bid_below_val)
        
            total_avg_utils_individuals +=  avg_utility_individuals
            total_avg_cartel_utils += avg_cartel_members_util
            total_leader_utils += cartel_leader_util
            total_cartel_wins_allruns +=total_cartel_wins

            if theo_k>=k:
                k_lt_7+=1
            else:
                k_nlt_7+=1

        # print("K theorotial < K passed , cases correct ",k_lt_7,"/500 cases wrong ",k_nlt_7,"/500")

        avg_avg_utils_individuals=total_avg_utils_individuals/runs
        avg_avg_cartel_utils=total_avg_cartel_utils/runs
        avg_leader_utils=total_leader_utils/runs
        avg_cartel_wins=total_cartel_wins_allruns/runs

        Y1.append(avg_avg_utils_individuals)
        Y2.append(avg_avg_cartel_utils)
        Y3.append(avg_leader_utils)
        Y4.append(avg_cartel_wins)
        Y5.append(k_lt_7)
        xAxis.append(cartel_members)

        print("============== ",runs," runs ==============")
    
        # print("Avg of all runs (Avg utility of all non cartel members in a run) : ",avg_avg_utils_individuals)
        # print("Avg of all runs (Avg utility of all cartel members in a run) : ",avg_avg_cartel_utils)
        # print("Avg of cartel leader utility of all runs : ",avg_leader_utils)
        # print("Avg of cartel wins of all runs : ",avg_cartel_wins)

    plt.figure()
    plt.plot(xAxis,Y1)
    plt.title("Non cartel Members utility changing no. of cartel members")
    plt.savefig('./outputs/CmemY1.png')

    plt.figure()
    plt.plot(xAxis,Y2)
    plt.title("cartel Members utility changing no. of cartel members")
    plt.savefig('./outputs/CmemY2.png')

    plt.figure()
    plt.plot(xAxis,Y3)
    plt.title("cartel leader util changing no. of cartel members")
    plt.savefig('./outputs/CmemY3.png')

    plt.figure()
    plt.plot(xAxis,Y4)
    plt.title("cartel wins changing no. of cartel members")
    plt.savefig('./outputs/CmemY4.png')

    plt.figure()
    plt.plot(xAxis,Y5)
    plt.title("k theo >= k changing no. of cartel members")
    plt.savefig('./outputs/CmemY5.png')

