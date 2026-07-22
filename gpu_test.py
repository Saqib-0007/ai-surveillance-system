from ultralytics import YOLO
import torch

print("CUDA:", torch.cuda.is_available())
print("Device:", torch.cuda.get_device_name(0))

model = YOLO("yolov8l.pt")

results = model(
    "input/videos/traffic.mp4",
    device=0,
    stream=True,
)

for i, _ in enumerate(results):
    if i == 20:
        break

print("Inference completed.")