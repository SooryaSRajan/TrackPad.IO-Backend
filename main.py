import time
import win32api
import win32con
from flask import Flask, request, render_template
from flask_socketio import SocketIO
from engineio.async_drivers import gevent
from eventlet.hubs import epolls
import gevent
import geventwebsocket
from geventwebsocket import *
import subprocess
import pyautogui


def wlan_ip():
    result = subprocess.run('ipconfig', stdout=subprocess.PIPE, text=True).stdout.lower()
    scan = 0
    for i in result.split('\n'):
        if 'wireless' in i: scan = 1
        if scan:
            if 'ipv4' in i: return i.split(':')[1].strip()


app = Flask(__name__)
socket_ = SocketIO(app)
socket_.init_app(app, cors_allowed_origins="*")


@app.route('/')
def index():
    return render_template('index.html')


@socket_.on('mouse_data')
def displace_mouse(x, y):
    win32api.mouse_event(win32con.MOUSEEVENTF_MOVE, int(x), int(y))


@socket_.on('single_tap')
def single_tap():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


@socket_.on('double_tap')
def double_tap():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)
    time.sleep(.1)
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


@socket_.on('right_click_down')
def right_click_down():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTDOWN, 0, 0)


@socket_.on('right_click_up')
def right_click_up():
    win32api.mouse_event(win32con.MOUSEEVENTF_RIGHTUP, 0, 0)


@socket_.on('left_click_down')
def left_click_down():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, 0, 0)


@socket_.on('left_click_up')
def left_click_up():
    win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, 0, 0)


@socket_.on('scroll')
def scroll(x):
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, int(x), 0)


@socket_.on('get_ip_address')
def get_ip():
    print('received')
    ip = wlan_ip()
    if ip is None:
        socket_.emit('ip_recv', 'ERROR: No network found')
    else:
        socket_.emit('ip_recv', wlan_ip() + ':5000')


@socket_.on('scroll')
def scroll(x):
    win32api.mouse_event(win32con.MOUSEEVENTF_WHEEL, 0, 0, int(x), 0)


@socket_.on('play')
def play():
    pyautogui.press('playpause')


@socket_.on('increase_volume')
def increase_volume():
    pyautogui.press('volumeup')


@socket_.on('decrease_volume')
def decrease_volume():
    pyautogui.press('volumedown')


@socket_.on('mute_volume')
def mute_volume():
    pyautogui.press('volumemute')


@socket_.on('copy')
def copy():
    pyautogui.hotkey('ctrl', 'c')


@socket_.on('paste')
def paste():
    pyautogui.hotkey('ctrl', 'v')


@socket_.on('undo')
def undo():
    pyautogui.hotkey('ctrl', 'z')


@socket_.on('redo')
def redo():
    pyautogui.hotkey('ctrl', 'shift', 'z')


@socket_.on('cut')
def cut():
    pyautogui.hotkey('ctrl', 'x')


@socket_.on('key_down')
def key_down(key):
    pyautogui.keyDown(key)


@socket_.on('key_up')
def key_down(key):
    pyautogui.keyUp(key)


if __name__ == '__main__':
    socket_.run(app, debug=False, host='0.0.0.0', port=5000)
