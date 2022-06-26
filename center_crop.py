from PIL import Image
from random import choice

# функция для обрезки изображения по центру с заданным соотношением сторон
def center_crop(img, height, crop_ratio, scale_method):
  crop_ratio = crop_ratio
  ideal_width = round(height * crop_ratio)
  if img.width / img.height > crop_ratio:
    # crop the left and right edges:
    offset = round((img.width - crop_ratio * img.height) / 2)
    resize = (offset, 0, img.width - offset, img.height)
  else:
    # crop the top and bottom edges:
    offset = round((img.height - img.width / crop_ratio) / 2)
    resize = (0, offset, img.width, img.height - offset)
  return img.crop(resize).resize((ideal_width, height), scale_method)

# функция для создания одной линии коллажа
def create_line(images, width, line_height, ratio_delta=0.01, scale_method=Image.LANCZOS):
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
      # TODO: не допускать повторы изображений
      # 3 уровня настройки повторов
      # 1) разрешить любые повторы
      # 2) запретить повторы в одной линии
      # 3) запретить повторы во всем коллаже
    if sum_ratios(selected_ratios) > max_ratio:
      selected_ratios = []

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
    img = center_crop(img, line_height, new_ratios[i], scale_method)
    # append img to line
    line.paste(img, (current_x, 0))
    # TODO: сначала сохранять изображения в массив
    # потом считать их общую ширину и создавать линию данной ширины
    # а потом растягивать линию до нужного размера
    # тогда не будет черных полос в конце
    current_x += img.width
    img.close()
  
  return line.resize((width, line_height), scale_method), iters
