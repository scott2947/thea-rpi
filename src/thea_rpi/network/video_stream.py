from picamera2 import Picamera2
import cv2
from thea_rpi.network.client import UDPClient


class VideoSender:

    def __init__(self):
        self.camera = Picamera2()
        self.client = UDPClient()


    def stream(self) -> None:

        self.camera.start()
        self.client.start()

        print("Streaming started. Press Ctrl+C to stop")

        try:
            while True:
                frame = self.camera.capture_array()
                frame = cv2.cvtColor(frame, cv2.COLOR_RGB2BGR)
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
    cam = VideoSender()
    cam.stream()
