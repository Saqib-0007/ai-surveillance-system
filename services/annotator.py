import cv2
import supervision as sv

from config import COUNTING_LINE


class FrameAnnotator:
    """
    Draws detections, labels and surveillance overlays.
    """

    def __init__(self):

        self.box_annotator = sv.BoxAnnotator()

        self.label_annotator = sv.LabelAnnotator()

    def annotate(
        self,
        frame,
        detections,
        labels,
        analytics=None,
    ):

        frame = self.box_annotator.annotate(
            scene=frame,
            detections=detections,
        )

        frame = self.label_annotator.annotate(
            scene=frame,
            detections=detections,
            labels=labels,
        )

        # -----------------------------
        # Counting Line
        # -----------------------------
        cv2.line(
            frame,
            COUNTING_LINE[0],
            COUNTING_LINE[1],
            (0, 255, 0),
            3,
        )

        # -----------------------------
        # Counters
        # -----------------------------
        if analytics is not None:

            cv2.putText(
                frame,
                f"IN : {analytics.get('in', 0)}",
                (20, 40),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 0),
                2,
            )

            cv2.putText(
                frame,
                f"OUT : {analytics.get('out', 0)}",
                (20, 80),
                cv2.FONT_HERSHEY_SIMPLEX,
                1,
                (0, 255, 255),
                2,
            )

        return frame