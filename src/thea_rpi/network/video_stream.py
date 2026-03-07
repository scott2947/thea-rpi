from picamera2 import Picamera2
import cv2
from thea_rpi.network.client import UDPClient


class VideoSender:

    def __init__(self):
        self.camera = Picamera2()
        config = self.camera.create_video_configuration(main={"size": (640, 480)})
        self.camera.configure(config)
        self.camera.set_controls({
                                     "AwbEnable": False,
                                     "ColourGains": (1.393507719039917, 1.3565787076950073),
                                     "AeEnable": False,
                                     "ExposureTime": 59967,
                                     "AnalogueGain": 1.0
                                 })
        
        self.client = UDPClient()


    def stream(self) -> None:

        self.camera.start()
        self.client.start()

        print("Streaming started. Press Ctrl+C to stop")

        try:
            while True:
                frame = self.camera.capture_array()
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
                frame = cv2.flip(frame, 1)
                result, encoded_img = cv2.imencode(".jpg", frame, [int(cv2.IMWRITE_JPEG_QUALITY), 80])

                if result:
                    self.client.send(encoded_img.tobytes())

        except KeyboardInterrupt:
            print("Streaming stopped by user")
        except Exception as e:
            print(f"Error during streaming: {e}")
        finally:
            self.camera.stop()
            self.client.close()


if __name__ == "__main__":
    vs = VideoSender()
    vs.stream()
