from PIL import Image
import logging

from collage_utils import *

# collager class template

class Collager:
  #? repeat control consts
  # ALLOW_REPEATS = 0
  # NO_REPEATS = 1
  # NO_REPEATS_LINE = 2
  # NO_REPEATS_NEIGHBOR_LINES = 3

  def __init__(self, path):
    self.images = get_files(path, ['jpg', 'jpeg', 'png'])
    self.image_data = get_aspect_ratios(self.images)

  def collage(self, width, height, lines, ratio_delta=0.05, scale_method=Image.LANCZOS): # repeat_mode=ALLOW_REPEATS):
    collage = Image.new("RGBA", (width, height))
    line_height = height // lines

    for line_n in range(lines):
      line, iters = create_line(self.image_data, width, line_height, ratio_delta, scale_method)
      # logger.debug(f"line {line_n} created, {iters} iterations")
      collage.paste(line, (0, line_n * line_height))

    return collage

# settings

path = "C:\\Users\\Potato\\Desktop\\cats_dataset\\best"
width, height = (1920, 1080)
lines = 5
ratio_delta = 0.05
scale_method = Image.LANCZOS
# repeat_mode = Collager.ALLOW_REPEATS

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

# run

collager = Collager(path)
collage = collager.collage(width, height, lines, ratio_delta, scale_method)
collage.save("collage.png")