import cv2
import supervision as sv
import mariadb
from ultralytics import YOLO
import time
import logging

logging.getLogger("ultralytics").setLevel(logging.ERROR)

# Database Information
db_config = {
    "host": "localhost",
    "user": "root",
    "port": 3306,
    "password": "root",
    "database": "robertodb"
}

class DatabaseManager:
    def __init__(self, config):
        self.config = config
        self.connection = None
        self.cursor = None

    def connect(self):
        try:
            self.connection = mariadb.connect(**self.config)
            self.connection.autocommit = True  
            self.cursor = self.connection.cursor()
            return True
        except mariadb.Error as e:
            print(f"Error connecting to database: {e}")
            return False

    def get_last_sample_id(self):
        try:
            if not self.connection:
                if not self.connect():
                    return 0

            self.cursor.execute("SELECT MAX(Sample_ID) FROM FullBatch_tab")
            result = self.cursor.fetchone()[0]
            try:
                return int(result) if result is not None else 0
            except (ValueError, TypeError):
                return 0
        except mariadb.Error as e:
            print(f"Error getting last sample ID: {e}")
            return 0
        except Exception as e:
            print(f"Unexpected error while getting last sample ID: {e}")
            return 0

    def save_batch(self, sample_id, nugget_count, batch_weight, batch_validity):
        try:
            if not self.connection:
                if not self.connect():
                    return False

            insert_query = """
            INSERT INTO Fullbatch_tab (Sample_ID, Nugget_Count, Batch_weight, Batch_validity)
            VALUES (?, ?, ?, ?)
            """
            self.cursor.execute(insert_query, (str(sample_id), nugget_count, batch_weight, batch_validity))
            self.connection.commit()
            print(f"Rows affected: {self.cursor.rowcount}")
            return True
        except mariadb.Error as e:
            print(f"Error saving batch to database: {e}")
            return False
        except Exception as e:
            print(f"Unexpected error: {e}")
            return False

    def close(self):
        if self.cursor:
            self.cursor.close()
        if self.connection:
            self.connection.close()

def get_most_frequent_count(hashmap):
    if not hashmap:
        return 0
    return max(hashmap.items(), key=lambda x: x[1])[0]

def decision_algorithm(detections, avg_size=85, tolerance=0.8):
    if len(detections.xyxy) < 5:
        return False
    
    valid_nugget_count = 0
    total_nuggets = len(detections.xyxy)
    min_size = avg_size * 0.6  # 40% smaller than average
    max_size = avg_size * 1.4  # 40% larger than average
    
    for box in detections.xyxy:
        x_min, y_min, x_max, y_max = box
        width = x_max - x_min
        height = y_max - y_min
        largest_dimension = max(width, height)
        
        if min_size <= largest_dimension <= max_size:
            valid_nugget_count += 1 
    
    # If at least one nugget is valid OR majority of nuggets are valid, accept batch
    return valid_nugget_count > 0 and (valid_nugget_count / total_nuggets) >= (1 - tolerance)


def display_with_overlay(image, text, position, font=cv2.FONT_HERSHEY_SIMPLEX, font_scale=1, color=(0, 255, 0), thickness=2):
    # Get text size to adjust background rectangle
    text_size = cv2.getTextSize(text, font, font_scale, thickness)[0]
    padding = 10
    text_x, text_y = position
    bg_x1, bg_y1 = text_x - padding, text_y - text_size[1] - padding
    bg_x2, bg_y2 = text_x + text_size[0] + padding, text_y + padding

    # Create semi-transparent overlay
    overlay = image.copy()
    cv2.rectangle(overlay, (bg_x1, bg_y1), (bg_x2, bg_y2), (0, 0, 0), cv2.FILLED)
    image = cv2.addWeighted(overlay, 0.5, image, 0.5, 0)  # Blend with transparency

    # Overlay text on top
    cv2.putText(image, text, (text_x, text_y), font, font_scale, color, thickness)
    return image

def main():
    db_manager = DatabaseManager(db_config)
    print("Starting nugget detection system...")
    print("Press 'S' to save a batch")
    print("Press 'ESC' to exit")
    
    # Get the last sample ID from the database and increment by 1.
    batch_id = db_manager.get_last_sample_id() + 1
    print(f"Starting with Sample ID: {batch_id}")
    
    # Hashmap to keep track of nugget count frequencies.
    nugget_count_hashmap = {}
    
    # Initialize the YOLO model (set verbose to False if supported).
    model = YOLO('best.pt', verbose=False)
    bounding_box_annotator = sv.BoundingBoxAnnotator()
    label_annotator = sv.LabelAnnotator()

    # Start capturing from the first camera.
    capture = cv2.VideoCapture(0)
    if not capture.isOpened():
        print("Camera not working")
        return

    try:
        while True:
            ret, frame = capture.read()
            if not ret:
                print("Failed to grab frame")
                break

            start_time = time.time()

            results = model(frame)[0]
            detections = sv.Detections.from_ultralytics(results)
            current_count = len(detections.xyxy)

            if current_count > 0: 
                end_time = time.time()
                elapsed_time = end_time - start_time
                print(f"Time to count nuggets: {elapsed_time:.4f} seconds")
                print(f"Count of nuggets at this time: {current_count} nuggets")
            else:
                elapsed_time = 0 
            
            # Update count frequency
            nugget_count_hashmap[current_count] = nugget_count_hashmap.get(current_count, 0) + 1

            # Decision algorithm to check nugget size
            validity = decision_algorithm(detections)
            validity_text = "Valid Batch" if validity else "Invalid Batch"
            color = (0, 255, 0) if validity else (0, 0, 255)


            # Annotate frame with bounding boxes and labels
            annotated_image = bounding_box_annotator.annotate(scene=frame, detections=detections)
            annotated_image = label_annotator.annotate(scene=annotated_image, detections=detections)

            # Overlay current count on the frame.
            annotated_image = display_with_overlay(annotated_image, f"Count: {current_count}", (10, 40), color=(0, 255, 0))
            
            # Add the validity text with better readability
            annotated_image = display_with_overlay(annotated_image, validity_text, (10, 80), color=color)
            cv2.imshow('CAMERA', annotated_image)
            

            key = cv2.waitKey(1) & 0xFF

            if key == ord('s'):
                most_frequent_count = get_most_frequent_count(nugget_count_hashmap)
                success = db_manager.save_batch(
                    sample_id=batch_id,
                    nugget_count=most_frequent_count,
                    batch_weight=100,  # in LBS
                    batch_validity=validity   # in percentage
                )

                if success:
                    print(f"Batch {batch_id} saved successfully! Count: {most_frequent_count}")
                    batch_id += 1  # Increment sample ID for the next batch.
                    nugget_count_hashmap.clear()  # Reset the hashmap for the next batch.
                else:
                    print("Failed to save batch")
            elif key == 27:  # ESC key to exit
                print("Closing application...")
                break

    except Exception as e:
        print(f"An error occurred: {e}")
    
    finally:
        capture.release()
        cv2.destroyAllWindows()
        db_manager.close()

if __name__ == "__main__":
    main()
