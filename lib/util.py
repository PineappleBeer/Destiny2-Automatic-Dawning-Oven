
from PIL import ImageGrab
import numpy as np
import cv2 as cv
import pyautogui as pg
from paddleocr import PaddleOCR
from lib.cookies import cookies
import win32gui as w

# 抓取屏幕


def getScreen(type="L"):
    im = ImageGrab.grab().convert(type)
    im = np.array(im)
    return im

# 多个图像匹配


def compareMultipleImg(path):
    result = []
    tl = cv.imread(path, 0)
    sc = getScreen()
    r = cv.matchTemplate(sc, tl, cv.TM_CCOEFF_NORMED)
    threshold = 0.85
    loc = np.where(r >= threshold)
    for po in zip(*loc[::-1]):
        result.append(po)
    if len(result) == 0:
        return 0
    return result

# 单个图像匹配


def compareImg(path):
    tl = cv.imread(path, cv.IMREAD_GRAYSCALE)
    tldst = np.zeros_like(tl)
    cv.normalize(tl, tldst, 0, 255, cv.NORM_MINMAX, cv.CV_8U)
    sc = getScreen()
    scdst = np.zeros_like(sc)
    cv.normalize(sc, scdst, 0, 255, cv.NORM_MINMAX, cv.CV_8U)
    r = cv.matchTemplate(scdst, tldst, cv.TM_CCOEFF_NORMED)
    min_val, max_val, min_loc, max_loc = cv.minMaxLoc(r)
    if max_val > 0.9:
        return [max_loc, tl.shape[0], tl.shape[1]]
    return 0


# 移动鼠标并点击


def moveClick(po,  width=60, height=60, type="click",):
    pg.moveTo(po[0] + width / 2, po[1] + height / 2)
    if type == 'click':
        pg.mouseDown()
        pg.mouseUp()
    elif type == 'rightclick':
        pg.rightClick()

# 保存图片


def saveImg(img, path='./img/save.png'):
    cv.imwrite(path, img, [int(cv.IMWRITE_PNG_COMPRESSION), 9])

# 获取屏幕文字


def getOCR():
    ocr = PaddleOCR(use_angle_cls=True, lang="ch")
    result = ocr.ocr(getScreen(), cls=True)
    return result

# 判断屏幕文字返回匹配目标


def compareOCR(result):
    r = ''
    for line in result:
        for cookie in cookies:
            if line[1][0].find(cookie) != -1:
                r = cookie
    return r

# 获取当前焦点窗口


def getWindowName():
    return w.GetWindowText(w.GetForegroundWindow())
