import sys, random, math, statistics

def expRV(lam):
    """Generate exponential random variable"""
    U = random.random()
    x = -1 * (1/lam) * math.log(1 - U)
    return x

def main(num = 1000):
    print("Generating {} exponential RVs".format(num))
    random.seed()
    rvX = []
    for i in range(0, num):
        rvX.append(expRV(75))

    print("Mean: {}".format(statistics.mean(rvX)))
    print("Variance: {}".format(statistics.variance(rvX)))

if __name__ == "__main__":
    main()
