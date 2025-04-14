# NyanAR: Augmented Reality Nyan Cat 🌈😺

Turn your boring reality into a rainbow-filled paradise with this AR implementation that places the internet's favorite pop-tart cat on any chessboard pattern!

## What is this sorcery? 🧙‍♂️

NyanAR uses computer vision to detect a chessboard pattern in your video, then magically summons Nyan Cat to float above it in augmented reality. As you move the camera or the chessboard, Nyan Cat follows, leaving a trail of pixel rainbows and bewildered onlookers.

## Demo Video 📹

[![NyanAR Demo](https://img.youtube.com/vi/gNX_XyB2B8w/0.jpg)](https://www.youtube.com/watch?v=gNX_XyB2B8w)

## Requirements 🔧

- Python 3.x
- OpenCV (`cv2`)
- NumPy
- imageio

## How to Use 🚀

1. Print out a 10×7 crosspoints, 20mm checkerboard pattern
2. Make sure you have the input media files:
   - `media/checkerboard_1x.mp4` - A video of your checkerboard
   - `media/nyan.gif` - The glorious Nyan Cat animation
3. Run the script:
   ```
   python nyanAR.py
   ```
4. Watch as reality becomes significantly improved by the addition of a pop-tart cat

## Controls 🎮

- Press `Space` to pause/unpause
- Press `Esc` to exit and save the output video

## How it Works 🔍

1. Camera calibration parameters detect the chessboard in your video
2. 3D pose estimation figures out where the chessboard is in space
3. Nyan Cat is projected onto the chessboard with proper perspective
4. Your life is instantly 73% more awesome

## Known Issues 🐛

- Nyan Cat may occasionally clip through reality, causing existential crises
- Extended use may result in uncontrollable humming of "nyan nyan nyan nyan"

## License 📄


Check the beer license by [MINT Lab (Mobile Intelligence Lab)](https://github.com/mint-lab)