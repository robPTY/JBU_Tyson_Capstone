import cv2

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

def simulate_weight(nugget_count: int, weight_per_nugget=0.65) -> float:
    return round(nugget_count * weight_per_nugget, 2)

