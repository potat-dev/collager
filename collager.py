from PIL import Image
from tqdm import tqdm
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
path = "C:\\Users\\Potato\\Desktop\\cats_dataset"

# штрина и высота
width, height = (1920, 1080)

# количество строк в коллаже
lines = 5
height_per_line = height // lines

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

cache_data = {}
for image in tqdm(images[:], desc="calculating ratios"):
  try:
    img = Image.open(image)
    width, height = img.size
    ratio = width / height
    cache_data[image] = {"width": width, "height": height, "ratio": ratio}
    img.close()
  except:
    logger.warning(f"unable to open the image: {os.path.basename(image)}")
    images.remove(image)

logger.debug(f"valid images: {len(images)}")

# create collage
collage = Image.new("RGBA", (width, height))
for line_n in range(lines):
  pass # конструировать строку картинок и добавлять ее на коллаж

# dump cache_data to file with json for debug
# import json
# with open("cache_data.json", "w") as f:
#   json.dump(cache_data, f)