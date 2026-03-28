import time
from picamera2 import Picamera2

picam2 = Picamera2()

config = picam2.create_video_configuration(main={"size": (2592, 1944)})
picam2.configure(config)
picam2.start()

time.sleep(4)

meta = picam2.capture_metadata()

print("\n" + "="*40)
print("  MAX RESOLUTION CALIBRATION VALUES")
print("="*40)
print(f"ColourGains:  {meta['ColourGains']}")
print(f"ExposureTime: {meta['ExposureTime']}")
print(f"AnalogueGain: {meta['AnalogueGain']}")
print("="*40)

picam2.stop()
