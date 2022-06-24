from PIL import Image
from tqdm import tqdm
import os

# вычисляет хэш нескольких файлов
from hashlib import md5
def files_hash(files):
  temp = md5()
  for file in tqdm(files, desc="calculating files hash"):
    with open(file, "rb") as f:
      for chunk in iter(lambda: f.read(4096), b""):
        temp.update(chunk)
  return temp.hexdigest()

# путь к папке с картинками
path = "C:\\Users\\Potato\\Desktop\\cats_dataset"
cache_file = ".cache_data"
cache_path = os.path.join(path, cache_file)

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
    [file.lower().endswith(ext) for ext in (".jpg", "jpeg", ".png")]
  )
]

# всегда нужно вычислять хэш изображений
images_hash = files_hash(images)
print("image hash:", images_hash)

# проверяем кеш
if os.path.exists(cache_path):
  with open(cache_path, "r") as file:
    cache_hash = file.readline().strip()
    print("cache hash:", cache_hash)
    print("valid:", images_hash == cache_hash)
    cache_data = [line.split(" | ") for line in file.read().splitlines()]
    cache_data = {file:ratio for file, ratio in cache_data}

if not os.path.exists(cache_path) or cache_hash != images_hash:
  # рассчет соотношения сторон для каждого изображения и сохранение в файл
  cache_data = {}
  for image in tqdm(images, desc="calculating ratios\t"):
    # TODO: добавить проверку на неправильный формат изображения или битый файл
    img = Image.open(image)
    width, height = img.size
    ratio = width / height
    cache_data[image] = ratio
    img.close()
  print("saving cache")
  with open(cache_path, "w") as file:
    file.write(images_hash + "\n")
    for image, ratio in cache_data.items():
      file.write(f"{image} | {ratio}\n")

collage = Image.new("RGBA", (width, height))

for line_n in range(lines):
  pass # конструировать строку картинок и добавлять ее на коллаж