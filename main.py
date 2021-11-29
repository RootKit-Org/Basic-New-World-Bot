import pyautogui
import pydirectinput
import time
import random

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
    flipMouseMove = 2000

    # Making tuple with data from the window for later use
    region = (newWorldWindow.left, newWorldWindow.top, newWorldWindow.width, newWorldWindow.height)

    # Main bot loop, runs forever use CTRL+C to turn it off
    while True:
        # Find that image on screen, in that region, with a confidence of 65%
        if pyautogui.locateOnScreen("imgs/e0.png", grayscale=True, confidence=.65, region=region) is not None:
            pyautogui.press('e')
            time.sleep(1)
            continue

        # Do I got to explain?
        pyautogui.press(autowalkKey)

        # Randomly move foward 0 - 1.5 seconds
        temp = 1.5 * random.random()
        currentFoward += temp
        time.sleep(temp)

        # Brah, you know
        pyautogui.press(autowalkKey)

        # Flippy flip if you hitty hit the max move time (fowardMoveTotal)
        if currentFoward >= fowardMoveTotal:
            # Reset the move foward
            currentFoward = 0

            # Move the mouse 90 degrees
            pydirectinput.move(flipMouseMove * flip, 1, relative=True)

            # Move Foward 1.5 secs
            pyautogui.press(autowalkKey)
            time.sleep(1.5)
            pyautogui.press(autowalkKey)

            # Move the mouse 90 degrees
            pydirectinput.move(flipMouseMove * flip, 1, relative=True)

            # Flippy flippy the value. Evil math.
            flip *= -1

        # Sleeping for the animation
        time.sleep(.1)


# Runs the main function
if __name__ == '__main__':
    main()
