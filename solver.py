import cv2
import numpy as np
from kociemba import solve
import rubik.cube as rubik_cube
import rubik.solve as rubik_solve
import optimal.solver as sv

# Color to number mapping
color_to_number = {
    "w": 1,
    "r": 2,
    "b": 3,
    "y": 4,
    "o": 5,
    "g": 6
}

# Number to Kociemba notation
number_to_kociemba = {
    1: 'U',
    2: 'R',
    3: 'F',
    4: 'D',
    5: 'L',
    6: 'B'
}

# Define color ranges for each Rubik's Cube face
color_ranges = {
    "w": ([0, 0, 200], [180, 50, 255]),
    "r": ([0, 100, 100], [5, 255, 255]),
    "b": ([90, 100, 100], [130, 255, 255]),
    "y": ([20, 100, 100], [30, 255, 255]),
    "o": ([6, 100, 100], [10, 255, 255]),
    "g": ([35, 100, 100], [85, 255, 255])
}

def detect_color(image, color_ranges):
    hsv_image = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
    detected_colors = []
    for i in range(3):
        for j in range(3):
            x1, y1 = j * (box_width // 3), i * (box_height // 3)
            x2, y2 = (j + 1) * (box_width // 3), (i + 1) * (box_height // 3)
            cell = hsv_image[y1:y2, x1:x2]
            color_counts = {}
            for color_name, (lower, upper) in color_ranges.items():
                mask = cv2.inRange(cell, np.array(lower), np.array(upper))
                color_counts[color_name] = cv2.countNonZero(mask)
            detected_color = max(color_counts, key=color_counts.get)
            detected_colors.append(detected_color)
            cv2.rectangle(image, (x1, y1), (x2, y2), (255, 255, 255), 2)
    return np.array(detected_colors).reshape(3, 3), image

def convert_to_numerical(cube_faces):
    numerical_faces = []
    for face in cube_faces:
        numerical_faces.append([color_to_number[color] for color in face.flatten()])
    return numerical_faces

def convert_to_kociemba(numerical_faces):
    kociemba_string = ''
    for face in numerical_faces:
        kociemba_string += ''.join([number_to_kociemba[num] for num in face])
    return kociemba_string

def manually_correct_colors(detected_colors):
    print("Detected colors:")
    print(detected_colors)
    for i in range(3):
        for j in range(3):
            color_correct = input(f"Is the color {detected_colors[i, j]} at position ({i}, {j}) correct? (y/n): ")
            if color_correct.lower() == 'n':
                new_color = input("Enter the correct color (white, red, blue, orange, green, yellow): ").strip().lower()
                if new_color in color_to_number:
                    detected_colors[i, j] = new_color
                else:
                    print("Invalid color entered. Please enter one of the following: white, red, blue, orange, green, yellow.")
    return detected_colors

def main():
    cube_faces = []
    cap = cv2.VideoCapture(0)
    cap.set(cv2.CAP_PROP_SETTINGS, 1)
    cap.set(cv2.CAP_PROP_FPS, 30)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)

    for face_name in color_ranges.keys():
        recapture_face = False
        while True:
            ret, frame = cap.read()
            if not ret:
                print("Failed to capture image")
                break

            cv2.rectangle(frame, (100, 100), (400, 400), (255, 255, 255), 3)
            for i in range(1, 3):
                cv2.line(frame, (100 + i * (300 // 3), 100), (100 + i * (300 // 3), 400), (255, 255, 255), 2)
                cv2.line(frame, (100, 100 + i * (300 // 3)), (400, 100 + i * (300 // 3)), (255, 255, 255), 2)
            cv2.putText(frame, f"Position Rubik's Cube with {face_name} face", (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)
            cv2.imshow("Rubik's Cube Positioning", frame)

            if cv2.waitKey(1) & 0xFF == ord('q'):
                break
            elif cv2.waitKey(1) & 0xFF == ord('r'):
                recapture_face = True
                break

        if recapture_face:
            recapture_face = False
            continue

        ret, frame = cap.read()
        global box_width, box_height
        box_region = frame[100:400, 100:400]
        box_height, box_width, _ = box_region.shape

        detected_colors, frame_with_grid = detect_color(box_region, color_ranges)
        print(f"\nDetected colors for {face_name} face:")
        print(detected_colors)

        detected_colors = manually_correct_colors(detected_colors)

        while True:
            correct_input = input("Are the detected colors correct? (y/n): ")
            if correct_input.lower() == 'y':
                break
            elif correct_input.lower() == 'n':
                detected_colors = manually_correct_colors(detected_colors)
            else:
                print("Invalid input. Please enter 'y' for yes or 'n' for no.")

        cube_faces.append(detected_colors)
        cv2.imshow("Rubik's Cube Positioning", frame_with_grid)
        cv2.waitKey(0)

    print("Entire cube:")
    print(cube_faces)
    cap.release()
    cv2.destroyAllWindows()

    numerical_faces = convert_to_numerical(cube_faces)
    kociemba_string = convert_to_kociemba(numerical_faces)
    print(f"Kociemba notation: {kociemba_string}")
    #cube = rubik_cube.Cube(kociemba_string)

    try:
        # slow = rubik_solve.solve(kociemba_string)
        # print(f"Thistlethwaite's Solution: {slow}")

        optimalm = sv.solve(kociemba_string)
        print(f"Korf's Solution: {optimalm}")

        solution = solve(kociemba_string)
        print(f"Kociemba's Solution: {solution}")

    except Exception as e:
        print(f"Error solving the cube: {e}")

if __name__ == "__main__":
    main()
