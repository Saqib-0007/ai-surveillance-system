import time


class SpeedEstimator:
    """
    Estimates object speed using the time taken to
    travel between two virtual lines.
    """

    def __init__(self, distance_meters=10.0):

        self.distance = distance_meters

        self.line_a_times = {}

        self.speeds = {}

    def cross_line_a(self, object_id):

        if object_id not in self.line_a_times:

            self.line_a_times[object_id] = time.time()

    def cross_line_b(self, object_id):

        if object_id not in self.line_a_times:

            return None

        elapsed = time.time() - self.line_a_times[object_id]

        if elapsed <= 0:

            return None

        speed_mps = self.distance / elapsed
        speed_kmph = speed_mps * 3.6

        self.speeds[object_id] = round(speed_kmph, 2)

        del self.line_a_times[object_id]

        return self.speeds[object_id]

    def get_speed(self, object_id):

        return self.speeds.get(object_id)

    def remove(self, active_ids):

        active_ids = set(active_ids)

        for object_id in list(self.line_a_times.keys()):

            if object_id not in active_ids:

                self.line_a_times.pop(object_id, None)

        for object_id in list(self.speeds.keys()):

            if object_id not in active_ids:

                self.speeds.pop(object_id, None)