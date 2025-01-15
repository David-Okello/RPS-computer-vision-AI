# Hand Gesture Rock-Paper-Scissors Game

This project implements a real-time Rock-Paper-Scissors game using hand gesture recognition with OpenCV and MediaPipe. The game supports both single-player (against an AI) and two-player modes.

## Features
- Detects hand gestures for Rock, Paper, and Scissors using MediaPipe's hand tracking solution.
- Displays game progress and results in real-time using OpenCV.
- Supports single-player mode against a computer opponent and two-player mode.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/David-Okello/RPS-computer-vision-AI.git
   cd RPS-computer-vision-AI
   ```

2. Install the required dependencies using the `requirements.txt` file:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

1. Run the script:
   ```bash
   python main.py
   ```

2. Allow access to your webcam.

3. Follow the on-screen prompts to play the game:
   - Ready Players?
   - Ready?... Set... PLAY!
   - The game will display the results and declare the winner.

4. Press 'q' to quit the game.

## How It Works

- The script captures video from the webcam and uses MediaPipe to detect hand landmarks.
- The `readHandMove` function determines the gesture (Rock, Paper, Scissors) based on the position of the fingers.
- The game logic compares the gestures to decide the winner and displays the result using OpenCV.

## Game Rules

- **Rock**: No fingers raised.
- **Paper**: All fingers raised.
- **Scissors**: Only the index and middle fingers raised.

## Dependencies
- [OpenCV](https://opencv.org/)
- [MediaPipe](https://mediapipe.dev/)

## Example Output

- The game window will show the countdown, the gestures detected, and the game result.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements
- [MediaPipe](https://mediapipe.dev/) for hand tracking.
- [OpenCV](https://opencv.org/) for real-time video processing.
