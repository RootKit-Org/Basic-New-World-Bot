import pyautogui
import pydirectinput
import time
import random
import mss
import numpy as np
from PIL import Image
import gc

def main():
    """
    Main function for the program
    """
    # Finds all Windows with the title "New World"
    newWorldWindows = pyautogui.getWindowsWithTitle("New World")

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
    pyautogui.moveTo(centerW, centerH)

    # Clicky Clicky
    time.sleep(.1)
    pyautogui.click()
    time.sleep(.1)

    # Auto Run Key
    autowalkKey = '='

    # Seconds to move foward
    fowardMoveTotal = 20

    # Current seconds foward moved
    currentFoward = 0

    # Go right or left
    flip = 1

    # Turn 90 degrees, value will be different for you, im on a 4k monitor
    flipMouseMove = 1000

    # If the bot has stopped moving
    stopped = False

    # Making tuple with data from the window for later use
    region = (newWorldWindow.left, newWorldWindow.top, newWorldWindow.width, newWorldWindow.height)
    mssRegion = {"mon": 1, "top": newWorldWindow.top, "left": newWorldWindow.left + round(newWorldWindow.width/3), "width": round(newWorldWindow.width/3)*2, "height": newWorldWindow.height}

    # Prep screenshots, walk forward and log time
    sct = mss.mss()
    pydirectinput.press(autowalkKey)
    startTime = time.time()

    # Main bot loop, runs forever use CTRL+C to turn it off
    while True:
        # Get Screenshot and reset unstuck tracker
        sctImg = Image.fromarray(np.array(sct.grab(mssRegion)))
        stuckTracker = 0

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
            sctImg = Image.fromarray(np.array(sct.grab(mssRegion)))

            # Check if the 'q' image is on screen
            while pyautogui.locate("imgs/1.png", sctImg, grayscale=True, confidence=.8) is None:
                time.sleep(.5)
                sctImg = Image.fromarray(np.array(sct.grab(mssRegion)))
                print("Waiting...")
                gc.collect()

                # If stuckTracker gets to 15, move the mouse
                if stuckTracker == 15:
                    pydirectinput.move(5, 0, relative=True)
                    stuckTracker = 0

                stuckTracker += 1

            print("Done waiting")
            continue

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

        # Garbage man
        gc.collect()


# Runs the main function
if __name__ == '__main__':
    main()
