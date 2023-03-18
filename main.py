import time
import yaml
import random
import pyautogui

with open("config/configuration.yaml", "r") as yamlfile:
    configuration = yaml.safe_load(yamlfile)

cast = True

screenWidth = configuration['screenWidth']
screenHeight = configuration['screenHeight']

fishCaughtWidth = configuration['fishCaughtWidth']
fishCaughtHeight = configuration['fishCaughtHeight']
captureFishCaught = configuration['captureFishCaught']
fishCaughtTemplate = configuration['fishCaughtTemplateName']
fishCaughtCoef = configuration['fishCaughtCoefficient']
fishCaughtGrayScale = configuration['fishCaughtGrayScale']

repairStartX = configuration['repairIndicatorStartX']
repairStartY = configuration['repairIndicatorStartY']
repairWidth = configuration['repairIndicatorWidth']
repairHeight = configuration['repairIndicatorHeight']
captureRepairIndicator = configuration['captureRepairIndicator']
repairIndicatorTemplate = configuration['repairIndicatorTemplateName']
repairIndicatorCoef = configuration['repairIndicatorCoefficient']
repairIndicatorGrayScale = configuration['repairIndicatorGrayScale']

fishPondLocationX = configuration['fishPondLocationX']
fishPondLocationY = configuration['fishPondLocationY']

fishCaughtStartX = int(screenWidth/2 - fishCaughtWidth/2)
# 50 is offset since the indicator is not dead in the middle
fishCaughtStartY = int(screenHeight/2 - fishCaughtHeight/2 - 50)

fishCaught = 0
reCastCount = 0

fishingKey = configuration['fishingKey']

def tryRepair():
    if (captureRepairIndicator):    
        imagePixels = pyautogui.screenshot(region=(repairStartX, repairStartY, repairWidth, repairHeight))
        imagePixels.save('repair_capture.png')

    repairFound = pyautogui.locateOnScreen(repairIndicatorTemplate, confidence=repairIndicatorCoef, grayscale=repairIndicatorGrayScale, region=(repairStartX, repairStartY, repairWidth, repairHeight))
    if repairFound is not None:
        print("Repairing")
        pyautogui.keyDown('alt')
        pyautogui.keyDown('p')
        pyautogui.keyUp('p')
        pyautogui.keyUp('alt')
        time.sleep(random.uniform(1.0, 1.5))

        tryClickButton('config/repair_btn.png', 0.8, True)
        tryClickButton('config/repair_all_btn.png', 0.8, True)
        confirmed = tryClickButton('config/confirm_btn.png', 0.8, True)

        if confirmed is True:
            pyautogui.press('esc')
            time.sleep(0.5)
            pyautogui.press('esc')

        # Move mouse back to fishing position
        pyautogui.click(x=fishPondLocationX, y=fishPondLocationY, clicks=0, button='left')

def tryClickButton(btnTemplate, confidenceCoeff, shouldGrayScale) -> bool:
    btnFound = pyautogui.locateOnScreen(btnTemplate, confidence=confidenceCoeff, grayscale=shouldGrayScale)
    if btnFound is not None:
        btnCenter = pyautogui.center(btnFound)
        pyautogui.click(x=btnCenter.x, y=btnCenter.y, clicks=0, button='left')
        time.sleep(random.uniform(0.5, 1.0))
        pyautogui.click(x=btnCenter.x, y=btnCenter.y, clicks=1, button='left')
        time.sleep(random.uniform(0.5, 1.0))
    return btnFound is not None


print("Fishing will be started in 5 seconds!")
time.sleep(5)
print("Started!")
castTime = time.time()
while True:
    if (cast):
        tryRepair()
        print("Casting out lure")
        pyautogui.press(fishingKey)
        castTime = time.time()
        cast = False

    if (captureFishCaught):
        imagePixels = pyautogui.screenshot(region=(fishCaughtStartX, fishCaughtStartY, fishCaughtWidth, fishCaughtHeight))
        imagePixels.save('capture_indicator.png')

    fishFound = pyautogui.locateOnScreen(fishCaughtTemplate, confidence=fishCaughtCoef, grayscale=fishCaughtGrayScale,region=(fishCaughtStartX, fishCaughtStartY, fishCaughtWidth, fishCaughtHeight))
    if (fishFound != None):
        print("Detected catch! Reeling in lure")
        pyautogui.press(fishingKey)
        time.sleep(random.uniform(6, 7.5))
        fishCaught += 1
        print(f"Caught {fishCaught} fishes")
        cast = True
        castTime = time.time()
        reCastCount = 0
    else:
        # Re-casting line, probably stuck
        if (time.time() - castTime > 25):
            cast = True
            castTime = time.time()
            reCastCount += 1
            # probably out of energy, stop the app
            if reCastCount == 6:
                break
    time.sleep(0.100)
