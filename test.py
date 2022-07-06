from collager import Collager

path = "D:/Projects/cats_dataset/best"
width, height = (1920, 1080)
lines = 5

collager = Collager(path)
collage = collager.collage(width, height, lines)
collage.save("collage.png")
