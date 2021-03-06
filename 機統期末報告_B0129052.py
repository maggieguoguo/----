# Wormy (a Nibbles clone)
# By Al Sweigart al@inventwithpython.com
# http://inventwithpython.com/pygame
# Released under a "Simplified BSD" license

import random, pygame, sys
from pygame.locals import *

範圍=     range
啟動=     pygame.init
鐘類=     pygame.time.Clock
幕設大小= pygame.display.set_mode
幕設標題= pygame.display.set_caption
字型類=   pygame.font.Font
事件取得= pygame.event.get
結束=     pygame.quit
離開=     sys.exit
畫方形=   pygame.draw.rect
幕更新=   pygame.display.update
方塊類=   pygame.Rect
時間等待= pygame.time.wait
對=  True
格子大小= random.randint
旋轉方法= pygame.transform.rotate
長度= len
格子函式= pygame.draw.line

每秒英尺 = 15
視窗寬度 = 640
視窗長度 = 480
單位尺寸 = 20
assert 視窗寬度 % 單位尺寸 == 0, "Window width must be a multiple of cell size."
assert 視窗長度 % 單位尺寸 == 0, "Window height must be a multiple of cell size."
每小格寬度 = int(視窗寬度 / 單位尺寸)
每小格長度 = int(視窗長度 / 單位尺寸)

#             紅 綠    藍
白色     = (255, 255, 255)
黑色     = (  0,   0,   0)
紅色       = (255,   0,   0)
綠色     = (  0, 255,   0)
深綠色 = (  0, 155,   0)
深灰色  = ( 40,  40,  40)
背景顏色 = 黑色

往上 = 'up'
往下 = 'down'
往左 = 'left'
往右 = 'right'

蟲蟲頭 = 0 # syntactic sugar: 蟲蟲的頭指標

def 主程式():
    global 每秒英尺的時間, 顯示視窗, 字體

    啟動()
    每秒英尺的時間 = 鐘類()
    顯示視窗 = 幕設大小((視窗寬度, 視窗長度))
    字體 = 字型類('freesansbold.ttf', 18)
    幕設標題('Wormy')

    顯示啟動畫面()
    while 對:
        遊戲啟動()
        螢幕顯示遊戲結束()


def 遊戲啟動():
    # 地到遊戲一開始的位置
    開始的x = 格子大小(5, 每小格寬度 - 6)
    開始的y = 格子大小(5, 每小格長度 - 6)
    蟲蟲的身體 = [{'x': 開始的x,     'y': 開始的y},
                  {'x': 開始的x - 1, 'y': 開始的y},
                  {'x': 開始的x - 2, 'y': 開始的y}]
    方向 = 往右

    # 得到蘋果的位置
    蘋果 = 得到隨機位置()

    while 對: # 遊戲的循環
        for 事件 in 事件取得(): # 事件 handling loop
            if 事件.type == QUIT:
                終止()
            elif 事件.type == KEYDOWN:
                if (事件.key == K_LEFT or 事件.key == K_a) and 方向 != 往右:
                    方向 = 往左
                elif (事件.key == K_RIGHT or 事件.key == K_d) and 方向 != 往左:
                    方向 = 往右
                elif (事件.key == K_UP or 事件.key == K_w) and 方向 != 往下:
                    方向 = 往上
                elif (事件.key == K_DOWN or 事件.key == K_s) and 方向 != 往上:
                    方向 = 往下
                elif 事件.key == K_ESCAPE:
                    終止()

        # 看蟲蟲有沒有超過表格
        if 蟲蟲的身體[蟲蟲頭]['x'] == -1 or 蟲蟲的身體[蟲蟲頭]['x'] == 每小格寬度 or 蟲蟲的身體[蟲蟲頭]['y'] == -1 or 蟲蟲的身體[蟲蟲頭]['y'] == 每小格長度:
            return # 遊戲結束
        for 蟲體 in 蟲蟲的身體[1:]:
            if 蟲體['x'] == 蟲蟲的身體[蟲蟲頭]['x'] and 蟲體['y'] == 蟲蟲的身體[蟲蟲頭]['y']:
                return # 遊戲結束

        # 檢查蟲蟲是否有吃掉蘋果
        if 蟲蟲的身體[蟲蟲頭]['x'] == 蘋果['x'] and 蟲蟲的身體[蟲蟲頭]['y'] == 蘋果['y']:
            # 不刪除蟲蟲的尾巴
            蘋果 = 得到隨機位置() # 放置新蘋果的位置
        else:
            del 蟲蟲的身體[-1] # 刪除蟲蟲的尾巴段

        # 通過後會增加一段蟲蟲的身體
        if 方向 == 往上:
            新頭 = {'x': 蟲蟲的身體[蟲蟲頭]['x'], 'y': 蟲蟲的身體[蟲蟲頭]['y'] - 1}
        elif 方向 == 往下:
            新頭 = {'x': 蟲蟲的身體[蟲蟲頭]['x'], 'y': 蟲蟲的身體[蟲蟲頭]['y'] + 1}
        elif 方向 == 往左:
            新頭 = {'x': 蟲蟲的身體[蟲蟲頭]['x'] - 1, 'y': 蟲蟲的身體[蟲蟲頭]['y']}
        elif 方向 == 往右:
            新頭 = {'x': 蟲蟲的身體[蟲蟲頭]['x'] + 1, 'y': 蟲蟲的身體[蟲蟲頭]['y']}
        蟲蟲的身體.insert(0, 新頭)
        顯示視窗.fill(背景顏色)
        畫網格()
        畫蟲蟲(蟲蟲的身體)
        畫蘋果(蘋果)
        畫分數區(長度(蟲蟲的身體) - 3)
        幕更新()
        每秒英尺的時間.tick(每秒英尺)

def 按任意鍵進入遊戲畫面():
    字體顏色 = 字體.render('Press a key to play.', 對, 深灰色)
    按鍵框框 = 字體顏色.get_rect()
    按鍵框框.topleft = (視窗寬度 - 200, 視窗長度 - 30)
    顯示視窗.blit(字體顏色, 按鍵框框)


def 檢查是否有按任意鍵():
    if 長度(事件取得(QUIT)) > 0:
        終止()

    按鍵活動 = 事件取得(KEYUP)
    if 長度(按鍵活動) == 0:
        return None
    if 按鍵活動[0].key == K_ESCAPE:
        終止()
    return 按鍵活動[0].key


def 顯示啟動畫面():
    標題字體 = 字型類('freesansbold.ttf', 100)
    標題字1 = 標題字體.render('Wormy!', 對, 白色, 深綠色)
    標題字2 = 標題字體.render('Wormy!', 對, 綠色)

    程度1 = 0
    程度2 = 0
    while 對:
        顯示視窗.fill(背景顏色)
        旋轉1 = 旋轉方法(標題字1, 程度1)
        旋轉框框1 = 旋轉1.get_rect()
        旋轉框框1.center = (視窗寬度 / 2, 視窗長度 / 2)
        顯示視窗.blit(旋轉1, 旋轉框框1)

        旋轉2 = 旋轉方法(標題字2, 程度2)
        旋轉框框2 = 旋轉2.get_rect()
        旋轉框框2.center = (視窗寬度 / 2, 視窗長度 / 2)
        顯示視窗.blit(旋轉2, 旋轉框框2)

        按任意鍵進入遊戲畫面()

        if 檢查是否有按任意鍵():
            事件取得() # 得到事件中的按鍵
            return
        幕更新()
        每秒英尺的時間.tick(每秒英尺)
        程度1 += 3 # 每3程度旋轉一框架
        程度2 += 7 # 每7程度旋轉一框架


def 終止():
    結束()
    離開()


def 得到隨機位置():
    return {'x': 格子大小(0, 每小格寬度 - 1), 'y': 格子大小(0, 每小格長度 - 1)}


def 螢幕顯示遊戲結束():
    遊戲結束字體 = 字型類('freesansbold.ttf', 150)
    遊戲字體顏色 = 遊戲結束字體.render('Game', 對, 白色)
    結束字體顏色 = 遊戲結束字體.render('Over', 對, 白色)
    遊戲字體框框 = 遊戲字體顏色.get_rect()
    結束字體框框 = 結束字體顏色.get_rect()
    遊戲字體框框.midtop = (視窗寬度 / 2, 10)
    結束字體框框.midtop = (視窗寬度 / 2, 遊戲字體框框.height + 10 + 25)

    顯示視窗.blit(遊戲字體顏色, 遊戲字體框框)
    顯示視窗.blit(結束字體顏色, 結束字體框框)
    按任意鍵進入遊戲畫面()
    幕更新()
    時間等待(500)
    檢查是否有按任意鍵() # 清除事件隊列中的任何按鍵

    while 對:
        if 檢查是否有按任意鍵():
            事件取得() # 得到事件中的按鍵
            return

def 畫分數區(score):
    得分字體 = 字體.render('Score: %s' % (score), 對, 白色)
    得分框框 = 得分字體.get_rect()
    得分框框.topleft = (視窗寬度 - 120, 10)
    顯示視窗.blit(得分字體, 得分框框)


def 畫蟲蟲(蟲蟲的身體):
    for 座標 in 蟲蟲的身體:
        x = 座標['x'] * 單位尺寸
        y = 座標['y'] * 單位尺寸
        蟲蟲部分矩形= 方塊類(x, y, 單位尺寸, 單位尺寸)
        畫方形(顯示視窗, 深綠色, 蟲蟲部分矩形)
        蟲體部分矩形 = 方塊類(x + 4, y + 4, 單位尺寸 - 8, 單位尺寸 - 8)
        畫方形(顯示視窗, 綠色, 蟲體部分矩形)


def 畫蘋果(座標):
    x = 座標['x'] * 單位尺寸
    y = 座標['y'] * 單位尺寸
    蘋果框框 = 方塊類(x, y, 單位尺寸, 單位尺寸)
    畫方形(顯示視窗, 紅色, 蘋果框框)


def 畫網格():
    for x in 範圍(0, 視窗寬度, 單位尺寸): # 畫垂直線
        格子函式(顯示視窗, 深灰色, (x, 0), (x, 視窗長度))
    for y in 範圍(0, 視窗長度, 單位尺寸): # 畫水平線
        格子函式(顯示視窗, 深灰色, (0, y), (視窗寬度, y))


if __name__ == '__main__':
    主程式()

