import cv2
import numpy as np
import os

# ✅ NEW SPEAK FUNCTION (NO FREEZE ISSUE)
def speak(text):
    os.system(f'start /min powershell -c "Add-Type –AssemblyName System.Speech; '
              f'(New-Object System.Speech.Synthesis.SpeechSynthesizer).Speak(\'{text}\');"')

# Camera
camera = cv2.VideoCapture(0)
if not camera.isOpened():
    print("Cannot open camera")
    exit()

last_signal = ""

while True:
    ret, frame = camera.read()
    if not ret:
        break

    frame = cv2.resize(frame, (640, 480))
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Color masks
    red_mask = cv2.inRange(hsv, np.array([0,120,70]), np.array([10,255,255]))
    yellow_mask = cv2.inRange(hsv, np.array([20,100,100]), np.array([30,255,255]))
    green_mask = cv2.inRange(hsv, np.array([40,50,50]), np.array([90,255,255]))

    # Detection function
    def detect(mask):
        contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        for cnt in contours:
            if cv2.contourArea(cnt) > 500:
                return True
        return False

    current_signal = None

    # RED
    if detect(red_mask):
        current_signal = "STOP"
        cv2.putText(frame, "STOP", (50,50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,0,255), 2)

    # YELLOW
    elif detect(yellow_mask):
        current_signal = "WAIT"
        cv2.putText(frame, "WAIT", (50,50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,255), 2)

    # GREEN
    elif detect(green_mask):
        current_signal = "GO"
        cv2.putText(frame, "GO", (50,50),
                    cv2.FONT_HERSHEY_SIMPLEX, 1, (0,255,0), 2)

    # 🔊 VOICE LOGIC
    if current_signal is not None and current_signal != last_signal:
        speak(current_signal)
        last_signal = current_signal

    if current_signal is None:
        last_signal = ""   # reset when no color

    cv2.imshow("Traffic Detection", frame)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

camera.release()
cv2.destroyAllWindows()
