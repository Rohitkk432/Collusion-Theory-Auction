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
        bidder = Bidder(i,min_budget,max_budget,min_val,max_val,max_bid_below_val,False)
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

def run_an_auction_NoCartel(objects,min_budget,max_budget,total_participants,cartel_members,k,min_val,max_val,max_bid_below_val):

    individual_bidders = total_participants-cartel_members

    auction = Auction(objects,total_participants)
    bidders = []

    for i in range(0,cartel_members):
        bidder = Bidder(i,min_budget,max_budget,min_val,max_val,max_bid_below_val,True)
        bidders.append(bidder)

    for i in range(cartel_members,total_participants):
        bidder = Bidder(i,min_budget,max_budget,min_val,max_val,max_bid_below_val,False)
        bidders.append(bidder)
    

    while(auction.objects>0):
        auction.startRound()

        for i in range(0,total_participants):
            bidderBid = bidders[i].get_valuation_and_bid()
            auction.placeBid(i,bidderBid)

        winner_id,second_price = auction.getWinner()

        for i in range(0,total_participants):
            bidders[i].checkWon(winner_id,second_price)
            
    total_utility_individuals = 0
    total_utility_wannabe_cartel = 0
    
    for i in range(cartel_members,total_participants):
        total_utility_individuals += bidders[i].getUtility()

    for i in range(0,cartel_members):
        total_utility_wannabe_cartel += bidders[i].getUtility()

    avg_utility_individuals = total_utility_individuals/individual_bidders 
    avg_utility_wannabe_cartel = total_utility_wannabe_cartel/(individual_bidders-1) 

    return avg_utility_individuals,avg_utility_wannabe_cartel


def VaryK(hidePrints):
    objects = 10
    min_budget = 200
    max_budget = 300
    total_participants=20
    cartel_members=10

    runs=500

    min_val=50
    max_val=75
    max_bid_below_val=10

    yAxis=[]
    xAxis=[]


    print('============= Parameters =============')
    print('-- Objects in auction = ',objects,"\n")
    print('-- budget = uniform random (',min_budget,',',max_budget,")","\n")
    print('-- total participants(bidders) = ',total_participants,"\n")
    print('-- cartel members(excluding leader)(have highest budget) = ',cartel_members,"\n")
    print('-- valuation = uniform random (',min_budget,',',max_budget,")","\n")
    print('-- Bid reduced from valuation by = uniform random (0,',max_budget,")","\n")
    print('-- k = 0.05 to 0.1',"\n\n")

    k=0.045

    yKTheo=[]

    while(k<=0.1):
        k+=0.005

        total_avg_utils_individuals=0
        total_avg_cartel_utils=0
        total_leader_utils = 0
        total_cartel_wins_allruns = 0

        k_lt_ktheo=0

        for i in range(runs):
            avg_utility_individuals,avg_cartel_members_util,cartel_leader_util,total_cartel_wins,theo_k = run_an_auction(objects,min_budget,max_budget,total_participants,cartel_members,k,min_val,max_val,max_bid_below_val)
        
            total_avg_utils_individuals +=  avg_utility_individuals
            total_avg_cartel_utils += avg_cartel_members_util
            total_leader_utils += cartel_leader_util
            total_cartel_wins_allruns +=total_cartel_wins

            if k<=theo_k:
                k_lt_ktheo+=1
        

        avg_avg_utils_individuals=total_avg_utils_individuals/runs
        avg_avg_cartel_utils=total_avg_cartel_utils/runs
        avg_leader_utils=total_leader_utils/runs
        avg_cartel_wins=total_cartel_wins_allruns/runs

        yAxis.append(avg_leader_utils)
        yKTheo.append(k_lt_ktheo)
        xAxis.append(k)

    if not hidePrints:

        print("================== ",runs," runs, k=",k," ==================")
    
        print("Avg of all runs (Avg utility of all non cartel members in a run) : ",avg_avg_utils_individuals)
        print("Avg of all runs (Avg utility of all cartel members in a run) : ",avg_avg_cartel_utils)
        print("Avg of cartel leader utility of all runs : ",avg_leader_utils)
        print("Avg of cartel wins of all runs : ",avg_cartel_wins,"\n")

    plt.figure()
    plt.plot(xAxis,yKTheo)
    plt.title("k <= k theoretical changing k")
    plt.savefig('./results/Result1_KTheo.png')

    plt.figure()
    plt.plot(xAxis,yAxis)
    plt.axhline(y = 0, color = 'r', linestyle = ':', label = "red line") 
    plt.title("Avg utility of leader changing k")
    plt.savefig('./results/Result1_LeaderUtil.png')
    plt.show()

def Vary_CM_at_Diff_K(hidePrints):
    objects = 10
    min_budget = 200
    max_budget = 300
    total_participants=20
    k=0.07
    runs=500

    min_val=50
    max_val=75
    max_bid_below_val=10

    print('============= Parameters =============')
    print('-- Objects in auction = ',objects,"\n")
    print('-- budget = uniform random (',min_budget,',',max_budget,")","\n")
    print('-- total participants(bidders) = ',total_participants,"\n")
    print('-- cartel members(excluding leader)(have highest budget) = 3 to 16',"\n")
    print('-- valuation = uniform random (',min_budget,',',max_budget,")","\n")
    print('-- Bid reduced from valuation by = uniform random (0,',max_budget,")","\n")
    print('-- k = 0.05, 0.07, 0.1',"\n\n")

    yAxis=[[],[],[]]
    xAxis=[]

    kArr=[0.05,0.07,0.1]

    yKTheo=[[],[],[]]

    for idx in range(0,3):
        cartel_members=3
        while (cartel_members<=16):
            cartel_members+=1
            k=kArr[idx]

            total_avg_utils_individuals=0
            total_avg_cartel_utils=0
            total_leader_utils = 0
            total_cartel_wins_allruns = 0

            k_lt_ktheo=0

            for i in range(runs):
                avg_utility_individuals,avg_cartel_members_util,cartel_leader_util,total_cartel_wins,theo_k = run_an_auction(objects,min_budget,max_budget,total_participants,cartel_members,k,min_val,max_val,max_bid_below_val)
        
                total_avg_utils_individuals +=  avg_utility_individuals
                total_avg_cartel_utils += avg_cartel_members_util
                total_leader_utils += cartel_leader_util
                total_cartel_wins_allruns +=total_cartel_wins

                if k<=theo_k:
                    k_lt_ktheo+=1
        

            avg_avg_utils_individuals=total_avg_utils_individuals/runs
            avg_avg_cartel_utils=total_avg_cartel_utils/runs
            avg_leader_utils=total_leader_utils/runs
            avg_cartel_wins=total_cartel_wins_allruns/runs

            yAxis[idx].append(avg_leader_utils)
            yKTheo[idx].append(k_lt_ktheo)
            if idx == 0:
                xAxis.append(cartel_members)
            
            if not hidePrints:

                print("================== ",runs," runs, k=",k,", cartel members = ",cartel_members," ==================")
    
                print("Avg of all runs (Avg utility of all non cartel members in a run) : ",avg_avg_utils_individuals)
                print("Avg of all runs (Avg utility of all cartel members in a run) : ",avg_avg_cartel_utils)
                print("Avg of cartel leader utility of all runs : ",avg_leader_utils)
                print("Avg of cartel wins of all runs : ",avg_cartel_wins,"\n")

    plt.figure()
    plt.plot(xAxis,yKTheo[0],label='k=0.05',color='blue')
    plt.plot(xAxis,yKTheo[1],label='k=0.07',color='green')
    plt.plot(xAxis,yKTheo[2],label='k=0.1',color='red')
    plt.title("k <= k theoretical changing cartel members at different k values")
    plt.savefig('./results/Result2_KTheo.png')

    plt.figure()
    plt.plot(xAxis,yAxis[0],label='k=0.05',color='blue')
    plt.plot(xAxis,yAxis[1],label='k=0.07',color='green')
    plt.plot(xAxis,yAxis[2],label='k=0.1',color='red')
    plt.title("Avg utility of leader changing cartel members at different k values")
    plt.savefig('./results/Result2_LeaderUtil.png')
    plt.show()


def VarySize(hidePrints):
    objects = 10
    min_budget = 200
    max_budget = 300
    total_participants=20
    cartel_members=10
    k=0.07
    runs=500

    min_val=50
    max_val=75
    max_bid_below_val=10

    yAxis=[]
    xAxis=[]

    yKTheo=[]

    print('============= Parameters =============')
    print('-- Objects in auction = ',objects,"\n")
    print('-- budget = uniform random (',min_budget,',',max_budget,")","\n")
    print('-- total participants(bidders) = 4 to 40 (cartel members * 2)',"\n")
    print('-- cartel members(excluding leader)(have highest budget) = 2 to 20',"\n")
    print('-- valuation = uniform random (',min_budget,',',max_budget,")","\n")
    print('-- Bid reduced from valuation by = uniform random (0,',max_budget,")","\n")
    print('-- k = 0.07',"\n\n")

    cartel_members=1
    while(cartel_members<=20):
        cartel_members+=1
        total_participants=cartel_members*2

        total_avg_utils_individuals=0
        total_avg_cartel_utils=0
        total_leader_utils = 0
        total_cartel_wins_allruns = 0

        k_lt_ktheo=0

        for i in range(runs):
            avg_utility_individuals,avg_cartel_members_util,cartel_leader_util,total_cartel_wins,theo_k = run_an_auction(objects,min_budget,max_budget,total_participants,cartel_members,k,min_val,max_val,max_bid_below_val)
        
            total_avg_utils_individuals +=  avg_utility_individuals
            total_avg_cartel_utils += avg_cartel_members_util
            total_leader_utils += cartel_leader_util
            total_cartel_wins_allruns +=total_cartel_wins

            if k<=theo_k:
                k_lt_ktheo+=1
        

        avg_avg_utils_individuals=total_avg_utils_individuals/runs
        avg_avg_cartel_utils=total_avg_cartel_utils/runs
        avg_leader_utils=total_leader_utils/runs
        avg_cartel_wins=total_cartel_wins_allruns/runs

        yAxis.append(avg_leader_utils)
        yKTheo.append(k_lt_ktheo)
        xAxis.append(total_participants)

    if not hidePrints:

        print("================== ",runs," runs, total participants=",total_participants,", cartel members= ",cartel_members," ==================")
    
        print("Avg of all runs (Avg utility of all non cartel members in a run) : ",avg_avg_utils_individuals)
        print("Avg of all runs (Avg utility of all cartel members in a run) : ",avg_avg_cartel_utils)
        print("Avg of cartel leader utility of all runs : ",avg_leader_utils)
        print("Avg of cartel wins of all runs : ",avg_cartel_wins,"\n")

    plt.figure()
    plt.plot(xAxis,yKTheo)
    plt.title("k <= k theoretical changing size of auction")
    plt.savefig('./results/Result3_KTheo.png')

    plt.figure()
    plt.plot(xAxis,yAxis)
    plt.axhline(y = 0, color = 'r', linestyle = ':', label = "red line") 
    plt.title("Avg utility of leader changing size of auction")
    plt.savefig('./results/Result3_LeaderUtil.png')
    plt.show()


def Cartel_NoCartel():
    objects = 10
    min_budget = 200
    max_budget = 300
    total_participants=20
    cartel_members=10
    k=0.07
    runs=500

    min_val=50
    max_val=75
    max_bid_below_val=10

    yAxis=[]
    xAxis=[]


    print('============= Parameters =============')
    print('-- Objects in auction = ',objects,"\n")
    print('-- budget = uniform random (',min_budget,',',max_budget,")","\n")
    print('-- total participants(bidders) = ',total_participants,"\n")
    print('-- cartel members(excluding leader)(have highest budget) = ',cartel_members,"\n")
    print('-- valuation = uniform random (',min_budget,',',max_budget,")","\n")
    print('-- Bid reduced from valuation by = uniform random (0,',max_budget,")","\n")
    print('-- k = 0.07',"\n\n")


    total_avg_utils_individuals=0
    total_avg_cartel_utils=0
    total_leader_utils = 0
    total_cartel_wins_allruns = 0

    for i in range(runs):
        avg_utility_individuals,avg_cartel_members_util,cartel_leader_util,total_cartel_wins,theo_k = run_an_auction(objects,min_budget,max_budget,total_participants,cartel_members,k,min_val,max_val,max_bid_below_val)
        
        total_avg_utils_individuals +=  avg_utility_individuals
        total_avg_cartel_utils += avg_cartel_members_util
        total_leader_utils += cartel_leader_util
        total_cartel_wins_allruns +=total_cartel_wins    

    avg_avg_utils_individuals=total_avg_utils_individuals/runs
    avg_avg_cartel_utils=total_avg_cartel_utils/runs
    avg_leader_utils=total_leader_utils/runs
    avg_cartel_wins=total_cartel_wins_allruns/runs

    print("+++++++++++++++++ CARTEL +++++++++++++++++")
    print("================== ",runs," runs, ==================")
    
    print("Avg of all runs (Avg utility of all non cartel members in a run) : ",avg_avg_utils_individuals)
    print("Avg of all runs (Avg utility of all cartel members in a run) : ",avg_avg_cartel_utils)
    print("Avg of cartel leader utility of all runs : ",avg_leader_utils)
    print("Avg of cartel wins of all runs : ",avg_cartel_wins,"\n\n")


    ## No cartel

    total_avg_utils_individuals=0
    total_avg_utils_wannabe_cartel=0

    for i in range(runs):
        avg_utility_individuals,avg_utility_wannabe_cartel = run_an_auction_NoCartel(objects,min_budget,max_budget,total_participants,cartel_members,k,min_val,max_val,max_bid_below_val)
        
        total_avg_utils_individuals +=  avg_utility_individuals
        total_avg_utils_wannabe_cartel += avg_utility_wannabe_cartel

    avg_avg_utils_individuals=total_avg_utils_individuals/runs
    avg_avg_utils_wannabe_cartel=total_avg_utils_wannabe_cartel/runs


    print("+++++++++++++++++ NO CARTEL +++++++++++++++++")
    print("================== ",runs," runs, ==================")
    
    print("Avg of all runs (Avg utility of all non cartel members in a run) : ",avg_avg_utils_individuals)
    print("Avg of all runs (Avg utility of all cartel members but not in a cartel in a run) : ",avg_avg_utils_wannabe_cartel,'\n\n')