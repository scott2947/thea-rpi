from picamera2 import Picamera2
import cv2, time
from thea_rpi.network.client import UDPClient


class FrameSender:
    def __init__(self):
        self.camera = Picamera2()
        self.client = UDPClient()


    def _tune(self) -> tuple[tuple[float, float], int, float]:
        config = self.camera.create_video_configuration(main={"size": (640, 480)})
        self.camera.configure(config)
        
        self.camera.start()

        time.sleep(3)

        meta = self.camera.capture_metadata()

        self.camera.stop()

        return (meta["ColourGains"], meta["ExposureTime"], meta["AnalogueGain"])


    def start(self) -> None:
        controls = self._tune()

        config = self.camera.create_video_configuration(main={"size": (640, 480)})
        self.camera.configure(config)
