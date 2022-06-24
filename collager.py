from PIL import Image
from tqdm import tqdm
import hashlib
import os

# путь к папке с картинками
path = "C:\\Users\\Potato\\Desktop\\cats_dataset\\best"
cache_file = ".cache_data"
cache_data = os.path.join(path, cache_file)

# штрина и высота
width, height = (1920, 1080)

# количество строк в коллаже
lines = 5
height_per_line = height // lines


if os.path.exists(cache_data):
  with open(cache_data, "r") as file:
    files_hash = file.readline().strip()
    cache_data = [line.split(" | ") for line in file.read().splitlines()]
    cache_data = {file:ratio for file, ratio in cache_data}

images = [os.path.join(path, file) for file in os.listdir(path)]
images = [file for file in images
  if os.path.isfile(file)
  and any(
    [file.lower().endswith(ext) for ext in (".jpg", "jpeg", ".png")]
  )
]

def file_hash(file):
  temp = hashlib.md5()
  with open(file, "rb") as f:
    for chunk in iter(lambda: f.read(4096), b""):
      temp.update(chunk)
  return temp.hexdigest()

images_md5 = ""
for image in tqdm(images):
  images_md5 += file_hash(image)

images_md5 = hashlib.md5(images_md5.encode("utf-8")).hexdigest()
print(images_md5)

print(files_hash == images_md5)

# здесь у нас в памяти находятся пути к картинкам в папке
# далее нужно прочитать файл, содержащий соотношения сторон картинок
# еще нужно проверить соответствие текущих файлов в папке и считанных из файла

# препроцессинг изображений
# рассчет соотношения сторон для каждого изображения и сохранение в файл

collage = Image.new("RGBA", (width, height))

for line_n in range(lines):
  pass # конструировать строку картинок и добавлять ее на коллаж
