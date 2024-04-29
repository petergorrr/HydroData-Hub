import cv2

def detect_and_annotate(image_np):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)

    # Use Canny Edge Detection to highlight edges
    edges = cv2.Canny(blurred, 100, 200)

    # Find contours from the edged image
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # Assume the largest contour corresponds to the most significant feature
    if contours:
        largest_contour = max(contours, key=cv2.contourArea)
        (x, y), radius = cv2.minEnclosingCircle(largest_contour)
        center = (int(x), int(y))
        radius = int(radius)
        
        if radius > 30:  # This threshold can be adjusted
            # Draw a circle around the largest contour in red color
            cv2.circle(image_np, center, radius, (0, 0, 255), 2)
            # Write text annotation beside the circle
            text = "Risk decreased due to netting"
            text_position = (center[0] + radius + 10, center[1])  # Adjust the position as needed
            cv2.putText(image_np, text, text_position, cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 32, 20), 2)

    return image_np

