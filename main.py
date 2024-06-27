import cv2
import numpy as np

cap = cv2.VideoCapture(0)

# Calculate the distance between two points
def distance(point1, point2):
    return np.sqrt((point1[0] - point2[0])**2 + (point1[1] - point2[1])**2)

# Draw a crosshair at the center of the image
def draw_crosshair(image):
    height, width, _ = image.shape
    center = (width // 2, height // 2)
    cv2.line(image, (center[0] - 10, center[1]), (center[0] + 10, center[1]), (0, 0, 255), 2)
    cv2.line(image, (center[0], center[1] - 10), (center[0], center[1] + 10), (0, 0, 255), 2)
    return center

# Convert the vertical displacement to the angle of rotation
def calculate_rotation_angle(delta_y, radius):
    # Convert radius to pixels (assuming the radius in cm and known pixels per cm ratio)
    # Here, we assume 1 cm equals 37.795275591 pixels (100 pixels per inch and 2.54 cm per inch)
    pixels_per_cm = 37.795275591
    radius_in_pixels = radius * pixels_per_cm
    # Calculate the angle in radians using the arcsin function
    angle_rad = np.arcsin(delta_y / radius_in_pixels)
    # Convert the angle to degrees
    angle_deg = np.degrees(angle_rad)
    return angle_deg

while True:
    ret, frame = cap.read()

    # Convert frame to grayscale
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)

    # Blur the grayscale image
    gray_blurred = cv2.blur(gray, (3, 3))

    # Apply Hough transform on the blurred image
    detected_circles = cv2.HoughCircles(gray_blurred,
                       cv2.HOUGH_GRADIENT, 1, 20, param1=50,
                       param2=30, minRadius=1, maxRadius=40)

    # Draw circles and calculate center coordinates
    if detected_circles is not None:
        detected_circles = np.uint16(np.around(detected_circles))
        
        # List to store the Δy values
        delta_y_values = []

        for pt in detected_circles[0, :]:
            a, b, r = pt[0], pt[1], pt[2]

            # Draw the circumference of the circle
            cv2.circle(frame, (a, b), r, (0, 255, 0), 2)

            # Draw a small circle (of radius 1) to show the center
            cv2.circle(frame, (a, b), 1, (0, 0, 255), 3)

            # Calculate the center of the display
            display_center = draw_crosshair(frame)

            # Calculate the distance between circle center and display center
            circle_center = (a, b)
            distance_x = circle_center[0] - display_center[0]
            distance_y = circle_center[1] - display_center[1]
            delta_y_values.append(distance_y)

            # Draw a line from circle center to display center
            cv2.line(frame, circle_center, display_center, (255, 0, 0), 2)

        if delta_y_values:
            # Get the minimum absolute delta y value
            min_delta_y = min(delta_y_values, key=abs)

            # Calculate the angle of rotation for the minimum delta y
            rotation_angle = calculate_rotation_angle(min_delta_y, 5)

            # Print the distance from circle center to display center on the display
            cv2.putText(frame, f'Delta Y: {min_delta_y:.2f}', (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)
            cv2.putText(frame, f'Rotation Angle: {rotation_angle:.2f} deg', (10, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.5, (255, 255, 255), 2)

            # Print the distance and angle in the terminal
            print(f'Delta Y: {min_delta_y:.2f}, Rotation Angle: {rotation_angle:.2f} degrees')

            def map_angle_to_analog(angle, min_angle=-30, max_angle=30, min_output=0, max_output=255):
                # Ensure the angle is within the specified range
                if angle < min_angle:
                    angle = min_angle
                elif angle > max_angle:
                    angle = max_angle
                
                # Map the angle to the analog output range
                analog_value = ((angle - min_angle) * (max_output - min_output)) / (max_angle - min_angle) + min_output
                return int(analog_value)

                
            analog_value = map_angle_to_analog(rotation_angle)
            print(f"Angle: {rotation_angle} degrees -> Analog value: {analog_value}")


    # Display the resulting frame
    cv2.imshow('Frame', frame)

    # Check for key press and break loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release the video capture object and close all windows
cap.release()
cv2.destroyAllWindows()
