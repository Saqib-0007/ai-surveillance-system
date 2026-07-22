from pathlib import Path
import numpy as np
# =====================================
# Project Paths
# =====================================

BASE_DIR = Path(__file__).resolve().parent

INPUT_DIR = BASE_DIR / "input"
OUTPUT_DIR = BASE_DIR / "output"
MODELS_DIR = BASE_DIR / "models"
LOGS_DIR = BASE_DIR / "logs"

# =====================================
# Supported Models
# =====================================

YOLO_MODELS = {
    "YOLOv8n (Fast)": "yolov8n.pt",
    "YOLOv8s (Balanced)": "yolov8s.pt",
    "YOLOv8m (Recommended)": "yolov8m.pt",
    "YOLOv8l (Maximum Accuracy)": "yolov8l.pt",
}

DEFAULT_MODEL = "YOLOv8m (Recommended)"

DEFAULT_CONFIDENCE = 0.50

# =====================================================
# Line Crossing
# =====================================================

COUNTING_LINE = (
    (100, 350),   # Start point (x, y)
    (1100, 350),  # End point (x, y)
)

LINE_OFFSET = 10

# =====================================================
# Intrusion Zone
# =====================================================

INTRUSION_ZONE = [
    (300, 200),
    (900, 200),
    (900, 700),
    (300, 700),
]

# =====================================================
# Speed Estimation
# =====================================================

SPEED_DISTANCE_METERS = 10.0

SPEED_LINE_A = (
    (250, 250),
    (950, 250),
)

SPEED_LINE_B = (
    (250, 550),
    (950, 550),
)

# =====================================================
# Queue Monitoring Zone
# =====================================================

QUEUE_ZONE = np.array(
    [
        (150, 250),
        (500, 250),
        (500, 700),
        (150, 700),
    ],
    dtype=np.int32,
)