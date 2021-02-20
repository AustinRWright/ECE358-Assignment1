from DiscreteEventSimulator import MM1K_DES, DES_Result
TRANSMISSION_RATE = 1000000
AVERAGE_LENGTH = 2000
T = 1000

def main():
    print("Queue size, Queue Utilization, Average in Queue, Probability Loss")
    for k in [10, 25, 50]:
        # print("Size {}".format(k))
        for i in range(50, 151, 10):
            des = MM1K_DES((i/100), TRANSMISSION_RATE, AVERAGE_LENGTH, T, k)
            result = des.simulate()
            print("{},{},{},{}".format(k, result.queueUtilization, result.avgInQ, result.probLoss))

if __name__ == "__main__":
    main()