import os

proxies = {
    'http': 'http://127.0.0.1:7896',
    'https': 'http://127.0.0.1:7896',
}

# 设置 HTTP 和 HTTPS 代理
os.environ['http_proxy'] = proxies['http']
os.environ['https_proxy'] = proxies['https']

import keyboard
import pyautogui
from paddleocr import PaddleOCR
import numpy as np
import pyttsx3
import translators as ts

p = (-1, -1)
p1, p2 = (-1, -1), (-1, -1)
ok = True
locating_mode = False  # 标志位，判断是否处于重新定位模式
ocr = PaddleOCR(use_angle_cls=False, cls=False, show_log=False, lang='en')
engine = pyttsx3.init()
txt = ''
txt_trans = ''

# 键盘初始化
def keyboard_init():
    keyboard.add_hotkey('l', locate)
    keyboard.add_hotkey('shift+k', location_init)
    keyboard.add_hotkey('d', work)
    keyboard.add_hotkey('f', translate)
    keyboard.add_hotkey('pause', pause)

# 定位
def locate():
    global p, locating_mode, p1, p2
    pos = pyautogui.position() 
    p = (pos.x, pos.y)
    
    # 检查是否处于定位模式
    if locating_mode:
        if p1 == (-1, -1):
            p1 = p
            print(f"左上角定位成功: {p1}")
        elif p2 == (-1, -1):
            p2 = p
            print(f"右下角定位成功: {p2}")
            locating_mode = False  # 退出定位模式
            print("重新定位完成！")
        else:
            print("已获取所有坐标，按 shift+k 重新开始定位。")
    else:
        print(f"当前鼠标位置: {p}")

# 暂停
def pause():
    global ok
    ok = not ok
    if ok: 
        print('结束暂停') 
    else: 
        print('开始暂停')

# 文本转语音
def TTS_init():
    global engine
    engine = pyttsx3.init()
    # 速率
    engine.setProperty('rate', 200) 
    # 音量
    engine.setProperty('volume',1.0)
    # 声音
    voices = engine.getProperty('voices')
    engine.setProperty('voice', voices[1].id)

# 位置预处理
def location_init():
    global p1, p2, locating_mode
    print('进入重新定位模式，按 L 键获取阅读窗口的左上角和右下角')
    p1, p2 = (-1, -1), (-1, -1)  # 重置坐标
    locating_mode = True  # 开启定位模式

# 讲话
def speak(txt):
    engine.say(txt)
    engine.startLoop(False)
    engine.iterate()
    engine.endLoop()

# 翻译
def translate():
    if not ok: return
    print(txt_trans)

# 阅读
def work():
    if not ok: return
    global ocr, txt, txt_trans
    w, h = p2[0] - p1[0], p2[1] - p1[1]
    if w <= 0 or h <= 0: 
        print('请确认获取坐标位置无误')
        return
    pic = pyautogui.screenshot(region=[p1[0], p1[1], w, h])
    pic = np.asarray(pic)
    result = ocr.ocr(pic, cls=False)
    result = result[0]
    if result is None: return
    txt = [line[1][0] for line in result]
    txt = ' '.join(txt)
    print(txt)
    speak(txt)
    txt_trans = ts.translate_text(txt, translator='iflyrec', from_language='auto', to_language='zh') # iflyrec, google  # proxies=proxies

if __name__ == '__main__':
    print('程序正在初始化')
    keyboard_init()
    TTS_init()
    print('程序运行中，按 D 键进行阅读，按 F 键显示翻译，按 shift-K 进行定位或重新定位，按 Pause 键暂停') 
    print('若想关闭程序，请直接关闭。')
    print('请按 shift-K 进行首次定位')
    keyboard.wait()
    engine.stop()
