from picamera2 import Picamera2
import cv2, time, struct, threading
from thea_rpi.network.client import TCPClient


class FrameSender:
    def __init__(self, send_event: threading.Event, client: TCPClient):
        self.send_event = send_event
        self.client = client
        self.camera = Picamera2()
        self.running = False


    def start(self) -> None:
        config = self.camera.create_video_configuration(main={"size": (640, 480)})
        self.camera.configure(config)
        self.camera.start()

        time.sleep(3)

        meta = self.camera.capture_metadata()
        self.camera.set_controls({
                                     "AwbEnable": False,
                                     "ColourGains": meta["ColourGains"],
                                     "AeEnable": False,
                                     "ExposureTime": meta["ExposureTime"],
                                     "AnalogueGain": meta["AnalogueGain"]
                                 })

        self.running = True


    def _send_frame(self) -> None:
        try:
            frame = self.camera.capture_array()
            frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
            frame = cv2.flip(frame, 1)
            result, encoded_img = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])
            if result:
                data = struct.pack('>d', time.monotonic()) + encoded_img.tobytes()
                self.client.send(data)
        except Exception:
            pass


    def run(self) -> None:
        for _ in range(10):
            self._send_frame()

        while self.running:
            self.send_event.wait()
            self.send_event.clear()
            self._send_frame()


    def stop(self) -> None:
        self.running = False
        self.camera.stop()


if __name__ == "__main__":
    pass
