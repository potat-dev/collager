from collage_utils import *
from sys import stderr
from PIL import Image

from loguru import logger
logger.remove()

log_level = "DEBUG"
log_format = "{module} : <lvl>{level}</lvl> : {message}"
logger.add(stderr, level=log_level, format=log_format)


class Collager:
    '''
    Collager class - for generating collages from random images

    Methods:
    - collage: creates a collage from the image_data
    - update_path: updates the path and scans it for images
    '''
    file_extensions = ["jpg", "jpeg", "png", "bmp"]

    def __init__(self, path: str | list[str]) -> None:
        '''
        Creates a new collager instance
        - scans the given path / multiple paths for images
        - calculates their aspect ratios
        '''
        match path:
            case str():
                self.image_paths = [path]
            case list():
                self.image_paths = path
            case _:
                raise TypeError("path must be a string or a list of strings")

        self.update_path(self.image_paths)

    def collage(self, width: int, height: int, lines: int, ratio_delta: int = 0.05,
                scale_method=Image.Resampling.LANCZOS) -> Image.Image:
        '''
        Creates a collage from the image_data
        - width: the width of the collage
        - height: the height of the collage
        - lines: the number of lines in the collage
        - ratio_delta: the maximum variation of the aspect ratio when cropping images
        - scale_method: the method to use for scaling the images

        TODO:
        - add support for horizontal / vertical collages
        - add duplicates control (e.g. no duplicates in a line, no duplicates in a neighbor lines, etc.)
        '''
        collage = Image.new("RGBA", (width, height))
        line_height = height // lines

        for line_n in range(lines):
            line = create_line(self.image_data, width,
                               line_height, ratio_delta, scale_method)
            collage.paste(line, (0, line_n * line_height))

        return collage

    def update_path(self, path: str | list[str]) -> None:
        '''
        Updates the path and scans it for images
        Then updates the image_data with new aspect ratios
        '''
        match path:
            case str():
                self.image_files = get_files(path, self.file_extensions)
                self.image_data = get_aspect_ratios(self.image_files)
            case list():
                self.image_files = []
                for p in path:
                    self.image_files += get_files(p, self.file_extensions)
                self.image_data = get_aspect_ratios(self.image_files)
            case _:
                raise TypeError("path must be a string or a list of strings")
