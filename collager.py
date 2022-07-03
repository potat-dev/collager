from PIL import Image
from collage_utils import *


class Collager:
  #? repeat control consts
  # ALLOW_REPEATS = 0
  # NO_REPEATS = 1
  # NO_REPEATS_LINE = 2
  # NO_REPEATS_NEIGHBOR_LINES = 3

  default_ratio_delta = 0.05
  default_scale_method = Image.LANCZOS

  def __init__(self, path):
    self.images = get_files(path, ['jpg', 'jpeg', 'png'])
    self.image_data = get_aspect_ratios(self.images)

  def collage(self, width, height, lines,
              ratio_delta=default_ratio_delta,
              scale_method=default_scale_method): # repeat_mode=ALLOW_REPEATS):

    collage = Image.new("RGBA", (width, height))
    line_height = height // lines

    for line_n in range(lines):
      line, iters = create_line(self.image_data, width, line_height, ratio_delta, scale_method)
      # logger.debug(f"line {line_n} created, {iters} iterations")
      collage.paste(line, (0, line_n * line_height))

    return collage

  # устанавливает новый путь и сканирует его
  # TODO: добавление нескольких директорий
  def update_path(path):
    pass


if __name__ == "__main__":
  path="C:\\Users\\Potato\\Desktop\\cats_dataset\\best"
  width, height = (1920, 1080)
  lines = 5
  ratio_delta = 0.05
  scale_method = Image.LANCZOS
  # repeat_mode = Collager.ALLOW_REPEATS

  collager = Collager(path)
  collage = collager.collage(width, height, lines, ratio_delta, scale_method)
  collage.save("collage.png")