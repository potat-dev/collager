from PIL import Image
from tqdm import tqdm
import os

# путь к папке с картинками
path = "C:\\Users\\Potato\\Desktop\\cats_dataset\\best"
cache_file = ".collage_data"

# штрина и высота
width, height = (1920, 1080)

# количество строк в коллаже
lines = 5

images = [os.path.join(path, file) for file in os.listdir(path)]
images = [file for file in images
  if os.path.isfile(file)
  and any(
    [file.lower().endswith(ext) for ext in (".jpg", "jpeg", ".png")]
  )
]

# здесь у нас в памяти находятся пути к картинкам в папке
# далее нужно прочитать файл, содержащий соотношения сторон картинок
# еще нужно проверить соответствие текущих файлов в папке и считанных из файла

# препроцессинг изображений
# рассчет соотношения сторон для каждого изображения и сохранение в файл

collage_data = os.path.join(path, cache_file)

if os.path.exists(collage_data):
  with open(collage_data, "r") as file:
    collage_data = [line.split(":") for line in file.read().splitlines()]
    collage_data = {file:ratio for file, ratio in collage_data}
    # здесь проверить хеш всех файлов
else:
  pass # здесь вычислять соотношения сторон и сохранять их

collage = Image.new("RGBA", (width, height))
height_per_line = height // lines

print(images)

for line_n in range(lines):
  # конструировать строку картинок и добавлять ее на коллаж
  pass
