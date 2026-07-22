import time


class LoiteringDetector:
    """
    Tracks how long an object remains in a monitored area.
    """

    def __init__(self, threshold_seconds=30):

        self.threshold = threshold_seconds

        self.first_seen = {}

        self.alerted = set()

    def update(self, object_id):

        now = time.time()

        if object_id not in self.first_seen:

            self.first_seen[object_id] = now

            return False, 0

        duration = now - self.first_seen[object_id]

        if (
            duration >= self.threshold
            and object_id not in self.alerted
        ):

            self.alerted.add(object_id)

            return True, round(duration, 1)

        return False, round(duration, 1)

    def remove(self, active_ids):

        active_ids = set(active_ids)

        for object_id in list(self.first_seen.keys()):

            if object_id not in active_ids:

                self.first_seen.pop(object_id, None)

                self.alerted.discard(object_id)