import cv2
import mediapipe as mp
import time
import numpy as np
import math
import pyautogui
from ctypes import cast, POINTER
from comtypes import CLSCTX_ALL
from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume
import screen_brightness_control as sbc


class GestureControlSystem:
    def __init__(self):
        self.hands = mp.solutions.hands.Hands(
            static_image_mode=False,
            max_num_hands=2,
            min_detection_confidence=0.8,
            min_tracking_confidence=0.7,
        )
        self.drawing = mp.solutions.drawing_utils
        self.style = mp.solutions.drawing_styles
        self.volume = 50
        self.brightness = 50

        # System volume setup
        devices = AudioUtilities.GetSpeakers()
        interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
        self.volume_ctrl = cast(interface, POINTER(IAudioEndpointVolume))
        vol_range = self.volume_ctrl.GetVolumeRange()
        self.minVol, self.maxVol = vol_range[0], vol_range[1]

    def distance(self, p1, p2, shape):
        h, w = shape[:2]
        x1, y1 = int(p1.x * w), int(p1.y * h)
        x2, y2 = int(p2.x * w), int(p2.y * h)
        return math.hypot(x2 - x1, y2 - y1), (x1, y1), (x2, y2)

    def draw_glow_effect(self, img, p1, p2):
        for thickness in range(8, 1, -2):
            alpha = thickness / 8
            color = (int(255 * alpha), int(255 * alpha), 255)
            cv2.line(img, p1, p2, color, thickness)
        for r in [30, 20, 10]:
            cv2.circle(img, p1, r, (255, 255, 255), -1)
            cv2.circle(img, p2, r, (255, 255, 255), -1)
        cv2.circle(img, p1, 6, (0, 0, 0), -1)
        cv2.circle(img, p2, 6, (0, 0, 0), -1)

    def draw_horizontal_bar(self, img, x, y, w, h, percent, label):
        radius = h // 2
        smooth_fill = int(w * percent / 100)
        overlay = img.copy()
        cv2.rectangle(overlay, (x, y), (x + w, y + h), (20, 20, 20), -1, cv2.LINE_AA)
        cv2.rectangle(
            overlay, (x, y), (x + smooth_fill, y + h), (50, 200, 100), -1, cv2.LINE_AA
        )
        cv2.addWeighted(overlay, 0.85, img, 0.15, 0, img)
        cv2.circle(img, (x, y + radius), radius, (50, 200, 100), -1)
        cv2.circle(img, (x + smooth_fill, y + radius), radius, (50, 200, 100), -1)
        cv2.putText(
            img,
            f"{label}: {int(percent)}%",
            (x, y - 10),
            cv2.FONT_HERSHEY_SIMPLEX,
            0.65,
            (255, 255, 255),
            2,
        )

    def draw_instructions(self, img):
        overlay = img.copy()
        cv2.rectangle(overlay, (10, 10), (350, 150), (0, 0, 0), -1)
        cv2.addWeighted(overlay, 0.5, img, 0.5, 0, img)
        lines = [
            "GESTURE CONTROLS:",
            " Raise hand to activate",
            " Left Pinch - Volume",
            " Right Pinch - Brightness",
            " Press 'Q' to Quit",
        ]
        for i, line in enumerate(lines):
            font_scale = 0.65 if i else 0.7
            color = (0, 255, 255) if i == 0 else (255, 255, 255)
            cv2.putText(
                img,
                line,
                (20, 40 + i * 24),
                cv2.FONT_HERSHEY_DUPLEX,
                font_scale,
                color,
                2,
            )

    def run(self):
        cap = cv2.VideoCapture(0)
        cap.set(3, 1280)
        cap.set(4, 720)
        print("\n🚀 Gesture UI Ready (Swipe Disabled)\n")

        while cap.isOpened():
            ret, img = cap.read()
            if not ret:
                continue
            img = cv2.flip(img, 1)
            rgb = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
            results = self.hands.process(rgb)

            if results.multi_hand_landmarks and results.multi_handedness:
                for lm, handness in zip(
                    results.multi_hand_landmarks, results.multi_handedness
                ):
                    label = handness.classification[0].label
                    hand_type = "Left" if label == "Right" else "Right"

                    self.drawing.draw_landmarks(
                        img,
                        lm,
                        mp.solutions.hands.HAND_CONNECTIONS,
                        self.style.get_default_hand_landmarks_style(),
                        self.style.get_default_hand_connections_style(),
                    )

                    dist, p1, p2 = self.distance(
                        lm.landmark[4], lm.landmark[8], img.shape
                    )
                    self.draw_glow_effect(img, p1, p2)
                    value = np.interp(dist, [50, 220], [0, 100])

                    if hand_type == "Left":
                        self.volume = 0.9 * self.volume + 0.1 * value
                        db = np.interp(
                            self.volume, [0, 100], [self.minVol, self.maxVol]
                        )
                        self.volume_ctrl.SetMasterVolumeLevel(db, None)
                    elif hand_type == "Right":
                        self.brightness = 0.9 * self.brightness + 0.1 * value
                        try:
                            sbc.set_brightness(int(self.brightness))
                        except Exception as e:
                            print("Brightness error:", e)

            self.draw_horizontal_bar(img, 60, 620, 350, 35, self.volume, "Volume")
            self.draw_horizontal_bar(
                img, 440, 620, 350, 35, self.brightness, "Brightness"
            )
            self.draw_instructions(img)

            cv2.imshow("Gesture Control Pro", img)
            if cv2.waitKey(1) & 0xFF == ord("q"):
                break

        cap.release()
        cv2.destroyAllWindows()


if __name__ == "__main__":
    gesture_ui = GestureControlSystem()
    gesture_ui.run()
