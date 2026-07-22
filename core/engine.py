from core.state import PlaybackState
from services.camera import CameraService
from services.video_processor import VideoProcessor


class SurveillanceEngine:

    def __init__(
        self,
        model_name,
        confidence,
    ):

        self.processor = VideoProcessor(
            model_name=model_name,
            confidence=confidence,
        )

        self.capture = None

        self.state = PlaybackState.STOPPED

        self.video_info = None

    def open_video(self, path):

        self.capture = CameraService.open_video(path)

        self.video_info = CameraService.get_video_info(
            self.capture
        )

    def play(self):

        self.state = PlaybackState.PLAYING

    def pause(self):

        self.state = PlaybackState.PAUSED

    def stop(self):

        self.state = PlaybackState.STOPPED

        if self.capture:

            self.capture.release()

            self.capture = None

    def seek(self, frame_number):

        CameraService.seek_frame(
            self.capture,
            frame_number,
        )

    def get_current_frame(self):

        return CameraService.current_frame(
            self.capture
        )

    def read_frame(self):

        if self.capture is None:

            return None, None

        success, frame = self.capture.read()

        if not success:

            return None, None

        return self.processor.process_frame(frame)