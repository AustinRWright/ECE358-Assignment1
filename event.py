class Event:
    """Base event class"""
    time = 0
    kind = "none"
    
    def __init__(self, time, kind):
        self.time = time
        self.kind = kind

class ArrivalEvent(Event):
    """Arrival event class"""
    length = 0
    
    def __init__(self, time, length):
        super().__init__(time, "Arrival")
        self.length = length

class DepartureEvent(Event):
    def __init__(self, time):
        super().__init__(time, "Departure")

class ObserverEvent(Event):
    def __init__(self, time):
        super().__init__(time, "Observer")
