import math
import random
import string
from io import BytesIO

from PIL import Image, ImageDraw, ImageFont
from random import choice


def gen_random_string(length:int) -> str:

    letters = string.ascii_lowercase + string.ascii_uppercase + string.digits
    confusing = {"1", "0", "o", "O", "L", "i", "l", "I"}
    valid = [c for c in letters if c not in confusing]
    return ''.join(choice(valid) for _ in range(length))

def random_color() -> tuple[int, int, int]:
    return random.randint(0,255),random.randint(0,255),random.randint(0,255)

def create_img(text:str):
    width,height = 240,80
    image = Image.new('RGB', (width,height),color=(255,255,255))
    draw = ImageDraw.Draw(image)

    font = ImageFont.load_default(size=45)

    bbox = draw.textbbox((0,0),text,font=font)

    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    x = (width-text_w)/2
    y = (height-text_h)/2

    draw.text((x,y),text,fill=random_color(),font=font)

    pixels = []
    amplitude = 4  # 扭曲幅度
    frequency = 0.1  # 扭曲频率

    for y in range(height):
        for x in range(width):
            # 计算扭曲后的 x 坐标
            offset_x = int(amplitude * math.sin(y * frequency))
            # 计算扭曲后的 y 坐标
            offset_y = int(amplitude * math.cos(x * frequency))

            # 获取原图片上扭曲后坐标处的颜色
            source_x = x + offset_x
            source_y = y + offset_y

            # 边界检查
            if 0 <= source_x < width and 0 <= source_y < height:
                pixel = image.getpixel((source_x, source_y))
            else:
                # 如果超出边界，则使用白色
                pixel = (255, 255, 255)

            pixels.append(pixel)

    image.putdata(pixels)

    for _ in range(4):
        start = (random.randint(0,width),random.randint(0,height))
        end = (random.randint(0,width),random.randint(0,height))
        draw.line([start,end], fill=random_color(),width=1)
    for _ in range(100):
        point = (random.randint(0,width),random.randint(0,height))
        draw.point(point,fill=random_color())

    buffer = BytesIO()
    image.save(buffer, format='PNG')
    img_bytes = buffer.getvalue()
    buffer.close()

    return img_bytes