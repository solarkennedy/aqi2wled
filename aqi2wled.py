#!/usr/bin/env python3
from purpleair import PurpleAir
import sys
from colour import Color
import requests
import os


lime = Color("lime")
green = Color("green")
yellow = Color("yellow")
orange = Color("orange")
red = Color("red")
purple = Color("magenta")
maroon = Color("maroon")
black = Color("black")

WLED = os.environ["WLED_HOST"]


def set_wled_color(c):
    print(f"Seeting the sunjar to {c}")
    brightness = 255
    r, g, b = int(c.red * 255), int(c.green * 255), int(c.blue * 255)
    u = f"http://{WLED}/win&T=1&A={brightness}&FX=0&SX=0&R={r}&G={g}&B={b}"
    print(u)
    requests.get(u)


def print_color(co):
    print(
        f"\x1b[38;2;{int(co.red*255)};{int(co.green*255)};{int(co.blue*255)}m{co}\x1b[0m"
    )


def color_step(start, end, r, step):
    print(f"Going from {start} to {end} in {r} steps, at step {step}")
    colors = list(start.range_to(end, r))
    for co in colors:
        print_color(co)
    print(colors)
    c = colors[step]
    return c


def get_aqi() -> int:
    p = PurpleAir(os.environ["PURPLEAIR_API_KEY"])
    s = p.get_sensor_data(os.environ["PURPLEAIR_SENSOR_ID"])
    ppm = s["sensor"]["pm2.5"]
    return int(ppm)


if __name__ == "__main__":
    aqi = get_aqi()
    if 0 <= aqi < 50:
        start = lime
        end = green
        r = 50
        step = aqi - 0
    elif 50 <= aqi < 100:
        start = yellow
        end = orange
        r = 50
        step = aqi - 50
    elif 100 <= aqi < 150:
        start = orange
        end = red
        r = 50
        step = aqi - 100
    elif 150 <= aqi < 200:
        start = red
        end = red
        r = 50
        step = aqi - 150
    elif 200 <= aqi < 300:
        start = purple
        end = purple
        r = 100
        step = aqi - 200
    elif 300 <= aqi < 1000:
        start = maroon
        end = black
        r = 700
        step = aqi - 300
    else:
        raise NotImplementedError(f"Didn't understand aqi {aqi}")
    c = color_step(start, end, r, step)
    h = c.hex_l.replace("#", "")
    print(f"AQI is {aqi} ({print_color(c)})")
    print(
        f'"AQI is {aqi} <br>![](https://raster.shields.io/badge/-{h}?style=flat-square)" | push-notification "Air Quality from Sunjar"'
    )

    set_wled_color(c)
