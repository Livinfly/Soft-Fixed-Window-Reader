import keyboard
import pyautogui
from paddleocr import PaddleOCR
import numpy as np
import pyttsx3
import translators as ts

p = (-1, -1)
p1, p2 = (-1, -1), (-1, -1)
ok = True
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
    global p
    pos = pyautogui.position() 
    p = (pos.x, pos.y)
# 暂停
def pause():
    global ok
    ok = not ok
    if ok: print('结束暂停') 
    else: print('开始暂停')
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
    global p, p1, p2
    print('首次，按 L 键获取阅读窗口的左上角')
    keyboard.wait('l')
    p1 = p
    p = (-1, -1)
    print('左上角坐标', p1)
    print('再次，按 L 键获取阅读窗口的右下角')
    keyboard.wait('l')
    p2 = p
    p = (-1, -1)
    print('右下角坐标', p2)
    return p1, p2

# 讲话
def speak(txt):
    engine.say(txt)
    # engine.runAndWait()
    engine.startLoop(False)
    engine.iterate()
    engine.endLoop()

# 翻译
def translate():
    print(txt_trans)
# 阅读
def work():
    if not ok: return
    global ocr, txt, txt_trans
    w, h = p2[0]-p1[0], p2[1]-p1[1]
    if w <= 0 or h <= 0: 
        print('请确认获取坐标位置无误')
        input('按任意键结束')
        exit(0)
    pic = pyautogui.screenshot(region=[p1[0], p1[1], w, h])
    pic = np.asarray(pic)
    result = ocr.ocr(pic, cls=False)
    result = result[0]
    if len(result) == 0: return
    txt =  [line[1][0] for line in result]
    txt = ' '.join(txt)
    print(txt)
    speak(txt)
    txt_trans = ts.translate_text(txt, translator='iflyrec', from_language='auto', to_language='zh') # 若使用代理，需要关闭。

if __name__ == '__main__':
    print('程序正在初始化')
    keyboard_init()
    location_init()
    TTS_init()
    print('程序运行中，按 D 键进行阅读，按 F 键显示翻译，按 shift-L 重新进行定位，按 P 键暂停') 
    print('若想关闭程序，请直接关闭。')
    keyboard.wait()
    engine.stop()