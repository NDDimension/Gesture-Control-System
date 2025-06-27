import numpy as np
import screen_brightness_control as sbc
import time


class BrightnessControl:
    def __init__(self):
        self.last_update = 0
        self.update_delay = 0.2  # seconds

    def set_brightness(self, percent):
        now = time.time()
        if now - self.last_update < self.update_delay:
            return percent

        value = int(np.clip(percent, 0, 100))
        try:
            sbc.set_brightness(value)
        except Exception as e:
            print(f"Brightness error: {e}")
        self.last_update = now
        return value
