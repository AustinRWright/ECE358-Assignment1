from DiscreteEventSimulator import MM1_DES, DES_Result
TRANSMISSION_RATE = 1000000
AVERAGE_LENGTH = 2000
T = 1000

def main():
    print("Queue Utilization, Average in Queue, Proportion Idle")
    des = MM1_DES(1.2, TRANSMISSION_RATE, AVERAGE_LENGTH, T)
    result = des.simulate()
    print("{},{},{}".format(result.queueUtilization, result.avgInQ, result.probIdle))

if __name__ == "__main__":
    main()
