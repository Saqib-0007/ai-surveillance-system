import cv2
import numpy as np


class HeatmapGenerator:
    """
    Generates a movement heatmap from tracked object centers.
    """

    def __init__(self, width, height):

        self.width = width
        self.height = height

        self.heatmap = np.zeros(
            (height, width),
            dtype=np.float32,
        )

    def update(self, center):

        x, y = center

        if (
            0 <= x < self.width
            and 0 <= y < self.height
        ):
            cv2.circle(
                self.heatmap,
                (x, y),
                20,
                1,
                -1,
            )

    def overlay(
        self,
        frame,
        alpha=0.45,
    ):

        normalized = cv2.normalize(
            self.heatmap,
            None,
            0,
            255,
            cv2.NORM_MINMAX,
        ).astype(np.uint8)

        colored = cv2.applyColorMap(
            normalized,
            cv2.COLORMAP_JET,
        )

        return cv2.addWeighted(
            frame,
            1 - alpha,
            colored,
            alpha,
            0,
        )

    def reset(self):

        self.heatmap.fill(0)