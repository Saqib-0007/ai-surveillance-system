import cv2


class CameraService:
    """
    Handles video, webcam and RTSP sources.
    """

    @staticmethod
    def open_video(video_path: str):

        capture = cv2.VideoCapture(video_path)

        if not capture.isOpened():
            raise ValueError(f"Unable to open video: {video_path}")

        return capture

    @staticmethod
    def open_webcam(camera_index: int = 0):

        capture = cv2.VideoCapture(camera_index)

        if not capture.isOpened():
            raise ValueError("Unable to open webcam.")

        return capture

    @staticmethod
    def open_rtsp(rtsp_url: str):

        capture = cv2.VideoCapture(rtsp_url)

        if not capture.isOpened():
            raise ValueError("Unable to connect to RTSP stream.")

        return capture

    @staticmethod
    def get_video_info(capture):

        fps = capture.get(cv2.CAP_PROP_FPS)

        total_frames = int(capture.get(cv2.CAP_PROP_FRAME_COUNT))

        width = int(capture.get(cv2.CAP_PROP_FRAME_WIDTH))

        height = int(capture.get(cv2.CAP_PROP_FRAME_HEIGHT))

        duration = total_frames / fps if fps > 0 else 0

        return {
            "fps": fps,
            "total_frames": total_frames,
            "width": width,
            "height": height,
            "duration": duration,
        }

    @staticmethod
    def seek_frame(capture, frame_number):

        capture.set(
            cv2.CAP_PROP_POS_FRAMES,
            frame_number,
        )

    @staticmethod
    def current_frame(capture):

        return int(
            capture.get(cv2.CAP_PROP_POS_FRAMES)
        )