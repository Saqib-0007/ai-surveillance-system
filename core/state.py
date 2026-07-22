from enum import Enum


class PlaybackState(Enum):
    """
    Represents the current playback state.
    """

    STOPPED = "Stopped"
    PLAYING = "Playing"
    PAUSED = "Paused"