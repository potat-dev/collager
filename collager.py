from PIL import Image
from tqdm import tqdm
from random import choice
import os, logging

from center_crop import center_crop

log_level = logging.DEBUG
log_format = '[%(levelname)s]: %(message)s'

class TqdmLoggingHandler(logging.Handler):
  def __init__(self, level=logging.NOTSET):
    super().__init__(level)

  def emit(self, record):
    try:
      msg = self.format(record)
      tqdm.write(msg)
      self.flush()
    except Exception:
      self.handleError(record)

logger = logging.getLogger(__name__)
handler = TqdmLoggingHandler()

logger.setLevel(log_level)
handler.setLevel(log_level)

handler.setFormatter(logging.Formatter(log_format))
logger.addHandler(handler)

# путь к папке с картинками
path = "C:\\Users\\Potato\\Desktop\\cats_dataset\\best"

# штрина и высота
width, height = (1920, 1080)

# количество строк в коллаже
lines = 5
line_height = height // lines

# получаем все изображения в папке
images = [os.path.join(path, file) for file in os.listdir(path)]
images = [file for file in images
  if os.path.isfile(file)
  and any(
    [file.lower().endswith(ext) for ext in (".jpg", ".jpeg", ".png")]
  )
]

# рассчет соотношения сторон для каждого изображения
logger.debug(f"images in folder: {len(images)}")

cache_data = []
for image in tqdm(images[:], desc="calculating ratios"):
  try:
    img = Image.open(image)
    cache_data.append(
      {
        "path": image,
        "width": img.width,
        "height": img.height,
        "ratio": img.width / img.height
      }
    )
    img.close()
  except:
    logger.warning(f"unable to open the image: {os.path.basename(image)}")
    images.remove(image)

logger.debug(f"valid images: {len(images)}")

# функция для создания одной линии коллажа
def create_line(images, width, line_height, ratio_delta=0.01):
  def sum_ratios(items):
    return sum([item["ratio"] for item in items])

  height_shift = ratio_delta * line_height
  line_ratio = width / line_height
  min_ratio = width / (line_height + height_shift)
  max_ratio = width / (line_height - height_shift)

  iters = 0
  selected_ratios = []
  while selected_ratios == []:
    iters += 1
    while sum_ratios(selected_ratios) < min_ratio:
      selected_ratios.append(choice(images))
    if sum_ratios(selected_ratios) > max_ratio:
      selected_ratios = []
  
  # log iters
  logger.debug(f"iters: {iters}")

  curr_ratio = sum_ratios(selected_ratios)
  ratio_delta = line_ratio - curr_ratio

  old_ratios = [item["ratio"] for item in selected_ratios]
  new_ratios = [
    item["ratio"] + ratio_delta * item["ratio"] / curr_ratio
    for item in selected_ratios
  ]

  # создаем изображение с размерами width и line_height
  line = Image.new("RGB", (width, line_height))
  current_x = 0

  # применяем новые параметры к изображениям
  for i, image in enumerate(selected_ratios):
    img = Image.open(image["path"])
    img = center_crop(img, line_height, new_ratios[i])
    # append img to line
    line.paste(img, (current_x, 0))
    current_x += img.width
    img.close()
  
  return line.resize((width, line_height), Image.LANCZOS)

# create collage
collage = Image.new("RGBA", (width, height))
for line_n in range(lines):
  line = create_line(cache_data, width, line_height)
  collage.paste(line, (0, line_n * line_height))
  pass # конструировать строку картинок и добавлять ее на коллаж

# save collage
collage.save("collage.png")

# dump cache_data to file with json for debug
# import json
# with open("cache_data.json", "w") as f:
#   json.dump(cache_data, f)