import pyautogui
import pydirectinput
import time
import random
import mss
import numpy as np
from PIL import Image
import gc
import pygetwindow
import win32api, win32con
import bettercam

def main():
    """
    Main function for the program
    """
    # Auto Run Key
    autowalkKey = '='

    # Seconds to move foward
    fowardMoveTotal = 20

    # Current seconds foward moved
    currentFoward = 0

    # Go right or left
    flip = 1

    # Turn 90 degrees, value will be different for you, im on a 4k monitor
    flipMouseMove = 3000

    # If the bot has stopped moving
    stopped = False
 
    # Finds all Windows with the title "New World"
    newWorldWindows = pygetwindow.getWindowsWithTitle("New World")

    # Find the Window titled exactly "New World" (typically the actual game)
    for window in newWorldWindows:
        if window.title == "New World":
            newWorldWindow = window
            break

    # Select that Window
    newWorldWindow.activate()

    # Move your mouse to the center of the game window
    centerW = newWorldWindow.left + (newWorldWindow.width/2)
    centerH = newWorldWindow.top + (newWorldWindow.height/2)

    print(centerH, centerW)
    # pyautogui.moveTo(centerW, centerH)
    # win32api.mouse_event(win32con.MOUSEEVENTF_ABSOLUTE, int(centerW), int(centerH), 0, 0)

    win32api.SetCursorPos((int(centerW), int(centerH)))

    # Clicky Clicky
    time.sleep(1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN,0,0)
    time.sleep(0.01)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP,0,0)
    time.sleep(1)

    # TODO - newWorldWindow.top keeps giving a negative number, so I'm just going to use 0 for now
    region = (
        newWorldWindow.left + round(newWorldWindow.width/3),
        newWorldWindow.top,
        newWorldWindow.left + (round(newWorldWindow.width/3)*2),
        newWorldWindow.top + newWorldWindow.height
    )

    camera = bettercam.create(region=region, output_color="BGRA", max_buffer_len=512)
    camera.start(target_fps=120, video_mode=True)
    # This should resolve issues with the first cast being short
    time.sleep(2)

    pydirectinput.press(autowalkKey)
    startTime = time.time()

    # Main bot loop, runs forever use CTRL+C to turn it off
    while win32api.GetAsyncKeyState(ord("Q")) == 0:
        # Get Screenshot and reset unstuck tracker
        npImg = np.array(camera.get_latest_frame())

        sctImg = Image.fromarray(npImg)
        stuckTracker = 0

        try:
            # Find that image on screen, in that region, with a confidence of 65%
            if pyautogui.locate("imgs/e0.png", sctImg, grayscale=True, confidence=.8) is not None:
                # If not stopped, stop
                if not stopped:
                    pydirectinput.press(autowalkKey)

                stopped = True
                pyautogui.press('e')
                print("Pressing e")
                time.sleep(1.2)

                # Get a new Screenshot
                sctImg = Image.fromarray(np.array(camera.get_latest_frame()))

                # Check if the 'q' image is on screen
                while pyautogui.locate("imgs/1.png", sctImg, grayscale=True, confidence=.8) is None:
                    time.sleep(.5)
                    sctImg = Image.fromarray(np.array(camera.get_latest_frame()))
                    print("Waiting...")

                    # If stuckTracker gets to 15, move the mouse
                    if stuckTracker == 15:
                        pydirectinput.move(5, 0, relative=True)
                        stuckTracker = 0

                    stuckTracker += 1

                print("Done waiting")
                continue
        except Exception as e:
            pass

        # If bot is stopped, make the bot move again
        if stopped:
            pydirectinput.press(autowalkKey)
            stopped = False
            startTime = time.time()

        # Calculated how much the bot has moved forward
        currentFoward += (time.time() - startTime)
        startTime = time.time()

        # Flippy flip if you hitty hit the max move time (fowardMoveTotal)
        if currentFoward >= fowardMoveTotal:
            # Reset the move foward
            currentFoward = 0

            for i in range(0, flipMouseMove, round(flipMouseMove/5)):
                # Moving the mouse a 5th of the total move amount
                pydirectinput.move(round(flipMouseMove/5) * flip, 0, relative=True)
                # Wait for .3 seconds
                time.sleep(.3)

            # Flippy flippy the value. Evil math.
            flip *= -1

# Runs the main function
if __name__ == '__main__':
    main()
