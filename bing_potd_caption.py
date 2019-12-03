#!/usr/bin/env python3

import requests
import wget
import json
import os
from PIL import Image, ImageDraw, ImageFont

url_base = 'https://www.bing.com/'
url_json = 'https://www.bing.com/HPImageArchive.aspx?format=js&idx=0&n=1'

folder_img_out = "/home/sebastian/Pictures/my_wallpaper/"
folder_temp = "/tmp"
FONT_FILENAME = "/usr/share/fonts/truetype/freefont/FreeSans.ttf"

r = requests.get(url_json)

if r.status_code == 200:
    raw_data = json.loads(r.text)

    # Extract useful data from json file
    url_img_tail = raw_data["images"][0]["url"]
    img_name = raw_data["images"][0]["startdate"]
    img_description = raw_data["images"][0]["copyright"]

    year, month, day = (img_name[:4], img_name[4:6], img_name[6:8])
    img_caption = "%s - %s/%s/%s" % (img_description, year, month, day)

    temp_filename = os.path.join(folder_temp, img_name)
    try:
        os.remove(temp_filename)
    except FileNotFoundError:
        pass

    url_img = url_base + url_img_tail
    img_temp_filename = wget.download(url_img, temp_filename)

    img = Image.open(img_temp_filename)
    img_rgba = img.convert("RGBA")

    font = ImageFont.truetype(FONT_FILENAME, 16)
    font_factor = 3.6
    text_length = len(img_caption) * font_factor

    width, height = img.size
    pad = 5
    txt_box = {"x0": round(width / 2) - text_length - pad,
               "y0": round(height * 0.95 - pad),
               "x1": round(width / 2) + text_length + pad,
               "y1": round(height * 0.965 + pad)}

    # make a blank image for the text, initialized to transparent text color
    txt_img = Image.new("RGBA", img.size, (255, 255, 255, 0))
    draw_txt = ImageDraw.Draw(txt_img)

    draw_txt.rectangle([txt_box["x0"], txt_box["y0"], txt_box["x1"], txt_box["y1"]],
                       fill=(0, 0, 0, 60))

    draw_txt.text((txt_box["x0"] + pad, txt_box["y0"] + pad),
                  img_caption,
                  anchor="pepe",
                  fill=(255, 255, 255),
                  font=font)

    out_img = Image.alpha_composite(img_rgba, txt_img)

    out_img_filename = "%s.%s" % (img_name, img.format.lower())
    out_img_path = os.path.join(folder_img_out, out_img_filename)
    out_img.convert("RGB").save(out_img_path, format=img.format)

    print("\n", out_img_path, "\n", img_caption)
