import cv2 # OpenCV library
import random 
import mediapipe as mp

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

def readHandMove(hand_landmarks):
    landmarks = hand_landmarks.landmark
    
    # Helper function to check if a finger is extended
    def is_finger_raised(tip, base):
        # Check if the fingertip is above the base (y) and not bent sideways (x)
        return landmarks[tip].y < landmarks[base].y and abs(landmarks[tip].x - landmarks[base].x) < 0.1
    
    # Check each finger
    fingers = [
        is_finger_raised(8, 6),   # Index finger
        is_finger_raised(12, 10), # Middle finger
        is_finger_raised(16, 14), # Ring finger
        is_finger_raised(20, 18)  # Pinky finger
    ]
    
    # Recognize gestures based on finger states
    if not any(fingers):  # No fingers raised
        return "rock"
    elif fingers[0] and fingers[1] and not fingers[2] and not fingers[3]:  # Only index and middle fingers raised
        return "scissors"
    elif all(fingers):  # All fingers raised
        return "paper"
    else:
        return "unknown"


# Open up webcam
cap = cv2.VideoCapture(0) # Opens default camera (index 0)

clock = 0
player1 = None
player2 = None
p1 = None
ai = None
gameText = ''
winner = ''
success = True
mode = ''

# Check if the webcam opened successfully
if not cap.isOpened():
    print("Error: Could not open camera.")
    exit()

with mp_hands.Hands(model_complexity = 0, 
                    min_detection_confidence = 0.5, 
                    min_tracking_confidence = 0.5) as hands:

    while True:
        success, img = cap.read()
        if not success or img is None:
            print("Error: Failed to read image from camera.")
            break

        # Flip the image horizontally (Makes it look like you are looking into a mirror)
        img = cv2.flip(img, 1)

        # In order to add hands...Convert the frame(img) into RGB colorspace from BGR
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

        # Runs model on the img and figures out where out hands are
        results = hands.process(img)

        # Revert img back to original colorspace
        img = cv2.cvtColor(img, cv2.COLOR_RGB2BGR)

        # Superimpose the hands landmarks onto the hand on the frame
        if results.multi_hand_landmarks:
            for hand_landmarks in results.multi_hand_landmarks: 
                mp_drawing.draw_landmarks(
                    img,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
        
        if 0 <= clock < 20:
            success = True
            gameText = 'Ready Players?'
        elif clock < 30 : gameText = "Rock..."
        elif clock < 40 : gameText = "Paper..."
        elif clock < 50 : gameText = "Scissors..."
        elif clock < 60 : gameText = "SHOOT!"
        elif clock == 60 : 
            hls = results.multi_hand_landmarks
            if hls and len(hls) == 2: # Checks if hls is an actual list or null object. Checks number of hands
                player1 = readHandMove(hls[0])
                player2 = readHandMove(hls[1])
                mode = '2 Player'
            elif hls and len(hls) == 1: # If one hand then play against computer
                randomMove = ['rock', 'paper', 'scissors']
                ai = random.choice(randomMove)
                p1 = readHandMove(hls[0])
                mode = '1 Player'
            else:
                success = False
        elif clock < 100:
            if success and mode == '2 Player':
                gameText = f"Player 1: {player1} ... Player 2: {player2}"
                if player1 == player2: winner = "Tie"
                elif player1 == 'paper' and player2 == 'rock': winner = f'Player 1 ({player1}) wins'
                elif player1 == 'rock' and player2 == 'scissors': winner = f'Player 1 ({player1}) wins'
                elif player1 == 'scissors' and player2 == 'paper': winner = f'Player 1 ({player1}) wins'
                else: winner = f'Player 2 ({player2}) wins'
            elif success and mode == '1 Player':
                gameText = f"Player 1: {p1} ... AI: {ai}"
                if p1 == ai: winner = "Tie"
                elif p1 == 'paper' and ai == 'rock': winner = f'Player 1 ({p1}) wins'
                elif p1 == 'rock' and ai == 'scissors': winner = f'Player 1 ({p1}) wins'
                elif p1 == 'scissors' and ai == 'paper': winner = f'Player 1 ({p1}) wins'
                else: winner = f'AI ({ai}) wins'
            else: gameText = "Invalid move"

        cv2.putText(img, f"Timer: {clock}", (50,50), cv2.FONT_HERSHEY_PLAIN, 2, (66,66,104), 2, cv2.LINE_AA)
        cv2.putText(img, gameText, (50,80), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,255), 2, cv2.LINE_AA)
        cv2.putText(img, winner, (50,110), cv2.FONT_HERSHEY_PLAIN, 2, (0,255,255), 2, cv2.LINE_AA)

        clock = (clock + 1) % 100  # Repeats every 100 frames

        cv2.imshow("Image", img)
        if cv2.waitKey(1) & 0xFF == ord('q'): break  # 1ms delay (waitkey) & Press 'q' to quit

cap.release() # Releases the camera resource
cv2.destroyAllWindows() # Close all open windows