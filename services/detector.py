from ultralytics import YOLO
import torch
import time


class Detector:

    def __init__(self, model_name: str):

        # Select device
        self.device = 0 if torch.cuda.is_available() else "cpu"

        # Load model once
        self.model = YOLO(model_name)

        # Move model to GPU if available
        if torch.cuda.is_available():
            self.model.to(self.device)

    def track(self, frame, confidence):

        start = time.perf_counter()

        results = self.model.track(
            source=frame,
            conf=confidence,
            persist=True,
            tracker="bytetrack.yaml",
            device=self.device,
            half=torch.cuda.is_available(),   # FP16 on GPU
            verbose=False,
        )

        elapsed = (time.perf_counter() - start) * 1000

        print(f"YOLO + ByteTrack: {elapsed:.1f} ms")

        return results[0]