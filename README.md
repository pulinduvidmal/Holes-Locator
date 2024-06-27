# Holes-Locator

This project uses OpenCV to detect holes in a video feed and calculates the angle of rotation needed to align one of the holes to a specified initial point. The angle is then mapped to an analog value in the range of 0 to 255, which can be used for further processing or control.

## Table of Contents
- [Introduction](#introduction)
- [Requirements](#requirements)
- [Installation](#installation)
- [Usage](#usage)
- [Acknowledgments](#acknowledgments)

## Introduction
The goal of this project is to detect holes in a video feed from a camera and calculate the vertical displacement (\( \Delta y \)) of the detected holes from the center of the frame. This displacement is then used to calculate the angle of rotation needed to align a hole with an initial point. The calculated angle is mapped to an analog value (0-255) for use in various applications.

## Requirements
- Python 3.10
- OpenCV
- NumPy

## Installation
1. Clone the repository:
   ```bash
   git clone https://github.com/pulinduvidmal/Holes-Locator.git
   cd Holes-Locator
   
3. Install the required packages:
   ```bash
   pip install -r requirements.txt
   
## Usage
1. Run the script:
   ```bash
   python main.py

2. The script will open a window displaying the video feed. It will detect circles and draw them on the frame along with the calculated vertical displacement and rotation angle.

## Acknowledgments
This project was inspired by a need to detect and align objects using computer vision and to map these alignments to analog values for further processing.

Feel free to contribute to the project by submitting issues or pull requests.

