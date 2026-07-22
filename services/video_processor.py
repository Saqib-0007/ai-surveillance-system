import supervision as sv

from analytics.metrics import Metrics
from services.annotator import FrameAnnotator
from services.detector import Detector


class VideoProcessor:

    def __init__(
        self,
        model_name: str,
        confidence: float,
    ):

        self.detector = Detector(model_name)
        self.metrics = Metrics()
        self.annotator = FrameAnnotator()
        self.confidence = confidence

    def process_frame(self, frame):

        # Detection + Tracking
        results = self.detector.track(
            frame,
            self.confidence,
        )

        # Update analytics first
        analytics = self.metrics.update(results)

        detections = sv.Detections.from_ultralytics(results)

        labels = []

        if results.boxes is not None and results.boxes.cls is not None:

            names = results.names
            classes = results.boxes.cls.int().tolist()

            if results.boxes.id is not None:

                ids = results.boxes.id.int().tolist()

                labels = [
                    f"ID {track_id} | {names[cls]}"
                    for track_id, cls in zip(ids, classes)
                ]

            else:

                labels = [
                    names[cls]
                    for cls in classes
                ]

        annotated = self.annotator.annotate(
            frame,
            detections,
            labels,
            analytics,
        )

        return annotated, analytics