import json
import winsound
from time import sleep

import cv2
import numpy as np
import pyautogui as root


def start_timer(sec):
    for i in range(0, sec - 1):
        sleep(1)
        winsound.Beep(300, 70)
    sleep(1)
    winsound.Beep(500, 540)


def get_json(json_f):
    with open(json_f) as f_obj:
        tile_list = json.load(f_obj)
    return tile_list


start_timer(3)

# t_list = ['draco_black.png', 'draco_green.png', 'draco_red.png', 'flower_1.png', 'flower_2.png', 'flower_3.png',
#           'flower_4.png', 'jap_1.png', 'jap_2.png', 'jap_3.png', 'jap_4.png', 'jap_5.png', 'jap_6.png', 'jap_7.png',
#           'jap_8.png', 'jap_9.png', 'season_1.png', 'season_2.png', 'season_3.png', 'season_4.png', 'stick_1.png',
#           'stick_2.png', 'stick_3.png', 'stick_4.png', 'stick_5.png', 'stick_6.png', 'stick_7.png', 'stick_8.png',
#           'stick_9.png', 'weel_1.png', 'weel_2.png', 'weel_3.png', 'weel_4.png', 'weel_5.png', 'weel_6.png',
#           'weel_7.png', 'weel_8.png', 'weel_9.png', 'wind_e.png', 'wind_n.png', 'wind_s.png', 'wind_w.png']
flag = True
while flag:
    flag = False
    root.screenshot(region=(0, 0, 1920, 1080), imageFilename='main_field.png')  # сделали скриншот всего экрана
    img_main = cv2.imread('main_field.png')
    j = get_json('tile_json.json')
    flowers_a, season_a = [], []
    for tile_name in j:
        # print(tile_name)
        img_tile = cv2.imread('tiles/' + tile_name)
        h, w = img_tile.shape[:-1]
        res = cv2.matchTemplate(img_main, img_tile, cv2.TM_CCOEFF_NORMED)
        threshold = j[tile_name]['treshhold']
        loc = np.where(res >= threshold)
        x, y = 0, 0
        temp_l = []
        for pt in sorted(list(zip(*loc[::-1]))):  # Switch collumns and rows
            if abs(x - pt[0]) > 10 or abs(y - pt[1]) > 10:
                x, y = pt[0], pt[1]
                # cv2.rectangle(img_main, pt, (pt[0] + w, pt[1] + h), (0, 0, 255), 2)
                temp_l.append((x, y))
                if tile_name[:6] == 'season':
                    season_a.append((x, y))
                if tile_name[:6] == 'flower':
                    season_a.append((x, y))
                flag = True
        j[tile_name]['coord'] = temp_l
        if len(temp_l) > 1:
            for x in temp_l:
                root.moveTo(x[0] + 10, x[1] + 10)
                root.click()
            root.moveTo(10, 100)
            root.click()
    if len(flowers_a) > 1:
        for x in flowers_a:
            root.moveTo(x[0] + 10, x[1] + 10)
            root.click()
        root.moveTo(10, 100)
        root.click()
    if len(season_a) > 1:
        for x in season_a:
            root.moveTo(x[0] + 10, x[1] + 10)
            root.click()
        root.moveTo(10, 100)
        root.click()
