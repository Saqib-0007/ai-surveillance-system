import cv2
import numpy as np
import streamlit as st
from streamlit_drawable_canvas import st_canvas


class DrawingManager:
    def __init__(self):
        pass

    def draw_line(self, frame):

        rgb = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)

        canvas = st_canvas(
            fill_color="rgba(0,0,0,0)",
            stroke_width=3,
            stroke_color="#ff0000",
            background_image=rgb,
            update_streamlit=True,
            height=rgb.shape[0],
            width=rgb.shape[1],
            drawing_mode="line",
            key="line_canvas",
        )

        if canvas.json_data is None:
            return None

        objects = canvas.json_data.get("objects", [])

        if len(objects) == 0:
            return None

        line = objects[-1]

        x1 = line["x"]
        y1 = line["y"]

        x2 = x1 + line["x2"]
        y2 = y1 + line["y2"]

        return (
            int(x1),
            int(y1),
            int(x2),
            int(y2),
        )