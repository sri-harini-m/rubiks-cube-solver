# Importing libraries
import cv2
import numpy as np

def detect_color(image, color_ranges):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)

    # Initialize an array to store the detected colors
    detected_colors = []

    # Iterate over each cell in the grid
    for i in range(3):
        for j in range(3):
            # Define the bounding box coordinates for the current cell
            x1, y1 = j * (box_width // 3), i * (box_height // 3)
            x2, y2 = (j + 1) * (box_width // 3), (i + 1) * (box_height // 3)
            cell = hsv_image[y1:y2, x1:x2]

            # Find the dominant color within the cell
            color_counts = {}
            for color_name, (lower, upper) in color_ranges.items():
                mask = cv2.inRange(cell, np.array(lower), np.array(upper))
                color_counts[color_name] = cv2.countNonZero(mask)

            # Determine the color with the maximum count
            detected_color = max(color_counts, key=color_counts.get)
            detected_colors.append(detected_color)

            # Draw the grid cell onto the original image (for visualization)
            cv2.rectangle(image, (x1, y1), (x2, y2), (255, 255, 255), 2)

    # Reshape the detected colors into a 3x3 matrix
    return np.array(detected_colors).reshape(3, 3), image

# Main function
def main():

    cube_faces = []
    # Open camera
    cap = cv2.VideoCapture(0)

    # Apply a different filter to the camera feed
    cap.set(cv2.CAP_PROP_SETTINGS, 1)  # Set camera settings
    cap.set(cv2.CAP_PROP_FPS, 30)  # Set frame rate
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)  # Set frame width
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)  # Set frame height

    # Define color ranges for each Rubik's Cube face
    color_ranges = {
    "red": ([0, 100, 100], [5, 255, 255]),        # Adjusted range for red
    "orange":  ([6, 100, 100], [10, 255, 255]),    # Adjusted range for orange
    "yellow": ([20, 100, 100], [30, 255, 255]),   # Adjusted range for yellow
    "green": ([40, 100, 100], [80, 255, 255]),    # Adjusted range for green
    "blue": ([90, 100, 100], [130, 255, 255]),    # Adjusted range for blue
    "white": ([0, 0, 200], [180, 40, 255])        # Adjusted range for white
}


    # Repeat for each Rubik's Cube face
    for face_name, (lower, upper) in color_ranges.items():
        print(f"Position the Rubik's Cube with the {face_name} face inside the box and press 'q' to capture...")

        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture image")
                break

            # Draw a thick box around the grid
            cv2.rectangle(frame, (100, 100), (400, 400), (255, 255, 255), 3)

            # Draw grid lines with larger cells
            for i in range(1, 3):
                cv2.line(frame, (100 + i * (300 // 3), 100), (100 + i * (300 // 3), 400), (255, 255, 255), 2)
                cv2.line(frame, (100, 100 + i * (300 // 3)), (400, 100 + i * (300 // 3)), (255, 255, 255), 2)

            # Display instructions on the frame
            cv2.putText(frame, f"Position Rubik's Cube with {face_name} face", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

            cv2.imshow("Rubik's Cube Positioning", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break

        # Capture frame after positioning Rubik's Cube
        ret, frame = cap.read()

        # Crop the frame to get the box region
        global box_width, box_height
        box_region = frame[100:400, 100:400]
        box_height, box_width, _ = box_region.shape

        # Detect the colors of the Rubik's Cube face and arrange them in a 3x3 matrix
        detected_colors, frame_with_grid = detect_color(box_region, color_ranges)

        # Print the detected colors for the current face
        print(f"\nDetected colors for {face_name} face:")
        print(detected_colors)
        cube_faces.append(detected_colors)

        # Display the grid and detected colors on the frame
        cv2.imshow("Rubik's Cube Positioning", frame_with_grid)
        cv2.waitKey(0)

    print("Entire cube:")
    print(cube_faces)
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()