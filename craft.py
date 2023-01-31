from craft_text_detector import Craft
import click
import numpy as np
import torch
from coors import get_coordinates
import cv2
import statistics


class Box:
    def __init__(self, x1, x2, y1, y2):
        self.x1 = x1
        self.x2 = x2
        self.y1 = y1
        self.y2 = y2

    def get_area(self):
        return abs(self.x1 - self.x2) * abs(self.y1 - self.y2)

    def contains(self, box):
        return is_x_in(box.x1, self) and is_x_in(box.x2, self) and is_y_in(box.y2, self) and is_y_in(box.y1, self)


def craft(image):
    # create a craft instance
    craft = Craft(output_dir=None,
                crop_type="poly",
                export_extra=False,
                link_threshold=0.1,
                text_threshold=0.3,
                long_size=1500,
                cuda= torch.cuda.is_available())
    (real_height, real_width) = image.shape[:2]
    prediction_result = craft_text_detection(image, craft, 0, real_height, real_width)
    copy = image.copy()
    boxes = []
    for i, j in enumerate(prediction_result):
        x1, x2, y1, y2 = get_coordinates(prediction_result[i])
        boxes.append(Box(x1, x2, y1, y2))
        cv2.rectangle(copy, (x1 - 1, y1 - 1), (x2 - 1, y2 - 1), (252, 3, 3), 1)
    chopped = chop_big_boxes(boxes)
    unified = unify(chopped)
    for i, j in enumerate(unified):
        # cv2.putText(copy, f"({x1}, {y1}) ({x2}, {y2})",
        #             (x1, y1),
        #             cv2.FONT_HERSHEY_SIMPLEX,
        #             0.3,
        #             (0, 255, 255),
        #             1,
        #             2)
        cv2.rectangle(copy, (unified[i].x1, unified[i].y1), (unified[i].x2, unified[i].y2), (255, 255, 3), 1)
    cv2.imwrite("/tmp/debug.jpg", copy)
    return unified


def craft_text_detection(image, craft, start, size, width):
    """
    recursive function to helps craft calculate text regions
    """
    try:
        decrease = int(size / 10)
        real_start = start - decrease if start - decrease > 0 else 0
        result = adjust_height(craft.detect_text(image[real_start:start + size, 0:width])['boxes'],
                               real_start)
        amount = len(result)
        click.echo(f"Calculated (0,{start}) ({width}, {start + size}): {amount}", err=True)
        for r in result:
            x1, x2, y1, y2 = get_coordinates(r)
            if x1 != x2 and y1 != y2:
                if real_start == y1:
                    from_start = x2 - size if x2 - size > 0 else 0
                    result = np.concatenate((result, adjust_height(craft.detect_text(image[from_start:x2, 0:width])
                                                                  ['boxes'], from_start)), axis=0)
        return result
    except ValueError:
        first_step = int(size / 2)
        click.echo(f"Downscaling image from {start} to {first_step}", err=True)
        second_step = int(size - first_step)
        first_boxes = craft_text_detection(image, craft, start, first_step, width)
        second_boxes = craft_text_detection(image, craft, start + first_step, second_step, width)
        if len(first_boxes) > 0 and len(second_boxes) > 0:
            return np.concatenate((first_boxes, second_boxes), axis=0)
        else:
            return first_boxes if len(first_boxes) > 0 else second_boxes


def adjust_height(boxes, size):
    """
    calculate real coordinates of parts of the image
    """
    for i, j in enumerate(boxes):
        boxes[i][0][1] = int(boxes[i][0][1]) + size
        boxes[i][2][1] = int(boxes[i][2][1]) + size
    return boxes


def chop_big_boxes(boxes):
    """
    Big boxes sometimes need to be chop in small boxes because CRAFT in some cases mix lines
    """
    median = statistics.median(list(map(lambda b: abs(b.y1 - b.y2), boxes)))
    height = median * 2
    selected = []
    click.echo(f"Max height to be chopped {height}", err=True)
    click.echo()
    for box in boxes:
        click.echo(f"   Box ({box.x1}, {box.y1}), ({box.x2}, {box.y2})", err=True)
        if abs(box.y1 - box.y2) > height:
            click.echo(f"   Chopping...", err=True)
            intersected = list(filter(lambda i: abs(i.y1 - i.y2) <= height and
                                                box.y2 > i.y2 > box.y1 and box.y1 < i.y1 < box.y2 and not
                                                box.x2 > i.x2 > box.x1 and not box.x1 < i.x1 < box.x2, boxes))
            if len(intersected) > 0:
                for i, j in enumerate(intersected):
                    if i == 0:
                        click.echo(f"       Box ({box.x1}, {box.y1}), ({box.x2}, {intersected[i].y1})", err=True)
                        selected.append(Box(box.x1, box.x2, box.y1, intersected[i].y1))
                    click.echo(f"       Box ({box.x1}, {intersected[i].y1}), ({box.x2}, {intersected[i].y2})", err=True)
                    selected.append(Box(box.x1, box.x2, intersected[i].y1, intersected[i].y2))
            else:
                selected.append(box)
        else:
            selected.append(box)
    return sort(selected)


def unify(result):
    """
    Unify overlapped boxes.
    For example [(0,15, (15,30))] overlaps with [(5,10, (25,30))] so the method should return:
        [(0,10, (25,30))]
    """
    unified = []
    for i, j in enumerate(result):
        current = result[i]
        click.echo(f"   Current ({current.x1}, {current.y1}), ({current.x2}, {current.y2})", err=True)
        coincidences = list(filter(lambda i: get_overlapped_percent(i, current) > 20, unified))
        for coincidence in coincidences:
            current.x1 = min(current.x1, coincidence.x1)
            current.y1 = min(current.y1, coincidence.y1)
            current.x2 = max(current.x2, coincidence.x2)
            current.y2 = max(current.y2, coincidence.y2)
            unified.remove(coincidence)
        unified.append(current)
    return unified


def get_overlapped_percent(box1: Box, box2: Box):
    box1_overlapped = are_coordinates_overlap(box1.x1, box1.x2, box1.y1, box1.y2, box2)
    box2_overlapped = are_coordinates_overlap(box2.x1, box2.x2, box2.y1, box2.y2, box1)
    if box1_overlapped or box2_overlapped:
        if box1.contains(box2) or box2.contains(box1):
            return 100
        else:
            return get_partial_overlapped(box1, box2) if box1_overlapped else get_partial_overlapped(box2, box1)
    else:
        return 0


def get_partial_overlapped(box1, box2):
    x1, x2, y1, y2 = get_overlapped_coordinates(box1, box2)
    area = Box(x1, x2, y1, y2).get_area()
    area1 = box1.get_area()
    area2 = box2.get_area()
    return int(max((100 * area) / area2 if area > 0 and area2 > 0 else 0,
                   (100 * area) / area1) if area > 0 and area1 > 0 else 0)


def get_overlapped_coordinates(box1, box2):
    if is_x_in(box1.x1, box2) and is_x_in(box1.x2, box2) or is_y_in(box2.y1, box1) and is_y_in(box2.y2, box1):
        return box1.x1, box1.x2, box1.y1, box2.y2
    elif is_x_in(box2.x1, box1) and is_x_in(box2.x2, box1) or is_y_in(box1.y1, box2) and is_y_in(box1.y2, box2):
        return box2.x1, box2.x2, box2.y1, box1.y2
    else:
        x1 = box1.x1 if is_x_in(box1.x1, box2) else box1.x2
        y1 = box1.y1 if is_y_in(box1.y1, box2) else box1.y2
        x2 = box2.x1 if is_x_in(box2.x1, box1) else box2.x2
        y2 = box2.y1 if is_y_in(box2.y1, box1) else box2.y2
        return x1, x2, y1, y2



def sort(boxes):
    def get_y(box):
        return min(box.y1, box.y2)

    boxes.sort(key=get_y)
    return boxes


def are_x_coordinates_overlap(y1, y2, coors):
    """
    Check if y coordinates of box are overlapped by the others y coordinates
    """
    return is_x_in(y1, coors) and is_x_in(y2, coors)


def are_coordinates_overlap(x1, x2, y1, y2, box):
    """
    Check if coordinates of box are overlapped by the others coordinates
    """
    return (is_x_in(x1, box) and is_y_in(y1, box)) or (is_x_in(x2, box) and is_y_in(y2, box)) or \
           (is_x_in(x1, box) and is_y_in(y2, box)) or (is_x_in(x2, box) and is_y_in(y1, box))


def is_x_in(x, coordinates: Box):
    """
    Check if x coord is in range of coordinates
    """
    return coordinates.x1 >= x >= coordinates.x2 or coordinates.x2 >= x >= coordinates.x1


def is_y_in(y, coordinates):
    """
    Check if y coord is in range of coordinates
    """
    return coordinates.y2 >= y >= coordinates.y1 or coordinates.y1 >= y >= coordinates.y2

