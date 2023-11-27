from runners import run_an_auction,Vary_CM_at_Diff_K,VaryK,VarySize,Cartel_NoCartel

if __name__ == "__main__":
    print("=========== Game Theory Project ===========\n")
    print("=========== Collusion in Auctions ===========\n")
    print("Choose Which Result to view: (1-4) \n")
    print("1) Cartel Leader Utility, K<=K theoretical Varying K \n")
    print("2) Cartel Leader Utility, K<=K theoretical Varying Cartel Members at different K \n")
    print("3) Cartel Leader Utility, K<=K theoretical Varying Auction Size at ratio cartel members = 1/2 total participants \n")
    print("4) Cartel Vs No Cartel utility of same people with highest budget. \n")
    
    res = input('Choose (1-4): ')
    print('\n')

    hideRes = "1"
    if int(res) < 4:
        hideRes =  input('Hide the print of each 500 simulation  Yes(1) No(0) : ')
        print('\n')

    if res=="1":
        VaryK(hideRes=="1")
    elif res=="2":
        Vary_CM_at_Diff_K(hideRes=="1")
    elif res=="3":
        VarySize(hideRes=="1")
    elif res=="4":
        Cartel_NoCartel()