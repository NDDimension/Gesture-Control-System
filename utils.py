import math
import time


def count_fingers(lmList):
    fingers = []

    # Thumb (works for both hands)
    if (lmList[4][1] > lmList[3][1] and lmList[4][1] > lmList[2][1]) or (
        lmList[4][1] < lmList[3][1] and lmList[4][1] < lmList[2][1]
    ):
        fingers.append(1)
    else:
        fingers.append(0)

    # Other fingers
    tips_ids = [8, 12, 16, 20]
    for tip_id in tips_ids:
        if lmList[tip_id][2] < lmList[tip_id - 2][2]:
            fingers.append(1)
        else:
            fingers.append(0)

    return sum(fingers)


def is_wave(prev_pos, curr_pos, threshold=40, cooldown=1.0):
    if prev_pos is None or curr_pos is None:
        return False
    dx = curr_pos[0] - prev_pos[0]
    return abs(dx) > threshold
