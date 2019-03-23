import collections
import math
import random
from PIL import Image


img  = Image.open("example_screenshot.png")

# PNG를 JPEG로 저장하기 위해서 필요함
img = img.convert('RGB')
WIDTH, HEIGHT = img.size

wanted_num_of_crops = random.randint(5, 10)
div = math.floor(HEIGHT / wanted_num_of_crops)

print(f"이미지의 높이는 {HEIGHT} 정도 입니다.")
print(f"이미지를 {wanted_num_of_crops}개로 나누면, 약 {div} 정도의 사이즈를 가집니다.")
print(f"{wanted_num_of_crops}개의 이미지로 나눕니다.")

first_div = random.randint(10, div)

num_of_crops = 0
cur_height = first_div
crop_positions = []

while (cur_height < HEIGHT - 10) and (num_of_crops < wanted_num_of_crops):
     cur_height = random.randint(cur_height, cur_height + div)
     crop_positions.append(cur_height)
     num_of_crops += 1

print(crop_positions)

# (가로 시작점, 세로 시작점, 가로 범위, 세로 범위)
Area = collections.namedtuple("Area", "start_width start_height end_width end_height")
crop_area = Area(start_width=0, start_height=0, end_width=WIDTH, end_height=0)
for num, crop_height in enumerate(crop_positions, start=1):
    if num < wanted_num_of_crops:
        crop_area = Area._make([0, crop_area.end_height+1, WIDTH, crop_height])
        cropped_img = img.crop(crop_area)
        cropped_img.save(f"{num}.jpeg", format='JPEG')
    else:
        crop_area = Area._make([0, crop_area.end_height+1, WIDTH, HEIGHT])
        cropped_img = img.crop(crop_area)
        cropped_img.save(f"{num}.jpeg", format='JPEG')
        break
print(num)
