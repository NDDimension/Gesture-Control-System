import platform
import subprocess


class VolumeControl:
    def __init__(self):
        self.system = platform.system().lower()
        self.method = "fallback"
        self.current_volume = 50

        if self.system == "windows":
            try:
                from pycaw.pycaw import AudioUtilities, AudioEndpointVolume
                from comtypes import CLSCTX_ALL
                from ctypes import cast, POINTER

                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(
                    AudioEndpointVolume._iid_, CLSCTX_ALL, None
                )
                self.volume = cast(interface, POINTER(AudioEndpointVolume))
                self.method = "pycaw"
            except:
                print("⚠️ pycaw not installed. Install with: pip install pycaw")

    def set_volume(self, percent):
        percent = max(0, min(100, percent))
        if self.method == "pycaw":
            try:
                self.volume.SetMasterVolumeLevelScalar(percent / 100.0, None)
            except Exception as e:
                print(f"Volume error: {e}")
        self.current_volume = percent
        return percent
