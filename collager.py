from PIL import Image
from tqdm import tqdm
import os, logging

log_level = logging.DEBUG

logger = logging.getLogger(__name__)
logger.setLevel(log_level)

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

tqdm_handler = TqdmLoggingHandler()
tqdm_handler.setLevel(log_level)

formatter = logging.Formatter('[%(levelname)s]: %(message)s')
tqdm_handler.setFormatter(formatter)

# add the handler to the logger
logger.addHandler(tqdm_handler)

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
    cache_data[image] = ratio
    img.close()
  except:
    logger.warning(f"unable to open the image: {os.path.basename(image)}")
    images.remove(image)

logger.debug(f"valid images: {len(images)}")

collage = Image.new("RGBA", (width, height))

for line_n in tqdm(range(lines)):
  # logger.debug(f"line: {line_n}") # handler is working!
  pass # конструировать строку картинок и добавлять ее на коллаж