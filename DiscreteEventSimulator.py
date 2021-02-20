import random, math, collections
from event import Event, ArrivalEvent, DepartureEvent, ObserverEvent

class DES_Result():
    queueUtilization = 0.25
    avgInQ = 0.0
    probIdle = 0.0
    probLoss = 0.0

    def __init__(self, queueUtilization, avgInQ, probIdle, probLoss):
        self.queueUtilization = queueUtilization
        self.avgInQ = avgInQ
        self.probIdle = probIdle
        self.probLoss = probLoss

class MM_Base_DES():
    avgLength = 0 # Average packet length
    transmissionRate = 0.0 # Transmission rate of the output link in bits per second
    queueUtilization = 0.0 # Utilization of the queue
    packetsPerSec = 0.0 # Average number of packets arrived per second
    observerPerSec = 0.0 # Average number of observation events per second
    tMax = 0 # Total simulation time
    events = collections.deque() # Event list
    q = collections.deque() # Queued packet list

    def __init__(self, queueUtilization, transmissionRate, avgLength, tMax):
        random.seed()
        self.queueUtilization = queueUtilization
        self.transmissionRate = transmissionRate
        self.avgLength = avgLength
        self.tMax = tMax
        self.packetsPerSec = (queueUtilization * transmissionRate) / avgLength
        self.observerPerSec = 5 * self.packetsPerSec

    def expRV(self, lam):
        """Generate exponential random variable"""
        U = random.random()
        x = -1 * (1/lam) * math.log(1 - U)
        return x

    def generateArrivalEvents(self):
        events = []
        arrivalTime = 0
        while True:
            arrivalTime += self.expRV(self.packetsPerSec)
            if arrivalTime > self.tMax:
                break
            event = ArrivalEvent(arrivalTime, round(self.expRV(1/self.avgLength)))
            events.append(event)
        return events

    def generateObserverEvents(self):
        events = []
        observerTime = 0
        while True:
            observerTime += self.expRV(self.observerPerSec)
            if observerTime > self.tMax:
                break
            event = ObserverEvent(observerTime)
            events.append(event)
        return events

    def generateEvents(self):
        events = []
        events.extend(self.generateArrivalEvents())
        events.extend(self.generateObserverEvents())
        events.sort(key=lambda x: x.time)
        self.events.clear()
        self.events.extend(events)

    def simulate(self):
        self.generateEvents()
        self.q.clear()

        numArrivals = 0
        numDepartures = 0
        numObservations = 0

        qCount = 0
        idleCount = 0
        fullCount = 0

        while len(self.events) > 0:
            event = self.events.popleft()
            if event.time > self.tMax:
                break
            if isinstance(event, ArrivalEvent):
                numArrivals += 1
                if len(self.q) == 0:
                    # create departure event
                    self.q.append(event.length)
                    transmissionTime = event.length / self.transmissionRate
                    depTime = event.time + transmissionTime
                    self.insertDepartureEvent(depTime)
                elif not self.isQueueFull():
                    # add to Queue
                    self.q.append(event.length)
                #else drop packet

            elif isinstance(event, DepartureEvent):
                numDepartures += 1
                self.q.popleft()
                if len(self.q) > 0:
                    length = self.q[0]
                    transmissionTime = length / self.transmissionRate
                    depTime = event.time + transmissionTime
                    self.insertDepartureEvent(depTime)

            elif isinstance(event, ObserverEvent):
                numObservations += 1
                qCount += len(self.q)
                if self.isQueueFull():
                    fullCount += 1
                elif len(self.q) == 0:
                    idleCount += 1

        avgInQ = qCount / numObservations
        probIdle = idleCount / numObservations
        probLoss = fullCount / numObservations
        return DES_Result(self.queueUtilization, avgInQ, probIdle, probLoss)


    def isQueueFull(self):
        pass

    def insertDepartureEvent(self, time):
        for i in range(0, len(self.events)):
            if self.events[i].time >= time:
                self.events.insert(i, DepartureEvent(time))
                return
        # append if end is reached
        self.events.append(DepartureEvent(time))



class MM1_DES(MM_Base_DES):
    def isQueueFull(self):
        return False

class MM1K_DES(MM_Base_DES):
    maxQueueSize = 0
    def __init__(self, queueUtilization, transmissionRate, avgLength, tMax, maxQueueSize):
        super().__init__(queueUtilization, transmissionRate, avgLength, tMax)
        self.maxQueueSize = maxQueueSize

    def isQueueFull(self):
        if len(self.q) == self.maxQueueSize:
            return True
        elif len(self.q) < self.maxQueueSize:
            return False
        else:
            raise Exception("Invalid State: Queue overfull")
