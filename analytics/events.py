from collections import deque
from datetime import datetime


class EventManager:
    """
    Stores and manages surveillance events.

    Examples:
    - Line Crossing
    - Intrusion
    - Loitering
    - Speed Violation
    - Queue Alert
    """

    def __init__(self, max_events=500):

        self.events = deque(maxlen=max_events)

    def add_event(
        self,
        event_type,
        object_id=None,
        label=None,
        details=None,
    ):

        event = {
            "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
            "type": event_type,
            "object_id": object_id,
            "label": label,
            "details": details or {},
        }

        self.events.appendleft(event)

        return event

    def get_events(self):

        return list(self.events)

    def latest(self, count=10):

        return list(self.events)[:count]

    def clear(self):

        self.events.clear()

    def count(self):

        return len(self.events)

    def filter(self, event_type):

        return [
            event
            for event in self.events
            if event["type"] == event_type
        ]