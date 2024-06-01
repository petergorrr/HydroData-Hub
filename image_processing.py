import cv2

def detect_and_annotate(image_np, blur_kernel_size=(5, 5), canny_threshold1=100, canny_threshold2=200, contour_size_threshold=50, max_annotations=5):
    # Convert the image to grayscale
    gray = cv2.cvtColor(image_np, cv2.COLOR_RGB2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, blur_kernel_size, 0)

    # Use Canny Edge Detection to highlight edges
    edges = cv2.Canny(blurred, canny_threshold1, canny_threshold2)

    # Find contours from the edged image
    contours, _ = cv2.findContours(edges, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    if not contours:
        print("No contours found.")
        return image_np

    # Sort contours by area and keep the largest ones
    contours = sorted(contours, key=cv2.contourArea, reverse=True)[:max_annotations]

    # Process each significant contour and annotate if it meets the size threshold
    annotated_count = 0
    for contour in contours:
        (x, y), radius = cv2.minEnclosingCircle(contour)
        center = (int(x), int(y))
        radius = int(radius)
        
        if radius > contour_size_threshold:
            # Draw a circle around the contour in red color
            cv2.circle(image_np, center, radius, (0, 0, 255), 2)
            
            # Write text annotation beside the circle
            text = "Risk decreased due to soil nailing"
            text_size, _ = cv2.getTextSize(text, cv2.FONT_HERSHEY_SIMPLEX, 0.7, 2)
            text_width, text_height = text_size
            
            # Ensure the text is within image boundaries
            text_x = min(center[0] + radius + 10, image_np.shape[1] - text_width)
            text_y = max(min(center[1] + text_height // 2, image_np.shape[0] - text_height // 2), text_height)
            
            cv2.putText(image_np, text, (text_x, text_y), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 32, 20), 2)
            
            annotated_count += 1
            if annotated_count >= max_annotations:
                break

    return image_np


