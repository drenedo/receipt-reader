import click
import cv2
import trocr
from craft import craft
from PIL import Image
from typing import List

DEFAULT_LINE_RANGE = 70
DEFAULT_MARGIN = 7


def scan(image_src, margin: int = DEFAULT_MARGIN, trocr_pretrained: str = None):
    """
    Main method for apply Optical Character Recognition
    """
    image = cv2.imread(image_src)
    height = image.shape[0]
    width = image.shape[1]
    craft_boxes = craft(image)
    text = []
    processor = trocr.get_processor() if trocr_pretrained is None else trocr.get_processor(trocr_pretrained)
    model = trocr.get_model() if trocr_pretrained is None else trocr.get_model(trocr_pretrained)
    click.echo(f"height {height} and width {width}", err=True)
    for unit in craft_boxes:
        try:
            x1 = unit.x1
            x2 = unit.x2
            y1 = unit.y1
            y2 = unit.y2
            click.echo(f"Unit ({x1}, {y1})  ({x2}, {y2})", err=True)
            if x1 != x2 or y1 != y2:
                final_y1 = y1 - margin if y1 - margin > 0 else 0
                final_x1 = x1 - margin if x1 - margin > 0 else 0
                final_x2 = x2 + margin if x2 + margin <= width else width
                final_y2 = y2 + margin if y2 + margin <= height else height
                click.echo(f"fUnit ({final_x1}, {final_y1})  ({final_x2}, {final_y2})", err=True)
                crop_img = image[final_y1:final_y2, final_x1:final_x2]
                text_found = trocr.scan(Image.fromarray(crop_img), processor, model)
                text.append(TextCoordinates(text_found, Coord(x1, y1), Coord(x2, y2)))
        except ValueError:
            click.echo("Error ", err=True)
    return Result(text)


class Coord:
    """
    Object that represents the cartesian coordinates. The first pixel of a image will be 0,0.
    """
    def __init__(self, x, y):
        self.x = x
        self.y = y

    def to_json(self):
        return {"x": self.x,
                "y": self.y}


class TextCoordinates:
    """
    This object contains some text in the image and its cartesian coordinates.
    The two pairs of cartesian coordinates represent the box that contains the text
    """
    def __init__(self, text, coord_1: Coord, coord_2: Coord):
        self.text = text
        self.coord_1 = coord_1
        self.coord_2 = coord_2

    def to_json(self):
        return {"text": self.text,
                "1": self.coord_1.to_json(),
                "2": self.coord_2.to_json()}


class Result:
    """
    Object returned at the end of the operation with all the information
    """
    def __init__(self, parts):
        self.parts = parts

    def to_json(self, line_range: int = DEFAULT_LINE_RANGE):
        return {"parts": [i.to_json() for i in self.parts],
                "lines": [i.to_json() for i in self.get_lines(line_range)]}

    def get_lines(self, line_range: int = DEFAULT_LINE_RANGE):
        lines: List[Line] = []
        for part in self.parts:
            coincidence: Line = next((l for l in lines if l.overlaps(part, line_range)), None)
            if coincidence is None:
                lines.append(Line(part))
            else:
                coincidence.append(part)
        return lines


class Line:
    """
    The line is a group of TextCoordinates. This object composes the text of a line
    """
    def __init__(self, part: TextCoordinates):
        self.start = part.coord_1.y if part.coord_1.y <= part.coord_2.y else part.coord_2.y
        self.end = part.coord_2.y if part.coord_1.y <= part.coord_2.y else part.coord_1.y
        self.parts = [part]

    def append(self, part: TextCoordinates):
        start = part.coord_1.y if part.coord_1.y <= part.coord_2.y else part.coord_2.y
        end = part.coord_2.y if part.coord_1.y <= part.coord_2.y else part.coord_1.y
        if start < self.start:
            self.start = start
        if end > self.end:
            self.end = end
        self.parts.append(part)

    def overlaps(self, part: TextCoordinates, line_range: int):
        coord_start = part.coord_1.y if part.coord_1.y <= part.coord_2.y else part.coord_2.y
        coord_end = part.coord_2.y if part.coord_1.y <= part.coord_2.y else part.coord_1.y
        return abs(coord_start - self.start) + abs(coord_end - self.end) < line_range

    def get_text(self):
        def get_x(val: TextCoordinates):
            return val.coord_1.x

        self.parts.sort(key=get_x)
        return ' '.join([t.text for t in self.parts])

    def to_json(self):
        return {"start_x": self.start,
                "end_x": self.end,
                "text": self.get_text()}
