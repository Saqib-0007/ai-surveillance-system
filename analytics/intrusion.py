import cv2
import numpy as np


class IntrusionDetector:
    """
    Detects whether tracked objects enter or leave
    a polygon zone.
    """

    def __init__(self, polygon):

        self.polygon = np.array(
            polygon,
            dtype=np.int32,
        )

        self.inside_objects = set()

    def update(self, object_id, center):

        point = (
            float(center[0]),
            float(center[1]),
        )

        inside = (
            cv2.pointPolygonTest(
                self.polygon,
                point,
                False,
            )
            >= 0
        )

        entered = False
        exited = False

        if inside and object_id not in self.inside_objects:

            self.inside_objects.add(object_id)

            entered = True

        elif (
            not inside
            and object_id in self.inside_objects
        ):

            self.inside_objects.remove(object_id)

            exited = True

        return {
            "inside": inside,
            "entered": entered,
            "exited": exited,
        }

    def occupancy(self):

        return len(self.inside_objects)