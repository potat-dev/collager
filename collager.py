from PIL import Image
from tqdm import tqdm
from center_crop import center_crop, create_line
import os, logging

# settings

path = "C:\\Users\\Potato\\Desktop\\cats_dataset\\best"
width, height = (1920, 1080)
lines = 5
ratio_delta = 0.01
scale_method = Image.LANCZOS

log_level = logging.DEBUG
log_format = '[%(levelname)s]: %(message)s'

# set up logging

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

handler = TqdmLoggingHandler()
handler.setLevel(log_level)

handler.setFormatter(logging.Formatter(log_format))
logger.addHandler(handler)

# get all images in folder

images = [os.path.join(path, file) for file in os.listdir(path)]
images = [file for file in images
  if os.path.isfile(file)
  and any(
    [file.lower().endswith(ext) for ext in (".jpg", ".jpeg", ".png")]
  )
]

# calculate aspect ratio for each image

logger.debug(f"images in folder: {len(images)}")

cache_data = []
for image in tqdm(images[:], desc="calculating ratios"):
  try:
    img = Image.open(image)
    cache_data.append({"path": image, "ratio": img.width / img.height})
    img.close()
  except:
    logger.warning(f"unable to open the image: {os.path.basename(image)}")
    images.remove(image)

logger.debug(f"valid images: {len(images)}")

# create collage

collage = Image.new("RGBA", (width, height))
line_height = height // lines

for line_n in range(lines):
  line, iters = create_line(cache_data, width, line_height, ratio_delta, scale_method)
  logger.debug(f"line {line_n} created, {iters} iterations")
  collage.paste(line, (0, line_n * line_height))

collage.save("collage.png")
