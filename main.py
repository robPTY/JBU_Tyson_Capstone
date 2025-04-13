import cv2
import time
import logging
from inference.database import DatabaseManager
from inference.inference_engine import InferenceEngine
from inference.utils import simulate_weight
from inference.utils import get_most_frequent_count, decision_algorithm, display_with_overlay

logging.getLogger("ultralytics").setLevel(logging.ERROR)

db_config = {
    "host": "localhost",
    "user": "root",
    "port": 3306,
    "password": "root",
    "database": "robertodb"
}

def main():
    db_manager = DatabaseManager(db_config)
    engine = InferenceEngine("best.pt")

    print("Starting nugget detection system...")
    print("Press 'S' to save a batch")
    print("Press 'ESC' to exit")

    batch_id = db_manager.get_next_sample_id()
    nugget_count_hashmap = {}

    cap = cv2.VideoCapture(0)
    if not cap.isOpened():
        print("Camera not working")
        return

    try:
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to grab frame")
                break

            start_time = time.time()
            detections = engine.run(frame)
            elapsed = time.time() - start_time

            # Getting the count of the nuggets detected
            current_count = len(detections.xyxy)
            if current_count > 0:
                print(f"Time to count: {elapsed:.4f} s | Nuggets: {current_count}")

            nugget_count_hashmap[current_count] = nugget_count_hashmap.get(current_count, 0) + 1
            validity = decision_algorithm(detections)

            # Geetting the validity status
            validity_save = "VALID" if validity else "INVALID"
            validity_text = "Valid Batch" if validity else "Invalid Batch"
            color = (0, 255, 0) if validity else (0, 0, 255)

            # Getting the estimated weight 
            estimated_weight = simulate_weight(current_count)
            weight_text = f"Weight: {estimated_weight} oz"
            height, width, _ = frame.shape

            # Annotate the frame with detections and overlay text
            frame = engine.annotate(frame, detections)
            frame = display_with_overlay(frame, f"Count: {current_count}", (10, 40))
            frame = display_with_overlay(frame, validity_text, (10, 80), color=color)
            frame = display_with_overlay(frame, weight_text, (width - 255, 40), color=(255, 255, 0))

            cv2.imshow("CAMERA", frame)
            key = cv2.waitKey(1) & 0xFF

            if key == ord("s"):
                most_frequent = get_most_frequent_count(nugget_count_hashmap)
                success = db_manager.save_batch(batch_id, most_frequent, estimated_weight, validity_save)
                if success:
                    print(f"Saved Batch {batch_id} ✅")
                    batch_id = db_manager.get_next_sample_id()
                    nugget_count_hashmap.clear()
            elif key == 27:
                break
    finally:
        cap.release()
        cv2.destroyAllWindows()
        db_manager.close()

if __name__ == "__main__":
    main()
