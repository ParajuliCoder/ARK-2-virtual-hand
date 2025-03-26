Hand Gesture Control System
📜 Overview
This project implements a computer vision-based hand gesture control system that allows you to interact with your computer using hand gestures. The system can:

Move the cursor

Perform clicks

Scroll up/down

Take screenshots

All without touching your mouse or keyboard!

✨ Features
Cursor Movement: Move your index finger to control the cursor

Click Gesture: Raise your pinky finger to perform a click

Scrolling:

Scroll up with index finger raised

Scroll down with all fingers down

Screenshots: Raise index and middle fingers to capture screen

Real-time Feedback: Visual indicators show detected gestures

🛠️ Technologies Used
OpenCV (for computer vision)

MediaPipe (for hand tracking)

PyAutoGUI (for system control)

NumPy (for calculations)

⚙️ Installation
Clone this repository:

bash
Copy
git clone https://github.com/your-username/hand-gesture-control.git
cd hand-gesture-control
Install required packages:

bash
Copy
pip install -r requirements.txt
Or install them manually:

bash
Copy
pip install opencv-python mediapipe pyautogui numpy
🚀 Usage
Run the application:

bash
Copy
python hand_gesture_control.py
Perform gestures in front of your webcam:

Move cursor: All fingers up

Click: Pinky finger up

Scroll up: Index finger up

Scroll down: All fingers down

Screenshot: Index and middle fingers up

Press q to quit the application

🤖 Gesture Reference
Gesture	Action
✋ All fingers up	Move cursor
☝️ Index finger up	Scroll up
🖐️ All fingers down	Scroll down
✌️ Index + middle fingers up	Take screenshot
🤘 Pinky finger up	Click
📷 Screenshots
Gesture Control Demo Example of gesture control in action

⚠️ Limitations
Requires good lighting conditions

Works best with one hand visible

May have reduced accuracy with complex backgrounds

🤝 Contributing
Contributions are welcome! Please open an issue or submit a pull request.

📄 License
This project is licensed under the MIT License - see the LICENSE file for details.
