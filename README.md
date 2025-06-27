# 🤖 Gesture Control Pro

Imagine a world where your hand movements replace buttons, sliders, and clicks.  
**Gesture Control Pro** turns your hand into a natural interface — to control volume, brightness, and even switch apps — all without touching your keyboard or mouse.

It’s not just software. It’s a new way to interact with your PC.

# [VIDEO Preview](/Gesture%20Control%20Pro%202025-06-27%2011-31-19.mp4)

## Image Preview 

![img](/image.png)



## 🌟 What Drives This

We believe interaction should be as effortless as motion itself.

With Gesture Control Pro:
> You don’t use your hand to click —  
> You use it to command.

The idea is simple: let your gestures do the talking.

## Media Pipe Hands Mapping

![map](/hand_landmarks_docs.png)



## 🧠 How It Works

1. You raise your hand in front of your webcam 📷  
2. Our system detects your fingertips and tracks movement using **MediaPipe** 🖐️  
3. **OpenCV** visualizes and interprets these landmarks in real time  
4. Your finger distance and direction are translated into system commands with **pycaw** and **screen_brightness_control**

⚡ All of this happens in milliseconds.



## 🧰 What Can You Do?

| Gesture                   | Action                             |
|---------------------------|-------------------------------------|
| 🤏 Left-hand pinch         | Adjust system volume 🎚             |
| 🤏 Right-hand pinch        | Control screen brightness 💡        |
| ❌ Press `Q`               | Exit gesture system gracefully 🛑  |

No need to memorize shortcuts. Just gesture and go.

---

## 🔍 What's Inside

- `main.py` – Core logic to process gestures and respond with system actions
- Real-time **gesture UI** with glowing highlights, sliders, and app switch ring
- `pycaw` + `screen_brightness_control` for full system control
- **Modular Functions**, clean structure to let you extend features easily




## 📦 Requirements

```txt
opencv-python
mediapipe
pycaw
screen_brightness_control
numpy
pyautogui
comtypes
```



## ⚙️ Getting Started

1. **Clone the repository**
```bash
git clone https://github.com/NDDimension/Gesture-Control-System.git
cd Gesture-Control-System
```

2. **Install all required packages**
```bash
pip install -r requirements.txt
```

3. **Run the gesture system**
```bash
python main.py
```

4. **Control your PC with just your hand**



## ✨ Why It Stands Out

- ✅ Beautiful, intuitive UI with glowing feedback
- ✅ Real-time system control with high precision
- ✅ Fully hands-free and no physical input devices required
- ✅ Easily customizable and extendable for new gestures



## 🔮 What’s Coming

- 🔧 On-screen gesture editor
- 🎵 Media controls (play/pause, next/prev)
- 🧠 AI gesture adaptation based on personal usage
- 🌈 Dark/light themes for day or night use
- 💻 Multi-platform support (Linux/macOS)



## 🙏 Credits

- 👨‍💻 Built from the ground up by Pratham Bhatnagar
- 🛠️ Powered by:
  - [MediaPipe](https://google.github.io/mediapipe/)
  - [OpenCV](https://opencv.org/)
  - [pycaw](https://github.com/AndreMiras/pycaw)
  - [screen_brightness_control](https://pypi.org/project/screen-brightness-control/)



## 📜 License

Licensed under the [MIT License](LICENSE).



> **Gesture Control Pro** — where your movements meet meaning.
