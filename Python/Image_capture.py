import cv2
import os
import time

# --- CONFIGURATION ---
CLASS_NAME = "Yess" 
SAVE_FOLDER = f"dataset/{CLASS_NAME}"
ENV_LIMIT = 50         # Images per environment (Total will be 100)
# ---------------------

os.makedirs(SAVE_FOLDER, exist_ok=True)
cap = cv2.VideoCapture(1) 

if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

# We will run this twice: once for White wall, once for Brown wall
for stage in [1, 2]:
    print(f"\n--- STAGE {stage} OF 2 ---")
    if stage == 1:
        print("Setup: WHITE WALL background.")
    else:
        print("Setup: BROWN/OTHER WALL background.")
    
    print("Press 's' to START capturing this stage.")
    
    # Phase 1: Positioning for this stage
    while True:
        ret, frame = cap.read()
        if not ret: break
        frame = cv2.flip(frame, 1)
        
        msg = f"STAGE {stage}: PRESS 'S' TO START"
        cv2.putText(frame, msg, (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 255), 2)
        cv2.imshow("Positioning", frame)
        
        key = cv2.waitKey(1)
        if key & 0xFF == ord('s'):
            break
        elif key & 0xFF == ord('q'):
            cap.release()
            cv2.destroyAllWindows()
            exit()

    # Phase 2: Capturing for this stage
    print(f"Capturing {ENV_LIMIT} images...")
    
    # If stage 1, count starts at 0. If stage 2, count starts at 50.
    start_count = (stage - 1) * ENV_LIMIT
    end_count = start_count + ENV_LIMIT
    
    current_count = start_count
    while current_count < end_count:
        ret, frame = cap.read()
        if not ret: break
        frame = cv2.flip(frame, 1)
        
        # Save image with unique index
        img_name = os.path.join(SAVE_FOLDER, f"{CLASS_NAME}_{current_count}.jpg")
        cv2.imwrite(img_name, frame)
        
        # UI Feedback
        cv2.putText(frame, f"Saving: {current_count}/{end_count-1}", (10, 30), 
                    cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
        cv2.imshow("Positioning", frame)
        
        current_count += 1
        time.sleep(0.05) # Delay to allow slight hand movement
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
    
    print(f"Stage {stage} complete.")

print(f"\nSUCCESS: 100 images saved in {SAVE_FOLDER}")
cap.release()
cv2.destroyAllWindows()