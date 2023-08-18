import random
import shelve
import sys
import json
import requests
from concurrent.futures import ThreadPoolExecutor, as_completed
from PIL import Image
from PIL import ImageDraw
from PIL import ImageFont

from django.conf import os

MEDIA_FOLDER = "./bookstore/ui/src/media/images/books"

podaci = shelve.open("./bookstore/db_work/shelve_data/podaci.dat", "r")
knjige = podaci["knjige"]


def full_dl(slika: str, naslov: str, i: int):
    d = dl(slika, i)
    n = create_new(d, naslov)
    delete_them(d, i)


def delete_them(slika, i):
    print(f"deleted: {slika}, {i}")
    os.remove(f"{MEDIA_FOLDER}/old/{slika}")
    os.remove(f"{MEDIA_FOLDER}/resized/{slika}")


def dl(url, i: int) -> str:
    res = requests.get(url)
    naziv = url.split("/")[9]
    with open(f"{MEDIA_FOLDER}/old/{naziv}", "wb") as f:
        f.write(res.content)
    return resize(naziv, i)


def to_dict(item):
    obj = {"title": "", "img": "", "price": ""}
    obj["title"] = item[0]
    obj["img"] = item[1]
    obj["price"] = item[2]
    return obj


def resize(naziv: str, i: int) -> str:
    image = None
    try:
        image = Image.open(f"{MEDIA_FOLDER}/old/{naziv}")
    except:
        image = Image.open(f"{MEDIA_FOLDER}/default.jpg")
    new_image = image.resize((200, 150))
    new_image.save(f"{MEDIA_FOLDER}/resized/{naziv}")
    return naziv


def new_rgb():
    while True:
        r = random.randint(0, 201)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        if r > 210 and g > 210:
            continue
        return (r, g, b)


def create_rect(img, naslov):
    size = int(len(naslov) / 24)
    w, h = 220, 190
    shape = ((0, 0), (450, 55 * (size + 1)))
    draw = ImageDraw.Draw(img)
    draw.rectangle(shape, fill="white")


def create_new(slika: str, naslov: str):
    color = new_rgb()
    img = Image.new(mode="RGB", size=(450, 650), color=color)
    try:
        img2 = Image.open(f"{MEDIA_FOLDER}/resized/{slika}")
        img2 = img2.resize((350, 400))
    except:
        img2 = Image.open(f"{MEDIA_FOLDER}/default.jpg")
        img2 = img2.resize((350, 400))
        return
    create_rect(img, naslov)
    text = ImageDraw.Draw(img)
    mf = ImageFont.truetype("OpenSans-Bold.ttf", size=30)
    text.text((15, 15), naslov, (0, 0, 0), font=mf)
    img.paste(img2, (150, 250))
    img.save(f"{MEDIA_FOLDER}/real/{slika}")
    return "ok"


def start():
    with ThreadPoolExecutor(max_workers=8) as executor:
        futures = []
        books = {"books": []}
        for i in range(30, 500):
            knjiga = knjige[i]
            naslov: str = knjiga[0]
            slika: str = knjiga[1]
            s = [(naslov[i : i + 24]) for i in range(0, len(naslov), 24)]
            naslov = ""
            for ch in s:
                naslov += f"{ch}-\n"
            naslov = naslov[:-2] + ""
            futures.append(executor.submit(full_dl, slika, naslov, i))
        for future in as_completed(futures):
            res = future.result()
        #     books["books"].append(res)
        # with open("books.json", "w") as f:
        #     json.dump(books, f, ensure_ascii=False)
    podaci.close()
