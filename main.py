import time
import yaml
import random
import pyautogui

with open("config/configuration.yaml", "r") as yamlfile:
    configuration = yaml.safe_load(yamlfile)

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
miniGameAttemps = 0
reCastCount = 0

fishingKey = configuration['fishingKey']
castNetKey = configuration['castNetKey']

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

def tryPlayMiniGame() -> bool:
    foundScreenshot = pyautogui.screenshot(region=(int(screenWidth/2 - 100), int(screenHeight/2), 150, 200))
    foundScreenshot.save('minigame_indicator.png')
    foundMiniGame = pyautogui.locateOnScreen('config/minigame_start.png', confidence=0.5, grayscale=True, region=(int(screenWidth/2 - 100), int(screenHeight/2 - 50), 200, 200))
    if foundMiniGame != None:
        print('Mini game found')
        time.sleep(2)
        print('Casting net')
        pyautogui.press(castNetKey)
        time.sleep(3)
        miniGameStart = time.time()
        while(time.time() - miniGameStart < 15):
            perfectFound = pyautogui.locateOnScreen('config/perfect_template.png', confidence=0.5, grayscale=True)
            if(perfectFound != None):
                pyautogui.press(' ')
                time.sleep(0.145)
    return foundMiniGame != None

def fishing() -> bool:
    print("Casting out lure")
    pyautogui.press(fishingKey)
    castTime = time.time()
    fishFound = None
    # countdown for recast could be stuck
    while(time.time() - castTime < 25 and fishFound == None):
        if (captureFishCaught):
            imagePixels = pyautogui.screenshot(region=(fishCaughtStartX, fishCaughtStartY, fishCaughtWidth, fishCaughtHeight))
            imagePixels.save('capture_indicator.png')

        fishFound = pyautogui.locateOnScreen(fishCaughtTemplate, confidence=fishCaughtCoef, grayscale=fishCaughtGrayScale,region=(fishCaughtStartX, fishCaughtStartY, fishCaughtWidth, fishCaughtHeight))
        if (fishFound != None):
            print("Detected fish! Reeling in!")
            pyautogui.press(fishingKey)
    return fishFound != None


# Starting the app   
print("Started!")
print("Fishing will be started in 5 seconds!")
time.sleep(5)
while True:
    tryRepair()
    if(fishing()):
        reCastCount = 0
        # Time between fishing before able to press key again
        time.sleep(random.uniform(5.5, 7))
        playedMiniGame = tryPlayMiniGame()
        time.sleep(1)

        fishCaught += 1
        print(f"Caught {fishCaught} fishes")
        if(playedMiniGame):
            miniGameAttemps += 1
            print(f"Mini game attempts: {miniGameAttemps}")
    else:
        reCastCount += 1
        # probably out of energy, stop the app
        if reCastCount == 6:
            break
