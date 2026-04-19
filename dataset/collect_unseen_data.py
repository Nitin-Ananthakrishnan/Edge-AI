import cv2
import numpy as np
import os
import time
from pathlib import Path

# --- 1. CONFIGURATION ---
# Points to your existing folder. We will ADD to it, not delete.
TEST_SET_DIR = Path("pi_test_set") 
os.makedirs(TEST_SET_DIR, exist_ok=True)

CLASSES = ['Background', 'Hello', 'Yes', 'Thumbsup', 'Pointing', 'Raised', 'Pinch', 'Call', 'Peace', 'L']
THRESHOLD_T = 138.92 
NEW_SAMPLES_PER_CLASS = 20 # Number of images to capture per sign

def process_to_binary(frame):
    small = cv2.resize(frame, (640, 480))
    ycrcb = cv2.cvtColor(small, cv2.COLOR_BGR2YCrCb)
    cr = ycrcb[:, :, 1]
    _, mask = cv2.threshold(cr, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
    contours, _ = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    if contours:
        c = max(contours, key=cv2.contourArea)
        mask_temp = np.zeros_like(mask); cv2.drawContours(mask_temp, [c], -1, 255, -1)
        if cv2.mean(cr, mask=mask_temp)[0] > THRESHOLD_T and cv2.contourArea(c) > 2000:
            x, y, w, h = cv2.boundingRect(c)
            return cv2.resize(mask_temp[y:y+h, x:x+w], (96, 96))
    return np.zeros((96, 96), dtype=np.uint8)

# --- 2. MAIN LOOP ---
cap = cv2.VideoCapture(0) # Change to 1 for USB cam if needed

print("\n" + "="*50)
print("📸 INTERACTIVE 'S-TRIGGER' DATA COLLECTION")
print("="*50)

for label in CLASSES:
    print(f"\n▶️ TARGET GESTURE: [{label.upper()}]")
    print("  1. Position your hand in a NEW spot/angle.")
    print("  2. Watch the 'Mask Preview' window.")
    print("  3. Press 's' to capture burst.")
    print("  4. Press 'q' to skip class.")

    capturing = False
    count = 0

    while count < NEW_SAMPLES_PER_CLASS:
        ret, frame = cap.read()
        if not ret: break
        frame = cv2.flip(frame, 1) # Mirror for easy positioning
        
        # Live processing for preview
        processed_mask = process_to_binary(frame)
        
        # Visual UI
        preview_frame = frame.copy()
        cv2.putText(preview_frame, f"Gesture: {label}", (10, 30), 2, 0.7, (0, 255, 0), 2)
        
        if not capturing:
            cv2.putText(preview_frame, "READY: PRESS 'S' TO START", (10, 60), 2, 0.7, (0, 255, 255), 2)
        else:
            cv2.putText(preview_frame, f"CAPTURING: {count}/{NEW_SAMPLES_PER_CLASS}", (10, 60), 2, 0.7, (0, 0, 255), 2)

        # Show Windows
        cv2.imshow("1. Live Camera Feed", preview_frame)
        cv2.imshow("2. AI Perception Mask (96x96)", processed_mask)

        key = cv2.waitKey(1) & 0xFF
        
        # Trigger Logic
        if key == ord('s'):
            capturing = True
            print(f"  🔥 Burst starting for {label}...")

        if capturing:
            if np.max(processed_mask) > 0 or label == "Background":
                # Generate unique filename using timestamp to avoid overwriting old data
                filename = f"{label}_UNSEEN_{int(time.time()*1000)}.jpg"
                cv2.imwrite(str(TEST_SET_DIR / filename), processed_mask)
                count += 1
                time.sleep(0.05) # Small gap for natural hand shake variance
            else:
                cv2.putText(preview_frame, "SIGNAL LOST - POSITION HAND", (10, 90), 2, 0.5, (0,0,255), 1)

        if key == ord('q'): 
            print(f"  ⏭️ Skipping {label}")
            break

print("\n" + "="*50)
print(f"✅ SUCCESS: New data added to {TEST_SET_DIR.absolute()}")
print("="*50)

cap.release()
cv2.destroyAllWindows()