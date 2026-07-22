import time
import cv2


class QueueMonitor:

    def __init__(self, zone):

        self.zone = zone
        self.waiting = {}

    def _inside(self, point):

        return (
            cv2.pointPolygonTest(
                self.zone,
                point,
                False,
            ) >= 0
        )

    def update(self, object_id, center):

        now = time.time()

        if self._inside(center):

            if object_id not in self.waiting:

                self.waiting[object_id] = now

            return (
                True,
                now - self.waiting[object_id],
            )

        self.waiting.pop(object_id, None)

        return False, 0

    def remove(self, active_ids):

        self.waiting = {
            k: v
            for k, v in self.waiting.items()
            if k in active_ids
        }

    def queue_size(self):

        return len(self.waiting)

    def average_wait(self):

        if not self.waiting:
            return 0

        now = time.time()

        waits = [
            now - t
            for t in self.waiting.values()
        ]

        return sum(waits) / len(waits)