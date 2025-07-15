import cv2
import pyttsx3

# Initialize text-to-speech engine
engine = pyttsx3.init()

def get_color_name(h, s, v):
    if v < 50:
        return "Black"
    if v > 200 and s < 30:
        return "White"
    if s < 40 and 50 <= v <= 200:
        return "Gray"

    if (h < 10) or (h > 160):
        if s > 100 and v > 100:
            return "Red"
        else:
            return "Brown"
    if 10 <= h <= 20:
        return "Orange"
    if 21 <= h <= 30:
        return "Yellow"
    if 31 <= h <= 85:
        return "Green"
    if 86 <= h <= 95:
        return "Cyan"
    if 96 <= h <= 125:
        return "Blue"
    if 126 <= h <= 145:
        return "Purple"
    if 146 <= h <= 160:
        return "Pink"
    return "Unknown"

# Open webcam
cap = cv2.VideoCapture(0)

# Store last spoken color to avoid repeating
last_spoken = None

while True:
    ret, frame = cap.read()
    if not ret:
        break

    # Flip frame horizontally for mirror view
    frame = cv2.flip(frame, 1)

    # Get frame dimensions
    height, width, _ = frame.shape
    cx, cy = width // 2, height // 2

    # Get BGR and HSV values at center
    pixel_bgr = frame[cy, cx]
    hsv_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)
    pixel_hsv = hsv_frame[cy, cx]
    h, s, v = pixel_hsv

    # Detect color name
    color_name = get_color_name(h, s, v)

    # Draw center marker
    cv2.circle(frame, (cx, cy), 10, (255, 255, 255), 2)

    # Display color name
    cv2.putText(frame, f"Color: {color_name}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    # Show RGB values for reference
    b, g, r = pixel_bgr
    cv2.putText(frame, f"RGB: ({r},{g},{b})", (10, 65),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255, 255, 255), 2)

    # Show video window
    cv2.imshow("Color Blindness Assistant", frame)

    # Speak color if changed
    if color_name != last_spoken and color_name != "Unknown":
        engine.say(color_name)
        engine.runAndWait()
        last_spoken = color_name

    # Quit on 'q'
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

cap.release()
cv2.destroyAllWindows()