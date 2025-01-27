from threading import Lock
from queue import Queue

class PubSubManager:
    def __init__(self):
        self.subscribers = []
        self.lock = Lock()

    def subscribe(self):
        """Create a new queue for a subscriber."""
        queue = Queue()
        with self.lock:
            self.subscribers.append(queue)
        return queue

    def publish(self, message):
        """Publish a message to all subscribers."""
        with self.lock:
            for subscriber in self.subscribers:
                subscriber.put(message)

    def unsubscribe(self, queue):
        """Remove a subscriber's queue."""
        with self.lock:
            self.subscribers.remove(queue)

pubsub_manager = PubSubManager()
