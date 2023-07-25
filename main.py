import cv2
import mediapipe as mp
import pyautogui

# Initialize Mediapipe
mp_hands = mp.solutions.hands
hands = mp_hands.Hands()

# Get the screen resolution for scaling
screen_width, screen_height = pyautogui.size()

# Set the deadzone size (adjust as needed)
deadzone = 10

# Set the flag for left-click action
left_click_pressed = False

# Main function
def main():
    global left_click_pressed
    # Open the webcam
    cap = cv2.VideoCapture(3)
    cap.set(cv2.CAP_PROP_FOURCC, cv2.VideoWriter.fourcc('m', 'j', 'p', 'g'))

    fps = int(cap.get(cv2.CAP_PROP_FPS))
    print(fps)


    while cap.isOpened():
        success, image = cap.read()
        if not success:
            break

        # Flip the image horizontally
        #image = cv2.flip(image, 1)

        # Convert the image from BGR to RGB
        image_rgb = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)

        # Process the image and detect hands
        results = hands.process(image_rgb)

        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks:
                # Draw rectangles around hand landmarks
                mp.solutions.drawing_utils.draw_landmarks(
                    image, hand_landmarks, mp_hands.HAND_CONNECTIONS,
                    mp.solutions.drawing_utils.DrawingSpec(color=(0, 255, 0), thickness=2, circle_radius=4),
                    mp.solutions.drawing_utils.DrawingSpec(color=(255, 0, 0), thickness=2)
                )

                # Get the x, y coordinates of the palm center
                palm_x = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].x
                palm_y = hand_landmarks.landmark[mp_hands.HandLandmark.WRIST].y

                # Scale the coordinates to match the screen resolution
                cursor_x = int((1 - palm_x) * screen_width)
                cursor_y = int(palm_y * screen_height)

                # Apply the deadzone to reduce shakiness
                if abs(cursor_x - pyautogui.position().x) < deadzone:
                    cursor_x = pyautogui.position().x

                if abs(cursor_y - pyautogui.position().y) < deadzone:
                    cursor_y = pyautogui.position().y

                # Move the mouse cursor
                pyautogui.moveTo(cursor_x, cursor_y)

                # Check if thumb and index finger are close together (left-click)
                thumb_x = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].x
                thumb_y = hand_landmarks.landmark[mp_hands.HandLandmark.THUMB_TIP].y

                index_finger_x = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].x
                index_finger_y = hand_landmarks.landmark[mp_hands.HandLandmark.INDEX_FINGER_TIP].y

                if abs(thumb_x - index_finger_x) < 0.05 and abs(thumb_y - index_finger_y) < 0.05:
                    if not left_click_pressed:
                        pyautogui.mouseDown()
                        left_click_pressed = True
                else:
                    if left_click_pressed:
                        pyautogui.mouseUp()
                        left_click_pressed = False

        # Show the video stream with landmarks
        cv2.imshow('Invisible Mouse', image)

        # Exit the loop on pressing 'q'
        if cv2.waitKey(5) & 0xFF == ord('q'):
            break

    # Release the video capture and close all windows
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()
