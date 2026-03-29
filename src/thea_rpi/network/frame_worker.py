from picamera2 import Picamera2
import cv2, time
from thea_rpi.network.client import UDPClient


class FrameSender:
    def __init__(self):
        self.camera = Picamera2()
        self.client = UDPClient()
        self.running = False


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

        self.camera.set_controls({
                                     "AwbEnable": False,
                                     "ColourGains": controls[0],
                                     "AeEnable": False,
                                     "ExposureTime": controls[1],
                                     "AnalogueGain": controls[2]
                                 })

        self.camera.start()
        self.client.start()
        self.running = True


    def run(self) -> None:
        while self.running:
            try:
                frame = self.camera.capture_array()
                frame = cv2.cvtColor(frame, cv2.COLOUR_RGB2BGR)
                frame = cv2.flip(frame, 1)
                result, encoded_img = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])

                if result:
                    self.client.send(encoded_img.tobytes())
            
            except Exception:
                pass


    def stop(self) -> None:
        self.running = False
        self.client.close()
        self.camera.stop()


if __name__ == "__main__":
    pass
