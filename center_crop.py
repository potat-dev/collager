from PIL import Image

def center_crop(img, height, crop_ratio):
  crop_ratio = crop_ratio
  ideal_width = int(height * crop_ratio)
  if img.width / img.height > crop_ratio:
    # crop the left and right edges:
    offset = (img.width - crop_ratio * img.height) / 2
    resize = (offset, 0, img.width - offset, img.height)
  else:
    # crop the top and bottom edges:
    offset = (img.height - img.width // crop_ratio) / 2
    resize = (0, offset, img.width, img.height - offset)
  return img.crop(resize).resize((ideal_width, height), Image.BICUBIC)

image = Image.open('cat.jpg')
image = center_crop(image, 200, 1.25)
image.save('cat_crop.jpg')
print(image.size, "aspect ratio:", image.width / image.height)