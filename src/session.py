'''
Session class that stores the active session information for an IP
'''
class Session:
    def __init__(self, ip='', start=0, count=0):
        self.ip = ip
        self.start = start
        self.count = count
        self.last_accessed = start
        self.prev = None
        self.next = None

    def update(self, count, time):
        self.count += count
        self.last_accessed = time