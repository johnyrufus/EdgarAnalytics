from session import Session

'''
Custom LRUQueue implementation with a doubly linked list of Sessions.
Most efficient as O(1) in moving the recently updated items to the front and
the expired sessions are checked from the back of the queue, until there are 
no more expired sessions.
'''
class LRUQueue:
    '''Initialize with the inactivity period and the doubly linked list'''
    def __init__(self, inactivity_period):
        self.lru_front, self.lru_back = Session(), Session()
        self.lru_front.next = self.lru_back
        self.lru_back.prev = self.lru_front
        self.inactivity_period = inactivity_period

    '''Update the queue with a list of recently accessed sessions'''
    def update(self, sessions):
        for session in sessions:
            self.move_to_front(session)

    '''Remove and return the expired sessions from the back of the queue'''
    def get_expired_sessions(self, time):
        res = []
        node = self.lru_back.prev
        while node != self.lru_front:
            prev = node.prev
            if (time - node.last_accessed).total_seconds() > self.inactivity_period:
                res.append(node)
                self.remove_node(node)
            node = prev
        return res

    '''Doubly Linked List helper methods'''
    def move_to_front(self, ptr):
        self.remove_node(ptr)
        self.insert_front(ptr)

    def insert_front(self, ptr):
        next = self.lru_front.next
        self.lru_front.next = ptr
        next.prev = ptr
        ptr.prev = self.lru_front
        ptr.next = next

    def remove_node(self, ptr):
        if not ptr.next or not ptr.prev:
            return
        prev, next = ptr.prev, ptr.next
        prev.next = next
        next.prev = prev
        ptr.prev, ptr.next = None, None

