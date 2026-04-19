import cv2
import os
import time

# --- CONFIGURATION ---
CLASS_NAME = "Call_outdoor" 
SAVE_FOLDER = f"dataset/{CLASS_NAME}"
TOTAL_IMAGES = 200  # Total images to capture
# ---------------------

os.makedirs(SAVE_FOLDER, exist_ok=True)
cap = cv2.VideoCapture(0)

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

print("\n--- SINGLE STAGE CAPTURE ---")
print("Setup: Use any background you want.")
print("Press 's' to START capturing.")

# Phase 1: Positioning
while True:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame, 1)

    msg = "PRESS 'S' TO START"
    cv2.putText(frame, msg, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
    cv2.imshow("Positioning", frame)

    key = cv2.waitKey(1)
    if key & 0xFF == ord('s'):
        break
    elif key & 0xFF == ord('q'):
        cap.release()
        cv2.destroyAllWindows()
        exit()

# Phase 2: Capturing
print(f"Capturing {TOTAL_IMAGES} images...")

current_count = 0
while current_count < TOTAL_IMAGES:
    ret, frame = cap.read()
    if not ret: break
    frame = cv2.flip(frame, 1)

    img_name = os.path.join(SAVE_FOLDER, f"{CLASS_NAME}_{current_count}.jpg")
    cv2.imwrite(img_name, frame)

    cv2.putText(frame, f"Saving: {current_count}/{TOTAL_IMAGES-1}", (10, 30),
                cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    cv2.imshow("Positioning", frame)

    current_count += 1
    time.sleep(0.05)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

print(f"\nSUCCESS: {TOTAL_IMAGES} images saved in {SAVE_FOLDER}")

cap.release()
cv2.destroyAllWindows()