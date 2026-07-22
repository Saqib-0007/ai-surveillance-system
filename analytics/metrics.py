import time
from analytics.queue import QueueMonitor
from config import QUEUE_ZONE
from analytics.events import EventManager
from analytics.line_counter import LineCounter
from analytics.intrusion import IntrusionDetector
from analytics.loitering import LoiteringDetector
from analytics.speed import SpeedEstimator
from analytics.heatmap import HeatmapGenerator
from analytics.report import ReportGenerator
from config import (
    COUNTING_LINE,
    INTRUSION_ZONE,
    SPEED_DISTANCE_METERS,
)


class Metrics:

    VEHICLE_CLASSES = {
        "car",
        "truck",
        "bus",
        "motorcycle",
        "bicycle",
    }

    def __init__(self):

        self.frame_count = 0
        self.start_time = time.time()

        self.unique_people = set()
        self.unique_vehicles = set()
        self.report = ReportGenerator()
        self.events = EventManager()
        self.line_counter = LineCounter(COUNTING_LINE)
        self.intrusion = IntrusionDetector(INTRUSION_ZONE)
        self.loitering = LoiteringDetector(
            threshold_seconds=30
        )
        self.speed = SpeedEstimator(
            distance_meters=SPEED_DISTANCE_METERS
        )
        self.queue = QueueMonitor(QUEUE_ZONE)
        self.heatmap = None
               

    def update(self, results):

        self.frame_count += 1

        people = 0
        vehicles = 0

        names = results.names
        active_ids = []

        if results.boxes is not None:

            ids = results.boxes.id
            classes = results.boxes.cls
            boxes = results.boxes.xyxy

            if ids is not None:

                ids = ids.int().tolist()
                classes = classes.int().tolist()

                for i, (object_id, cls) in enumerate(zip(ids, classes)):

                    active_ids.append(object_id)

                    label = names[cls]

                    x1, y1, x2, y2 = boxes[i].tolist()

                    center = (
                        int((x1 + x2) / 2),
                        int((y1 + y2) / 2),
                    )

                    # -------------------------
                    # Heatmap
                    # -------------------------

                    if self.heatmap is None:

                        height, width = results.orig_img.shape[:2]

                        self.heatmap = HeatmapGenerator(
                            width,
                            height,
                        )

                    self.heatmap.update(center)

                    # -------------------------
                    # Intrusion
                    # -------------------------

                    intrusion = self.intrusion.update(
                        object_id,
                        center,
                    )

                    if intrusion["inside"]:
                    
                        alert, duration = self.loitering.update(
                            object_id
                        )

                        if alert:
                        
                            self.events.add_event(
                                event_type="Loitering",
                                object_id=object_id,
                                label=label,
                                details={
                                    "duration": f"{duration:.1f} sec"
                                },
                            )

                    else:
                    
                        self.loitering.remove([object_id])

                    # -------------------------
                    # Queue Monitoring
                    # -------------------------

                    in_queue, wait_time = self.queue.update(
                        object_id,
                        center,
                    )

                    if (
                        label == "person"
                        and in_queue
                        and wait_time >= 30
                    ):

                        self.events.add_event(
                            event_type="Queue",
                            object_id=object_id,
                            label=label,
                            details={
                                "wait": f"{wait_time:.1f} sec"
                            },
                        )                    

                    if intrusion["entered"]:

                        self.events.add_event(
                            event_type="Intrusion",
                            object_id=object_id,
                            label=label,
                            details={
                                "status": "Entered Zone"
                            },
                        )

                    elif intrusion["exited"]:

                        self.events.add_event(
                            event_type="Intrusion",
                            object_id=object_id,
                            label=label,
                            details={
                                "status": "Exited Zone"
                            },
                        )

                    # -------------------------
                    # Line Counter
                    # -------------------------

                    crossing = self.line_counter.update(
                        object_id,
                        center,
                    )

                    if crossing["crossed"]:

                        if crossing["direction"] == "IN":

                            self.speed.cross_line_a(object_id)

                        elif crossing["direction"] == "OUT":

                            speed = self.speed.cross_line_b(object_id)

                            if speed is not None:

                                self.events.add_event(
                                    event_type="Speed",
                                    object_id=object_id,
                                    label=label,
                                    details={
                                        "speed": f"{speed:.1f} km/h"
                                    },
                                )

                        self.events.add_event(
                            event_type="Line Crossing",
                            object_id=object_id,
                            label=label,
                            details={
                                "direction": crossing["direction"]
                            },
                        )

                    # -------------------------
                    # Detection Counts
                    # -------------------------

                    if label == "person":

                        people += 1

                        if object_id not in self.unique_people:

                            self.unique_people.add(object_id)

                            self.events.add_event(
                                event_type="Detection",
                                object_id=object_id,
                                label="person",
                            )

                    elif label in self.VEHICLE_CLASSES:

                        vehicles += 1

                        if object_id not in self.unique_vehicles:

                            self.unique_vehicles.add(object_id)

                            self.events.add_event(
                                event_type="Detection",
                                object_id=object_id,
                                label=label,
                            )
                            
        self.queue.remove(active_ids)
        self.speed.remove(active_ids)
        
        elapsed = time.time() - self.start_time
        fps = self.frame_count / elapsed if elapsed else 0
        counts = self.line_counter.get_counts()
        occupancy = self.intrusion.occupancy()
        queue_size = self.queue.queue_size()
        average_wait = self.queue.average_wait()        
               
        
        return {
            "people": people,
            "vehicles": vehicles,
            "unique_people": len(self.unique_people),
            "unique_vehicles": len(self.unique_vehicles),
            "fps": round(fps, 2),
            "frame": self.frame_count,
            "events": self.events.latest(25),
            "in": counts["in"],
            "out": counts["out"],
            "occupancy": occupancy,
            "heatmap": self.heatmap,
            "queue_size": queue_size,
            "average_wait": round(average_wait, 1),
        }