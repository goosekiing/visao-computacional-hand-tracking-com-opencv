# Computer Vision: Hand Tracking with OpenCV

This repository contains a project focused on using the MediaPipe library to detect hand positions in images and videos. The project utilizes a webcam feed through the OpenCV library to perform real-time hand detection and associate specific movements with functions:

- Raising the index finger of the right hand opens Notepad on Windows.
- Lowering all fingers of the right hand closes Notepad.
- Raising the middle finger of the right hand stops the camera feed (same effect as pressing the Esc key).
- Raising the left hand brings up a virtual keyboard on the screen.
  - To type, bring the index finger close to the desired key on the image.
  - To delete a typed letter, raise the pinky finger.
  - To type uppercase letters, two or more fingers must be raised.
  - To type lowercase letters, only one finger should be raised.
- Raising both hands brings up a whiteboard where you can draw with your hand.
  - The brush is the tip of the index finger of the hand that was raised first.
  - The closer the hand is to the camera, the thicker the brush stroke.
  - The number of fingers raised on the second hand changes the brush color.
  - Closing all fingers of the second hand clears the entire screen.

The image resolution can be adjusted by changing the variables `resolucao_x` and `resolucao_y` available at the beginning of the code. These variables should be adjusted according to the screen resolution for optimal viewing. If this resolution is changed, it will also be necessary to adjust the variables `offset_x`, `offset_y`, and `tamanho_tecla` at the beginning of the main function so that the virtual keyboard fits the new resolution.

## Course Details
This project was completed as part of the 'Computer Vision with OpenCV' course on Alura. For more information about the course, visit [Alura](https://cursos.alura.com.br/formacao-visao-computacional-opencv).

## Objectives Achieved
- Learn about the free and open-source framework MediaPipe, created by Google.
- Integrate the webcam with Python code using the OpenCV library.
- Detect hand positions in images and videos.
- Extract hand landmark coordinates using the MediaPipe library.
- Build interactive projects controlled by hand gestures.

## Technologies Used
- Python (v3.8.10)
- Jupyter Notebook
- OpenCV (cv2 v3.4.8)
- MediaPipe (v0.8.11)
- Numpy

## Project Structure
The directory structure of the project is as follows:
```
visao-computacional-hand-tracking-com-opencv/
│
├── main.py
├── quadro.png
├── README.md
```

## Setup Instructions
1. Clone the repository:
   ```sh
   git clone https://github.com/goosekiing/visao-computacional-hand-tracking-com-opencv.git
   ```
2. Navigate to the project directory:
   ```sh
   cd visao-computacional-hand-tracking-com-opencv
   ```
3. Create a virtual environment and activate it:
   ```sh
   python -m venv venv
   source venv/bin/activate  # On Windows, use `venv\Scripts\activate`
   ```
4. Install the required libraries:
   ```sh
   pip install opencv-python-headless==3.4.8.29 mediapipe==0.8.11 numpy
   ```

## Running the Script
1. Ensure your webcam is connected and properly set up.
2. Run the `main.py` script to start the hand tracking and interactive functionalities:
   ```sh
   python main.py
   ```

## Language
The language used in this project is Brazilian Portuguese (pt-br).

## Author
GitHub Username: [goosekiing](https://github.com/goosekiing)
