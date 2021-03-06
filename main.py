
import time

from cv2 import repeat
from lib.util import getScreen, moveClick, compareMultipleImg, compareImg, compareOCRGetCookies, compareOCR, getWindowName
import pyautogui as pg
from lib.cookies import cookies
import keyboard

single = ''  # 是否只做一种饼干

taskPanel = False  # 已经打开悬赏面板，等待显示

ovenPanel = False  # 已经打开烤炉，等待显示

framePanel = False  # 已经代开饼干种类面板，等待显示

cookiePanel = False  # 已经进入烤炉

upperLimit = False  # 悬赏已经上限

haveTasks = False  # 已经打开NPC面板

getName = False  # 已经获取到要做的饼干名称

run = False  # 线程执行

taskCookies = []  # 已接悬赏要做的饼干们

cookiesImg = []  # 需要做的饼干们

repeat = False  # 重复做一种饼干

# 获取所有悬赏图标的位置


def getTasksCoordinate():
    pg.moveTo(10, 10)  # 避免鼠标触发悬赏详细影响抓取
    return compareMultipleImg('./img/task.png')

# 获取所有悬赏的饼干名称


def getCookiesName():
    global taskPanel
    global getName

    task = compareImg('./img/task.png')
    taskBtn = compareImg('./img/taskBtn.png')

    if (taskPanel == False) & (taskBtn == 0) & (task == 0):
        pg.press('f2')
        task = compareImg('./img/task.png')
        taskBtn = compareImg('./img/taskBtn.png')
        if (taskBtn != 0) & (task != 0):
            taskPanel = True
        time.sleep(2)
    elif taskPanel == False:
        return 0
    coordinates = getTasksCoordinate()
    cookiesName = []
    if coordinates == 0:
        return 0
    for co in coordinates:
        if run == False:
            return 0
        pg.moveTo(co)
        time.sleep(0.5)
        r = compareOCRGetCookies()
        if r != '':
            cookiesName.append(r)
            getName = True
    pg.moveTo(500, 10)
    return cookiesName

# 开始做饼干


def makeCookies():
    global ovenPanel
    global framePanel
    global cookiePanel
    global cookiesImg
    global taskPanel
    global taskCookies
    global repeat

    taskBtn = compareImg('./img/taskBtn.png')
    ovenBtn = compareImg('./img/oven.png')
    frameBtn = compareImg('./img/frameBtn.png')
    nextBtn = compareImg('./img/nextBtn.png')
    task = compareImg('./img/task.png')
    taskBtn = compareImg('./img/taskBtn.png')
    if (framePanel == True) & (nextBtn != 0) & (taskBtn == 0):
        for inx, img in enumerate(cookiesImg):
            if run == False:
                return 0
            preBtn = compareImg('./img/preBtn.png')
            if preBtn == 0:
                return 0
            moveClick(preBtn[0], preBtn[1], preBtn[2])
            time.sleep(0.5)
            cook = compareImg(img)
            if cook == 0:
                moveClick(nextBtn[0], nextBtn[1], nextBtn[2], 'click', )
                time.sleep(0.5)
                cook = compareImg(img)

            if cook != 0:
                pg.moveTo([cook[0][0] + cook[1] / 2, cook[0][1] + cook[2] / 2])
                repeat = True
                while(repeat & run):
                    if single == '':
                        repeat = False
                    pg.mouseDown()
                    time.sleep(2)
                    pg.mouseUp()
                    if single == '':
                        print(taskCookies[inx])
        if single == '':
            getRewards()
        closePanel()

    elif (framePanel == False) & (frameBtn != 0):
        moveClick(frameBtn[0], frameBtn[1], frameBtn[2], 'rightclick')
        framePanel = True

    elif (ovenPanel == False) & (ovenBtn != 0):
        moveClick(ovenBtn[0], ovenBtn[1], ovenBtn[2], 'rightclick')
        ovenPanel = True
    elif (taskPanel == False) & (taskBtn == 0) & (task == 0):
        pg.press('f2')
        taskPanel = True
    checkPanel()

# 接悬赏


def getTasks():
    global upperLimit
    global haveTasks

    npc = compareImg('./img/npc.png')
    limit = compareImg('./img/limit.png')
    gift = compareImg('./img/gift.png')
    evaGift = compareImg('./img/evaGift.png')
    accept = compareImg('./img/accept.png')

    if npc == 0:
        pg.press('esc')
        time.sleep(1)
        return 0
    elif (gift != 0) | (evaGift != 0):  # 有礼物要送
        hasgift = True
        while(hasgift & run):
            if gift != 0:
                moveClick(gift[0], gift[1], gift[2])
            else:
                pg.click()
            evaGift = compareImg('./img/evaGift.png')
            if evaGift == 0:
                hasgift = False
            time.sleep(0.5)
        return 0
    elif accept != 0:
        pg.press('enter')
        return 0
    elif limit == 0:
        task = compareImg('./img/task.png')
        if task != 0:
            while((limit == 0) & run):
                moveClick(task[0], task[1], task[2])
                limit = compareImg('./img/limit.png')
                time.sleep(0.5)
    else:
        haveTasks = True
        upperLimit = True


def checkPanel():
    global taskPanel
    global ovenPanel
    global framePanel
    global cookiePanel

    if cookiePanel == True:
        framePanel = True
        taskPanel = True
        ovenPanel = True
    elif framePanel == True:
        taskPanel = True
        ovenPanel = True
    elif ovenPanel == True:
        taskPanel = True


def closePanel():
    global taskPanel
    global ovenPanel
    global framePanel
    global cookiePanel
    global upperLimit
    global getName
    global haveTasks
    global taskCookies
    global cookiesImg
    global taskCoordinates

    taskPanel = False
    ovenPanel = False
    framePanel = False
    cookiePanel = False
    upperLimit = False
    getName = False
    haveTasks = False
    taskCookies = []
    cookiesImg = []
    taskCoordinates = []


def findCookieImg(cookieName):
    r = ''
    for co in cookies:
        if run == False:
            return 0
        if co == cookieName:
            r = cookies[co]
    return r


def getRewards():
    pg.press('esc')
    time.sleep(1)
    pg.moveTo(1000, 10)
    coordinates = compareMultipleImg('./img/rewards.png')
    while((coordinates != 0) & run):
        moveClick(coordinates[0])
        pg.moveTo([coordinates[0][0], coordinates[0][1] - 200])
        time.sleep(1)
        coordinates = compareMultipleImg('./img/rewards.png')


def stop(key):
    global run
    global repeat

    if (key.name == 'f4') & (key.event_type == 'down'):
        run = False
        repeat = False
        print('stop')


keyboard.wait('f3')
run = True
print('start')
keyboard.hook(stop)

while(run):
    if getWindowName() != 'Destiny 2':  # 开始后如果焦点窗口不是游戏，则退出
        pg.press('f4')
        break
    if single == '':
        if haveTasks == False:
            getTasks()
        elif (upperLimit == True) & (getName == False):
            taskCookies = getCookiesName()
            if taskCookies == 0:
                continue
            print(taskCookies)
            for co in taskCookies:
                if run == False:
                    break
                cookiesImg.append(findCookieImg(co))
        elif getName == True:
            makeCookies()
    else:
        cookiesImg = [findCookieImg(single)]
        makeCookies()
    time.sleep(1)
