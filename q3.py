from DiscreteEventSimulator import MM1_DES, DES_Result
TRANSMISSION_RATE = 1000000
AVERAGE_LENGTH = 2000
T = 1000

def main():
    print("Queue Utilization, Average in Queue, Proportion Idle")
    for i in range(25, 96, 10):
        des = MM1_DES((i/100), TRANSMISSION_RATE, AVERAGE_LENGTH, T)
        result = des.simulate()
        print("{},{},{}".format(result.queueUtilization, result.avgInQ, result.probIdle))

if __name__ == "__main__":
    main()
